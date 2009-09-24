## Script (Python) "updateLinks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=links=[], delete=[]
##title= Handle submission of links update form

links = filter(lambda l: l.id not in delete, links)
context.setLinks(links)
context.logAction('save')

psm = context.translate("message_links_updated", domain="rhaptos", default="Links updated.")
return state.set(portal_status_message=psm)
