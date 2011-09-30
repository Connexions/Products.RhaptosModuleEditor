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
edit_source = context.REQUEST.get('edit_source', 1)
if edit_source != 0:
  state.set(edit_source=edit_source)

return state.set(portal_status_message=psm)
