## Script (Python) "content_delete_post.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Notify Rhaptos content edit object that contents deleted
# this exists in order to have only one logAction per delete operation

context.logAction('save')

return state