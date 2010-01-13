## Script (Python) "deleteContent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Delete object from container

# Ask our parent to delete us and then redirect there
p = context.aq_parent
p.manage_delObjects(context.id)

psm = context.translate("message_item_deleted", domain="rhaptos", default="Item deleted.")
return state.set(context = p, portal_status_message=psm)

