## Script (Python) "validate_add_link"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=newLink=None
##title=Validate added link


if not newLink:
    psm = context.translate("message_one_link_required", domain="rhaptos", default="At least one link required.")
    return state.set(status='failure', portal_status_message=psm)

elif not newLink.title:
    psm = context.translate("message_specify_link_title", domain="rhaptos", default="You must specify a link title.")
    return state.set(status='failure', portal_status_message=psm)

elif not newLink.target and not newLink.objectId:
    psm = context.translate("message_specify_url_or_object", domain="rhaptos", default="You must specify either a URL or an object as the link target.")
    return state.set(status='failure', portal_status_message=psm)

else:
    return state.set()
