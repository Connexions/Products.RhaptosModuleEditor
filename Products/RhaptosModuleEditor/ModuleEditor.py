"""
Web-based editing of modules in Rhaptos repository

Author: Brent Hendricks
(C) 2002-2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

import re
import zLOG
import transaction
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError as XMLParseError
from zope.interface import implements
from DateTime import DateTime
from Persistence import Persistent
from ComputedAttribute import ComputedAttribute
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import getSecurityManager, ClassSecurityInfo, Unauthorized
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from Products.CMFPlone.PloneFolder import PloneFolder
from Products.CMFCore.WorkflowCore import WorkflowAction
from Products.CMFDiffTool.ChangeSet import ChangeSet
from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.utils import getToolByName
from Products.RhaptosCollaborationTool.CollaborationManager import CollaborationManager
from Products.RhaptosCollection.types.CollectionBase import CollectionBase
from Products.LinkMapTool.LinkMapTool import ExtendedLink
from Products.PloneLanguageTool import availablelanguages
from Products.Archetypes.public import DisplayList
from Products.CNXMLDocument import XMLService
from Products.CNXMLDocument import CNXML_SEARCHABLE_XSL as baretext

try:
    from Products.Archetypes.Referenceable import Referenceable
    from Products.Archetypes.interfaces.referenceable import IReferenceable
except ImportError:
    zLOG.LOG("RhaptosModuleEditor", zLOG.INFO, "Archetypes is not installed. Skipping.")
    class Referencable: pass
    class IReferencable: pass


# Import permission names
from Products.CMFCore import CMFCorePermissions
import permissions 


def addModuleEditor(self, id, REQUEST=None):
    """Create an empty ModuleEditor"""
    content_object = ModuleEditor(id)
    self._setObject(id, content_object)
    container = self.this()
    container[id].logAction('create', 'Created module')

class ModuleEditor(PloneFolder, CollaborationManager, Referenceable):
    """
    Module Editor class

    This defines an editor for modules in the Rhaptos system
    """
    try:
        __implements__ = (PloneFolder.__implements__, CollaborationManager.__implements__, IReferenceable)
    except:
        pass  # in case CollabMan grows an interface

    __implements__ = (PloneFolder.__implements__, IReferenceable)
    # we didn't have anything here previous to adding Referenceable, so if no Archetypes, nothing changes

    meta_type = "Module Editor"
    portal_type = 'Module'

    security = ClassSecurityInfo()
    security.declareObjectPublic()

    default_file = 'index.cnxml'
    default_linktypes = ['example', 'prerequisite', 'supplemental']
    #default_roles = ['Author', 'Maintainer', 'Licensor']
    optional_roles = {'Translator': 'Translators', 'Editor': 'Editors'}

    no_rename = 1

    # Module properties
    _properties=({'id':'title', 'type': 'string', 'mode': 'w'},
                 {'id':'version','type':'string', 'mode': 'w'},
                 {'id':'created', 'type':'date', 'mode': 'w'},
                 {'id':'revised','type':'date', 'mode': 'w'},
                 {'id':'authors','type':'lines', 'mode': 'w'},   
                 {'id':'maintainers','type':'lines', 'mode': 'w'},       
                 {'id':'licensors','type':'lines', 'mode': 'w'},
                 {'id':'parentAuthors','type':'lines', 'mode': 'w'},     
                 {'id':'keywords','type':'lines', 'mode': 'w'},
                 {'id':'abstract','type':'string', 'mode': 'w'},
                 {'id':'license','type':'string', 'mode': 'w'},
                 {'id':'language','type':'string', 'mode': 'w'},
                 {'id':'pub_authors','type':'lines', 'mode': 'w'},       
                 {'id':'pub_maintainers','type':'lines', 'mode': 'w'},   
                 {'id':'pub_licensors','type':'lines', 'mode': 'w'},     
                 {'id':'collaborators','type':'lines', 'mode': 'w'},     
                 {'id':'subject','type':'lines', 'mode': 'w'},
                 )

    # Compatibility attributes
    
    # Add a computed "roles" attribute so that optional roles on ModuleEditors
    # can be accessed in the same way as optional role on ModuleViews
    roles = ComputedAttribute(lambda self: self.getRolesDict(),1)
    
    # Force portal content to be true (even though we're a folder) so discussion threads work
    isPortalContent = 1

    def __init__(self, id):
        """Initialize a ModuleEditor instance of the class"""
        DefaultDublinCoreImpl.__init__(self)
        self.id=id
        self.objectId = None

        user = getSecurityManager().getUser().getUserName()
        # Setup default properties  
        self._defaults = {'title' : '(Untitled)',
                          'created': DateTime(),
                          'revised': DateTime(),
                          'version': "**new**",
                          'authors' : [user],
                          'maintainers' : [user],
                          'licensors' : [user],                          
                          'parentAuthors' : [],
                          'keywords': [],
                          'abstract': '',
                          'state': 'created',
                          'language': '',
                          'pub_authors' : [user],
                          'pub_maintainers' : [user],
                          'pub_licensors' : [user],
                          'collaborators' : [user],
                          'subject': (),
                          }

        # Store object properties
        for key, value in self._defaults.items():
            setattr(self, key, value)

        # Set the license separately so it doesn't get cleared by discard
        setattr(self, 'license', '')

        # logAction
        self.timestamp = DateTime()
        self.action = ''
        self.actor = ''
        self.message = ''

        self._links = []
        self._files = []

        self._parent_id = None
        self._parent_version = None

        #self.createTemplate() in manage_afterAdd (way below)


    def __setstate__(self, state):
        """Upgrade annotation instances"""
        Persistent.__setstate__(self, state)

        if self.portal_type == 'Folder':
            self.portal_type = 'Module'

        # Calculate original file list
        if not hasattr(self, '_files') and hasattr(self, self.default_file):
            files = self.objectIds() + self.removed
            for f in self.added:
                files.remove(f)
            self._files = files

        # Make sure the instance doesn't have an _properties
        try:
            del self._properties
        except AttributeError, KeyError:
            pass
        
        # Change back to properties for role storage
        if 'authors' not in self.__dict__.keys():
            self.authors = self.users_with_local_role('Author')
            self.maintainers = self.users_with_local_role('Maintainer')
            self.licensors = self.users_with_local_role('Licensor')

            for u, roles in self.__ac_local_roles__.items():
                try:
                    roles.remove('Author')
                    roles.remove('Maintainer')
                    roles.remove('Licensor')
                except ValueError:
                    pass
                if roles:
                    self.__ac_local_roles__[u] = roles
                else:
                    del self.__ac_local_roles__[u]

        # Add parentAuthors property
        if not hasattr(self, 'parentAuthors'):
            setattr(self, 'parentAuthors', [])

        # Add parent properties
        if not hasattr(self, '_parent_id'):
            setattr(self, '_parent_id', None)
            setattr(self, '_parent_version', None)

        # Set objectId
        if not hasattr(self, 'objectId'):
            if self.state == 'created':
                setattr(self, 'objectId', None)
            else:
                setattr(self, 'objectId', self.id)

    def isPublic(self):
        """Boolean answer true iff collection is in versioned repository.
        Based currently on value of 'state' attribute.
        """
        return self.state == 'public'
    
    security.declarePublic('SearchableText')
    def SearchableText(self):
        """Return the text of the module for searching"""
        cnxml_file = self.getDefaultFile()
        if cnxml_file:
            content = cnxml_file.getSource()
            try:
                # strip XML tags with XSLT if possible
                bare = XMLService.transform(content,baretext)
            except XMLService.XMLParserError:
                # strip non-parsable XML-ish text to the best of our ability
                bare = re.sub('(?s)<.*?>', ' ', content)
        else:
            bare = ''
        return bare

##     FIXME: This fixes various pasting problems but breaks forking :(
##     def _notifyOfCopyTo(self, container, op):
##         """Be picky about where we're copied"""

