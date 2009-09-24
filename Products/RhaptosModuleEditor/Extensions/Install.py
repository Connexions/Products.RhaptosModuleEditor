from Products.LinkMapTool.strengths import upgrade5to3

from Products.Archetypes.Extensions.utils import install_subskin
from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.utils import getToolByName
from Products.RhaptosModuleEditor import ModuleEditor, product_globals as GLOBALS
from cStringIO import StringIO
import string

import logging
logger = logging.getLogger('RhaptosModuleEditor.Install')
def log(msg, out=None):
    logger.info(msg)
    if out: print >> out, msg

def install(self):
    """Register ModuleEditor with the necessary tools. Upgrade requires run as Manager user."""
    out = StringIO()
    log("Starting RhaptosModuleEditor install", out)
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();
    
    # setup tool prep (see also RhaptosSite install)
    setup_tool = getToolByName(portal, 'portal_setup')
    prevcontext = setup_tool.getImportContextID()
    setup_tool.setImportContext('profile-CMFPlone:plone')  # get Plone steps registered
    setup_tool.setImportContext('profile-RhaptosSite:rhaptos-default')  # Rhaptos steps registered (FormController)
    setup_tool.setImportContext('profile-RhaptosModuleEditor:rhaptos-default')  # use profile from this product

    # run all import steps
    steps = ('skins','typeinfo', 'rhaptos_cmfformcontroller')
    log("...running profile steps", out)
    for step in steps:
        log(" - applying step: %s" % step, out)
        status = setup_tool.runImportStep(step)
        log(status['messages'][step], out)
    
    # Make workflow go away
    log("...making workflow empty", out)
    wf_tool = getToolByName(self,'portal_workflow')
    wf_tool.setChainForPortalTypes(['Module'],'')
    
    # upgrades, if necessary
    log("...checking for upgrades", out)
    try:
        lmtool = getToolByName(self, 'portal_linkmap')
        if not getattr(lmtool, '_linkrange_RME', None):
            # this is a little broad, as it will be triggered on first install too,
            # but in that case we shouldn't have any objects to upgrade, so it's okay
            log("Upgrading link strengths from 1-5 to 1-3", out)
            record = StringIO()
            lmtool._linkrange_RME = (1,3)
            # find all RMEs and change their links
            ctool = getToolByName(self, 'portal_catalog')
            allrme = ctool(portal_type='Module')
            counter = 0
            import transaction
            for brain in allrme:
                try:
                    rme = brain.getObject()
                    if rme._links and rme.state != 'published':
                        counter += 1
                        links = rme._links
                        for link in links:
                            # record existing state
                            ldict = {'rme':rme.absolute_url(relative=1),
                                     'target':link['url'], 'title':link['title'], 'strength':link['strength']}
                            record.write(str(ldict)+"\n")
                            log("... %s" % ldict['rme'], out)
                            # update strength value
                            link['strength'] = upgrade5to3(link['strength'])
                        rme._links = links
                        transaction.commit()
                except AttributeError:
                    pass  # objs cataloged in temp folder break on REQUEST; just skip
            olddata = portal.invokeFactory(type_name="File", id="linkconv-rme",
                                           title="RhaptosModuleEditor old 5-level data, from upgrade", file=record)
            olddata = portal[olddata]
            log("Migrated links on %s modules" % counter, out)
            log("5-level data recorded in File at %s" % olddata.absolute_url(), out)
    except AttributeError:
        log("LinkMap Tool does not exist; cannot upgrade links", out)
    
    # setup tool "teardown"
    setup_tool.setImportContext(prevcontext)

    log("Successfully installed RhaptosModuleEditor", out)
    return out.getvalue()

