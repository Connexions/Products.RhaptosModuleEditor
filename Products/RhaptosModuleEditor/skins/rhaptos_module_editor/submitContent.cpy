## Script (Python) "publishContent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=message='', lens_paths=[], **kw
##title= Perform all content submission activities


# log a submit early so that logAction minimization stuff knows we're publishing
newpublish = context.state == 'created'
context.logAction('submit', message)

psm = context.translate("message_item_submitted", domain="rhaptos", default="Item Submitted for Publication.")

return state.set(status='success', portal_status_message=psm)