##         # Don't allow duplicate modules in the same container
##         if self.getId() in container.objectIds():
##             # It's a duplicate if it's a copy, or it's a cut and a different object
##             if op == 0 or container[self.getId()].aq_base != self.aq_base:
##                 raise "DuplicateError", "An object with the id %s already exists here."  % self.getId()

##         # Don't allow modules to be pasted where they don't go
##         if self.portal_type not in [elt.id for elt in container.allowedContentTypes()]:
##             # FIXME: We should *not* be checking this.  RhaptosCollection
##             # should have its manage_paste function fixed so that it
##             # doesn't actuall call _notifyOfCopyTo since the objects
##             # aren't actually copied, they're transformed
##             if not isinstance(container, CollectionBase):
##                 raise "Bad Request", "Modules not allowed here."


    def listFolderContents(self, spec=None, contentFilter=None, suppressHiddenFiles=0 ):
        """Override PloneFolder method to hide CVS folder and put default file first"""

        items = self.contentValues(spec=spec, filter=contentFilter)
        l = []
        for obj in items:
            id = obj.getId()
            v = obj
            try:
                if suppressHiddenFiles and (id[:1]=='.' or id == 'CVS'):
                    raise Unauthorized(id, v)
                if getSecurityManager().validate(self, self, id, v):
                    l.append(obj)
            except (Unauthorized, 'Unauthorized'):
                pass

        # Make sure default_file is first
        f = self.getDefaultFile()
        if f:
            l.remove(f)
            l.insert(0, f)
        return l
                          

    def edit(self):
        """Change the instance's properties """
        pass
    edit = WorkflowAction(edit)


    def getPublishedObject(self):
        """Return the currently published version of this object or
           None if it is newly created"""
        try:
            return self.portal_url.getPortalObject().content.getRhaptosObject(self.objectId)
        except KeyError:
            return None

    def getBaseObject(self):
        """Return the object this working copy is based on"""
        try:
            return self.content.getRhaptosObject(self.objectId, self.version)
        except KeyError:
            return None

    def setBaseObject(self, objectId):
        """Set reference to the object of which this is a version """
        self.objectId = objectId

    def nearestRhaptosObject(self):
        """Return a handle to ourself, even in an acquisition context"""
        return self

    def url(self):
        """Return a full url to this object, like on RhaptosCollection or ModuleView"""
        return self.absolute_url()

    def setState(self, targetstate):
        """Set the state of the module forcefully."""
        self.state = targetstate

    def setParent(self, parent):
        if parent:
            self._parent_id = parent.objectId
            self._parent_version = parent.version
        else:
            self._parent_id = self._parent_version = None

    def getParent(self):
        if self._parent_id:
            try:
                return self.content.getRhaptosObject(self._parent_id, self._parent_version)
            except KeyError:
                return None

    def getParentId(self):
        return self._parent_id
    
    def createTemplate(self):
        """Create a template for the module.  Overwrites module contents."""
        self.invokeFactory('CNXML Document', self.default_file)  # FIXME: fails if exists
        self.getDefaultFile().createTemplate(objectId=self.objectId or 'new')
        self._writeMetadata()

    security.declareProtected(View, 'getMetadata')
    def getMetadata(self):
        """Return the metdata for this module as a dictionary.
        See also this method in RhaptosCollection.types.Collection
        """
        metadata = {}

        # Pull some metadata from properties...
        for pair in self.propertyItems():
            metadata[pair[0]] = pair[1]

        # ...some from attributes...
        for att in ['objectId', 'roles']:
            metadata[att] = getattr(self, att)

        # ...look inside the optional roles: translators, editors typically
        for role, members in self.roles.items():
            metadata[role] = members
        
        # ... and calculate others
        curFiles = self.objectIds()
        metadata['added'] = [x for x in curFiles if x not in self._files]
        metadata['removed'] = [x for x in self._files if x not in curFiles]
        
        repos = getToolByName(self, 'content')
        metadata['repository'] = repos.absolute_url()
        
        pubobj = self.getPublishedObject()
        if pubobj:
            metadata['url'] = pubobj.url
        
        pobj = self.getParent()
        parent = {}
        if pobj:
            parent['url'] = pobj.url
        metadata['parent'] = parent
        
        return metadata

    def getLinks(self):
        """Get overlay links"""
        links = []
        source = self.absolute_url()
        count = 0
        for l in self._links:
            now=DateTime()
            id = 'Link.'+now.strftime('%Y-%m-%d')+'.'+now.strftime('%M%S')+'.'+str(count)
            count += 1
            link = ExtendedLink(id)
            link.edit(source, l['url'], l['title'], l['type'].split(':')[-1], int(l['strength']))
            links.append(link)
        return links

    def setLinks(self, links):
        """Change module links"""
        self._links = [{'url':l.target, 'title':l.title, 'type':l.category.lower(), 'strength':l.strength} for l in links]
        self._p_changed = 1
        self.getDefaultFile().setFeaturedLinks(self._links)
        
    def getRolesDict(self):
        """Return the optional roles for this object"""

        role_dict = {}
        opt_roles = getattr(self,'optional_roles',{})
        for role in opt_roles.keys():
            role_name = role.lower()+'s'
            users = list(getattr(self,role_name,[]))
            if users:
                role_dict[role_name] = list(getattr(self,role_name,[]))
        return role_dict

    def resetOptionalRoles(self):
        """Set all the optional roles on the object to empty"""
        
        opt_roles = getattr(self,'optional_roles',{})
        for role in opt_roles.keys():
            role_name = role.lower()+'s'
            setattr(self,role_name,[])
            setattr(self,'pub_'+role_name,[])


    def editMetadata(self):
        """Edit the metadata properties."""

        # Update metadata in the CNXML file
        self._writeMetadata()

    def _getSource(self):
        """Get the published source, or local source if modified"""
        # If the module is published, use the repository copy
        if self.state == 'published': 
            module = self.content.getRhaptosObject(self.objectId, 'latest')
            source = module.normalize()
        else: # Otherwise use the local copy
            source = self.getDefaultFile().getSource()

        return source
    

    def getSourceLines(self):
        """Display lines of module source."""
        source = self._getSource()
        return [l.rstrip() for l in source.split('\n')]


    def updateMetadata(self):
        """Update the metadata to the latest from the repository"""

        # Copy metadata from metadata
        module = self.content.getRhaptosObject(self.objectId, 'latest')

        def_roles = [r.lower()+'s' for r in self.default_roles]
        opt_roles = [r.lower()+'s' for r in getattr(self,'optional_roles', {}).keys()]
        collab = []
        roles={}
        
        # Default ordering for roles: Authors before Maintainers before Licensors... optional roles last
        for role in def_roles:
            for u in list(getattr(module,role)):
                if u not in collab:
                    collab.append(u)
        for role in opt_roles:
            users = list(module.roles.get(role,()))
            if users:
                for u in users:
                    if u not in collab:
                        collab.append(u)

        # Ordering role lists to maintain consistency with the collaborators field
        for role in def_roles:
            role_list = list(roles.setdefault(role,[]))
            for c in collab:
                if c in getattr(module,role):
                    role_list.append(c)
                    roles[role]=role_list
                    
        for role in opt_roles:
            role_list = list(roles.setdefault(role,[]))
            for c in collab:
                users = list(module.roles.get(role,()))
                if users:
                    if c in users:
                        role_list.append(c)
                        roles[role]=role_list
            

        self.manage_changeProperties({'title': module.name,
                                      'created': module.created,
                                      'revised': module.revised,
                                      'authors': roles['authors'], 
                                      'maintainers': roles['maintainers'],        
                                      'licensors': roles['licensors'],
                                      'parentAuthors': module.parentAuthors, 
                                      'version': module.version,
                                      'abstract': module.abstract,
                                      'keywords': module.keywords,
                                      'license': module.license,
                                      'language': module.language,
                                      'pub_authors': roles['authors'], 
                                      'pub_maintainers': roles['maintainers'],    
                                      'pub_licensors': roles['licensors'],        
                                      'collaborators': collab
                                      }
                                     )

        self.subject = module.subject

        for role in opt_roles:
            setattr(self,role,list(roles[role]))
            setattr(self,'pub_'+role,list(roles[role]))

        self.objectId = module.objectId

        # Cancel any pending collaboration requests
        self.deleteCollaborationRequests()

        # Set the correct parent module
        self.setParent(module.getParent())

    def updateAuthorLinks(self):
        """Update author links to the latest from the DB"""

        self._links = self.content.getRhaptosObject(self.objectId, 'latest').getContextLinks()
        self._p_changed = 1
        #self.getDefaultFile().setFeaturedLinks(self._links)  # updateMetadata is called after for each use

    def doAddLink(self, link):
        """Add a link to the link list"""
        self._links.append(link)
        self._p_changed = 1
        self.getDefaultFile().setFeaturedLinks(self._links)
        self.logAction('save') # update modification date, reindex

    security.declarePublic('checkout')
    def checkout(self, objectId=None, REQUEST=None):
        """Check out this module from the repository"""

        # If an objectId was specified, use it. otherwise use what
        # we've already got
        if objectId:
            self.objectId = objectId

        # FIXME: we should check that the current objectId is valid

        # Checkout this module through the repository
        moduleView = self.content.getRhaptosObject(self.objectId, 'latest')
        moduleView.checkout(self)

        # Store the list of checked-out files so we can compare later
        self._files = self.objectIds()
        self._p_changed = 1

        # Get latest links
        self.updateAuthorLinks()

        # Get the latest version of metadata 
        self.updateMetadata()

        # Note the checkout in the properties
        self.logAction('checkout')

        # Clear the metadata out of the default file
        #self.getDefaultFile().clearMetadata()

        # adopt the Google Analytics tracking code from the version folder
        versionFolder = moduleView.aq_parent
        if hasattr(versionFolder, '_GoogleAnalyticsTrackingCode'):
            self.setGoogleAnalyticsTrackingCode(versionFolder.getGoogleAnalyticsTrackingCode())

    def computeChanges(self):
        name = ".change_set"
        if hasattr(self.aq_base, name):
            delattr(self, name)
        cs = ChangeSet(name).__of__(self)
        setattr(self, name, cs)
        transaction.savepoint()      # XXX TODO JCC: why?
        m = self.getBaseObject()
        cs.computeDiff(m, self, exclude=self.excludedIds())
        # don't index, because it never gets unindexed on delete because it's not in the folder contents
        # unindex contents, since the .change_set object itself never seems to get indexed
        for elt in cs.objectValues():
            elt.unindexObject()  ### XXX JCC: it would be better to not index at all, but that would require
                                 ###   a separate class for Patch, which needs to be indexed. Not too bad, but
                                 ###   this is rare enough that I'm okay with this.
        return cs

    def excludedIds(self):
        """Return excluded items when performing diffs"""
        exclude = ['CVS', '.change_set', 'index.cnxml.pre-v06', 'index.cnxml.pre-v07','index_auto_generated.cnxml']
        exclude.extend(self.objectIds('Collaboration Request'))
        return exclude
        
    def validate(self):
        """Validate this module.
        Returns list of (linenumber, error) tuples if error; empty list if valid.
        """
        f = self.getDefaultFile()
        if f:
            return f.validate()
    
    def wellformed(self):
        """Say if this module is correct XML; weaker than validation.
        Returns error string if not well-formed; None if good.
        """
        f = self.getDefaultFile()
        err = None
        if f:
            # FIXME: probably should delegate, like 'validate' does
            src = f.getSource()
            try:
                dom = parseString(src) # minidom; easy, maybe not as cheap as possible. FIXME: custom expat?
            except XMLParseError, e:
                err = str(e)
        return err

    def revert(self):
        """Revert to last-published version (or blank)"""
        self.manage_delObjects(self.objectIds())
        self._files = []
        self._p_changed = 1

        if self.state == 'created':
            # If it's a new module, re-initialize with original properties
            self._reset()
            self.createTemplate()
        else:
            # Otherwise, restore metadata and links from repository
            self.updateAuthorLinks()
            self.updateMetadata()

        self.reindexObject()

    def logAction(self, action, message=''):
        """Log last user action."""
        user = getSecurityManager().getUser()

        # State transition table
        nextState = {'create':'created',
                     'add':'published',
                     'save':'modified',
                     'upgrade':'modified',
                     'checkout':'checkedout',
                     'submit':'published',
                     'discard':'published'}

        # Do state changes unless the current state is 'created'
        if self.state == 'created' and action != 'submit':
            state = self.state
        else:
            state = nextState[action]

        self.state = state
        self.timestamp = DateTime()
        self.action = action
        self.actor = user.getUserName()
        self.message = message

        # Reindex the object in the catalog so that the folder listings will update
        self.reindexObject()


    def upgrade(self):
        """Upgrade to the next version of the module product"""
        pass


    def getDefaultFile(self):
        """Return the file object used in the default 'view' of this module"""
        pl = getToolByName(self, 'portal_languages')
        langs = pl.getLanguageBindings()
        files = self.objectIds()
        for f in ['index.%s.cnxml' % l for l in langs[0:2]]:
            if f in files:
                return self[f]
        try:
            return self[self.default_file]
        except KeyError:
            return None

    def getLanguageWithSubtypes(self,lang,*args,**kwargs):
        """get language codes w/ subtypes"""
        
        c = availablelanguages.countries
        locales = [(l[0],c[l[0][3:].upper()]) for l in availablelanguages.combined.items() if l[0].startswith(lang)]
        locales.sort(lambda x, y: cmp(x[1], y[1]))
        
        if len(locales):
            locales.insert(0,(lang,'None'))
        else:
            locales = [(lang,'(none available)')]
        return DisplayList(locales)
        
    def getLanguagesWithoutSubtypes(self):
        """get language codes that have no subtypes"""
        
        sl={}.fromkeys([l[:2] for l in availablelanguages.combined.keys()]).keys()
        langs = [l for l in availablelanguages.languages.keys() if l not in sl]
        langs.sort()
        return langs
    
    # internal functions #######################################################
    def _writeMetadata(self):
        """Write out metadata to CNXML file"""
        file = self.getDefaultFile()
        if file:
            # FIXME: all these do an update_data; we really only need one...
            file.setTitle(self.title)
            file.setMetadata()
            file.setFeaturedLinks(self._links)

        # Fix content type since metadata setting messes it up
        self.REQUEST.RESPONSE.setHeader('Content-type','text/html')

    def _reset(self):
        """Reset the module to its initial state"""

        self.manage_changeProperties(self._defaults)
        self._links = []
        self._p_changed = 1

    def getLinkTypes(self):
        """Hard-coded list of support link types"""
        return self.default_linktypes

    security.declarePublic('getAboutActions')
    def getAboutActions(self):
        return [{'id':'module_view', 'url':'module_view', 'name':'View'},
                {'id':'about', 'url':'about', 'name':'About'},
                {'id':'history', 'url':'history', 'name':'History'},
                {'id':'print', 'url':'module_view?format=pdf', 'name':'Print'}]

    def getObjectActions(self):
        url = self.absolute_url()
        actions = []
        if self.state != 'published':
            actions.append({'id':'publish', 'url':url+'/module_publish', 'name':'Publish'})

            if self.state != 'created':
                actions.append({'id':'patch', 'url':url+'/module_send_patch', 'name':'Suggest Edits'})
                actions.append({'id':'fork', 'url':url+'/confirm_fork', 'name':'Derive Copy'})

            actions.append({'id':'discard', 'url':url+'/confirm_discard', 'name':'Discard'})
        return actions
            

    def getViewActions(self):
        if self.state != 'published':
            url = self.absolute_url()
            actions = [{'id':'view', 'url':url+'/module_view', 'name':'Online'},
                       {'id':'print', 'url':url+'/module_view?format=pdf', 'name':'Print'},
                       {'id':'source', 'url':url+'/module_source', 'name':'Source'},]
            if self.state != 'created':
                actions.append({'id':'diff', 'url':url+'/diff', 'name':'Changes'})
            return actions
        else:
            url = self.getPublishedObject().url()
            return [{'id':'view', 'url':url, 'name':'Online'},
                    {'id':'print', 'url':url+'?format=pdf', 'name':'Print'},
                    {'id':'source', 'url':self.absolute_url()+'/module_source', 'name':'Source'},
                    ]

    def get_size(self):
        """ Used for FTP and apparently the ZMI now too """
        size = 0
        for obj in self.objectValues():
            if hasattr(obj.aq_base, "get_size"):
                size += obj.get_size()
        return size
    
    def ModificationDate(self):
        """DC/Plone hook for modification date; so catalog will play nice"""
        return self.timestamp


    ## HOOKS for Referenceable
    def manage_afterAdd(self, item, container):
        #Get browser set language. May want to have a userpref default lang.
        lang_tool = getToolByName(self,'portal_languages')
        langs=lang_tool.getLanguageBindings()
        self.language = langs[0]
        self._defaults['language'] = langs[0]

        if not self.getDefaultFile():
            self.createTemplate()

        PloneFolder.manage_afterAdd(self, item, container)
        try: Referenceable.manage_afterAdd(self, item, container)   # considered optional
        except AttributeError: pass
        try: CollaborationManager.manage_afterAdd(self, item, container)  # in case it grows one
        except AttributeError: pass


    def manage_afterClone(self, item):
        PloneFolder.manage_afterClone(self, item)
        try: Referenceable.manage_afterClone(self, item)
        except AttributeError: pass
        try: CollaborationManager.manage_afterClone(self, item)
        except AttributeError: pass

    def manage_beforeDelete(self, item, container):
        PloneFolder.manage_beforeDelete(self, item, container)
        try: Referenceable.manage_beforeDelete(self, item, container)
        except AttributeError: pass
        try: CollaborationManager.manage_beforeDelete(self, item, container)
        except AttributeError: pass

    #security.declareProtected('Edit Rhaptos Object', 'setGoogleAnalyticsTrackingCode')
    security.declarePublic('setGoogleAnalyticsTrackingCode')
    def setGoogleAnalyticsTrackingCode(self, GoogleAnalyticsTrackingCode):
        """set the Google Analytics Tracking Code"""
        self.GoogleAnalyticsTrackingCode = GoogleAnalyticsTrackingCode

    security.declarePublic('getGoogleAnalyticsTrackingCode')
    def getGoogleAnalyticsTrackingCode(self):
        """set the Google Analytics Tracking Code"""
        if hasattr(self,'GoogleAnalyticsTrackingCode'):
            return self.GoogleAnalyticsTrackingCode
        else:
            return None

InitializeClass(ModuleEditor)
