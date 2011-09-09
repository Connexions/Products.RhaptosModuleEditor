## Script (Python) "validate_description_of_changes_submit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=description_of_changes=''
##title=Validate description of changes. 

status = state.status
msg = state.getKwargs().get('portal_status_message', '')

if not description_of_changes:
    errormsg = context.translate(
        "description_of_changes_this_field_required",
        domain="rhaptos",
        default="This field is required.")
    state.setError('message', errormsg)
    status = 'failure'
    msg = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
        
return state.set(status=status, portal_status_message=msg)
