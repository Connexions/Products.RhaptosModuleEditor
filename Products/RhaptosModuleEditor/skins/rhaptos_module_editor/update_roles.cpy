## Script (Python) "updateRoles"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=updateRoles={}, deleteRoles=[], cancelRoles=[]
##title= Handle submission of role update form

delete = []
portal_status_message = ''

#user_role_delta = {}
pending = context.getPendingCollaborations()

collabs = context.getCollaborators()

user_role_delta = context.generateCollaborationRequests(newUser=False, newRoles=updateRoles, deleteRoles=deleteRoles)
        
for p in user_role_delta.keys():
    if p in pending.keys():
        new_changes = pending[p].roles.copy()
        for role in user_role_delta[p]:
            delta = user_role_delta[p][role]
            if role in new_changes:
                if new_changes[role] != delta:
                    new_changes.pop(role)
                elif new_changes[role] == delta:
                    #Shouldn't happen
                    psm = context.translate("message_role_change_matches_error", domain="rhaptos")
                    return state.set(status='failure', portal_status_message= portal_status_message +psm)
            else:
                new_changes[role] = delta
        if not new_changes:
            context.manage_delObjects(pending[p].id)
        else:
            context.editCollaborationRequest(pending[p].id, new_changes)
    else:
        context.requestCollaboration(p, user_role_delta[p])

for u in cancelRoles:
    # Only delete the request if it wasn't already deleted above by undoing the checkbox changes
    if u in context.getPendingCollaborations():
        # Revert the new roles back to the published version
        context.reverseCollaborationRequest(pending[u].id)
        
        # Delete the collaboration request
        context.manage_delObjects(pending[u].id)

#for r in context.getCollaborationRoles():
#    role_name = r.lower() + 's'
#    old_role = list(context[role_name])
#    if not old_role:
#        portal_status_message = portal_status_message + 'There are currently no ' + role_name + ' for this object!  You must add at least one ' + r.lower() + ' before it may be published. '

#Get the collaborators again if they have changed
all_roles = {}
for rolename in context.default_roles + getattr(context, 'optional_roles', {}).keys():
    for r in getattr(context,rolename.lower()+'s',[]):
        all_roles[r]=None
    for r in getattr(context, 'pub_'+rolename.lower()+'s', []):
        all_roles[r]=None
    
collabs = context.getCollaborators()
for c in collabs:
    if c not in all_roles.keys():
        context.removeCollaborator(c)
    
context.logAction('save')
psm = context.translate("message_roles_updated", domain="rhaptos", default="Roles updated.")
return state.set(portal_status_message=psm + ' ' + portal_status_message)
