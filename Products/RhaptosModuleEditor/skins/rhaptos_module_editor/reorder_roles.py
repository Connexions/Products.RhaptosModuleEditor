## Python Script "folder_position"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=position, id, updateRoles={}
##title=Move objects in a ordered folder
##
from Products.PythonScripts.standard import url_quote

collabs = list(context.getCollaborators())
new_collabs = collabs[:]

if position.lower()=='up':
    ind = collabs.index(id)
    if ind:
        collabs.remove(id)
        collabs.insert(ind-1,id)
        context.manage_changeProperties({'collaborators':tuple(collabs)})

if position.lower()=='down':
    ind = collabs.index(id)
    if ind < (len(collabs) -1):
        collabs.remove(id)
        collabs.insert(ind+1,id)
        context.manage_changeProperties({'collaborators':tuple(collabs)})

if position.lower()=='top':
    collabs.remove(id)
    collabs.insert(0,id)
    context.manage_changeProperties({'collaborators':tuple(collabs)})

if position.lower()=='bottom':
    collabs.remove(id)
    collabs.append(id)
    context.manage_changeProperties({'collaborators':tuple(collabs)})

for r in ['authors','maintainers','licensors','pub_authors','pub_maintainers','pub_licensors']:
    old_role = getattr(context,r)
    new_role = []
    for p in collabs:
        if p in old_role:
            new_role.append(p)
    context.manage_changeProperties({r:tuple(new_role)})

msg=context.translate("message_item_position_changed", domain="rhaptos", default="Item's position has changed.")
request = context.REQUEST
response = request.RESPONSE

ref = getattr(request, 'HTTP_REFERER', None)
if ref:
    return response.redirect(ref)
return response.redirect('%s/%s?portal_status_message=%s' % (context.absolute_url(),
                                                             'content_roles',
                                                             url_quote(msg)) )
