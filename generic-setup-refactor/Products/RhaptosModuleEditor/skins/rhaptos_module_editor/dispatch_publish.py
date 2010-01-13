## Script (Python) "validate_patchfork"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Determine what type of publishing (publish, patch, or fork) to do
REQUEST=context.REQUEST

status, errors = REQUEST.get('validation_status', 'success'), REQUEST.get('errors', {})
if errors or status != 'success':
    psm = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return (status, errors, {'portal_status_message':REQUEST.get('portal_status_message',psm)})

if REQUEST.has_key('patch'):
    return ('patch', {}, {})
elif REQUEST.has_key('fork'):
    return ('fork', {}, {})
elif REQUEST.has_key('publish'):
    return ('publish', {}, {})
else:
    raise ValueError, "How did you get here"
