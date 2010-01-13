## Script (Python) "addLink"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=newLink
##title=Add new link to this object

link = {}

if newLink.target:
    link['url'] = newLink.target
else:
    # If they didn't specify a URL, assemble it from the ID and version
    version = newLink.version or 'latest'
    try:
        link['url'] = context.content.getRhaptosObject(newLink.objectId, version).url()
    except KeyError:
        psm = context.translate("message_invalid_id_or_version", domain="rhaptos", default="Invalid ID or version")
        return state.set(status='failure', portal_status_message=psm)
link['title'] = newLink.title
link['type'] = newLink.category
link['strength'] = newLink.strength

context.doAddLink(link)

psm = context.translate("message_link_added", domain="rhaptos", default="Link added.")
return state.set(portal_status_message=psm, newLink=None)
