## Script (Python) "addPeople"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=newRoles={}
##title= Add contributors to this object

portal_status_message = ''
user_role_delta = context.generateCollaborationRequests(newUser=True, newRoles=newRoles)
added = []
omitted = []

for p in user_role_delta.keys():
    collabs = list(context.getCollaborators())
    if p not in collabs:
        context.addCollaborator(p)

        context.requestCollaboration(p, user_role_delta[p])
        added.append(p)
    else:
        omitted.append(p)

list_seperator = context.translate("list_seperator", domain="rhaptos", default=", ")
if added:
    portal_status_message = portal_status_message + context.translate("message_users_added", {"added_ids":list_seperator.join(added)}, domain="rhaptos", default='Users added: ' + ', '.join(added) + ' ')
if omitted:
    portal_status_message = portal_status_message + context.translate("message_users_already_have_roles", {"omitted_ids":list_seperator.join(omitted)}, domain="rhaptos", default='Users omitted because they already have roles: ' + ', '.join(omitted) + ' ')

context.logAction('save')

return state.set(portal_status_message=portal_status_message)



