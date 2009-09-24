## Script (Python) "discardContent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Discard Content

# We do this first so that the 'revised' date can be overwritten
context.logAction('discard')
context.revert()

psm = context.translate("message_changes_discarded", domain="rhaptos", default="Changes discarded.")
return state.set(portal_status_message=psm)
