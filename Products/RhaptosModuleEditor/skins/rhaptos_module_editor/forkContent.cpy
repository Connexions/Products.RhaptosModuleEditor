## Script (Python) "forkContent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=license, return_context=False, id=None
##title= Fork a new version of the module

# Make a copy of ourselves
ws = context.aq_parent
now = DateTime()
if id is None:
    id = context.portal_type.replace(' ', '_')+'.'+now.strftime('%Y-%m-%d')+'.'+now.strftime('%M%S')
ws.manage_clone(context, id)
new_context = ws[id]

# Remove old collaboration requests
new_context.manage_delObjects(new_context.objectIds('Collaboration Request'))

# Reset to same license
new_context.manage_changeProperties(license=license)

# Set parent module
original = context.getBaseObject()
new_context.setParent(original)
new_context.setBaseObject(None)

# Set parent authors
pa = list(context.parentAuthors)
pa.extend([a for a in original.authors if a not in pa])
pa.extend([a for a in original.parentAuthors if a not in pa])
new_context.manage_changeProperties(parentAuthors=pa)

# Set up default roles for new content
user = context.portal_membership.getAuthenticatedMember().getUserName()

new_context.manage_changeProperties(authors=(user,), maintainers=(user,), licensors=(user,), pub_authors=(user,), pub_maintainers=(user,), pub_licensors=(user,), collaborators=(user,))

# Reset all the optional roles to empty
new_context.resetOptionalRoles()

user_role_delta = new_context.generateCollaborationRequests(newUser=True, newRoles={'Author':context.pub_authors})
for p in user_role_delta.keys():
    collabs = list(new_context.getCollaborators())
    if p not in collabs:
        new_context.addCollaborator(p)
        new_context.requestCollaboration(p, user_role_delta[p])
new_context.updateRoleMetadata()
    
# Set state to newly created
new_context.logAction('create', 'Content copied')
new_context.manage_changeProperties(created=now)

# Since we're doing a fork, remove the existing CVS folder
if 'CVS' in new_context.objectIds():
    new_context.manage_delObjects(['CVS'])

# Clear any write locks
for o in new_context.objectValues():
    o.wl_clearLocks()

# This script may be used outside of a FormController context in which 
# case it must return here.
if return_context:
    return new_context

# clear the Google Analytics Tracking Code in the new forked object
if hasattr(new_context, 'GoogleAnalyticsTrackingCode'):
    new_context.setGoogleAnalyticsTrackingCode(None)

psm = context.translate("message_item_created", domain="rhaptos", default="Item created.")
return state.set(context=new_context, portal_status_message=psm)

