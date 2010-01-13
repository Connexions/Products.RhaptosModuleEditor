## Script (Python) "update_text"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contents=''
##title= Save the module's text

context.getDefaultFile().setSource(contents, idprefix="fs-")
context.editMetadata()
context.logAction('save')
psm = context.translate("message_saved", domain="rhaptos", default="Saved.")
return state.set(portal_status_message=psm, edit_source=1)
