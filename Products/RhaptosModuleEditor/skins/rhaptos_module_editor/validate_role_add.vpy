## Script (Python) "validate_role_add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=newRoles=[]
##title=validates the adding of people to content

if not newRoles:
    psm=context.translate("message_no_one_selected", domain="rhaptos", default="No one selected.")
    return state.set(status='failure', portal_status_message=psm)
else:
    return state.set()
