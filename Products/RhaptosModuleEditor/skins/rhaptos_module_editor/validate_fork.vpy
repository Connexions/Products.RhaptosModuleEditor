## Script (Python) "validate_fork"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=agree=''
##title=Validate forking request

if not agree:
    psm = context.translate("message_agree_to_license_to_proceed", domain="rhaptos", default="To proceed, you must agree to the license.")
    state.setError('agree', psm, 'agree_required')
    return state.set(status='failure', portal_status_message=psm)
else:
    return state
