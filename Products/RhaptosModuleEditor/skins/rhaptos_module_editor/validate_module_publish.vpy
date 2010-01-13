## Script (Python) "validate_module_publish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=message=''
##title=Validate module before publishing

status = state.status
msg = state.getKwargs().get('portal_status_message', '')
try:
    published_version = context.content.getRhaptosObject(context.id).latest.version
except KeyError:
    published_version = None

if not message:
    errormsg = context.translate("message_this_field_required", domain="rhaptos", default="This field is required.")
    state.setError('message', errormsg)
    status = 'failure'
    msg = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")

elif published_version and (context.version != published_version):
    status = 'failure'
    msg = context.translate("message_publish_version_conflict", {"context_title":context.Title()}, domain="rhaptos", default="Someone else has edited and published this object (" + context.Title() + ") while you had it checked out. Please make a note of the changes you have made, discard the object, check out a new copy, and make your changes again.")

elif context.getPendingCollaborations():
    status = 'role_error'
    msg = context.translate("message_publish_pending_roles", domain="rhaptos", default="You cannot publish with pending role requests.")

elif not context.authors or not context.maintainers or not context.licensors:
    status = 'role_error'
    msg = context.translate("message_must_specify_roles", domain="rhaptos", default="You must specify at least one Author, Maintainer and Copyright Holder.")

else:
    v_errors = context.validate()
    if v_errors:
        state.setError('validity', v_errors)
        status = 'invalid'
        msg = context.translate("message_module_didnt_validate", domain="rhaptos", default="The module did not validate.  Please fix before publishing.")
    elif context.state == 'created':
        status = 'confirm'
        msg=''
        
return state.set(status=status, portal_status_message=msg)
