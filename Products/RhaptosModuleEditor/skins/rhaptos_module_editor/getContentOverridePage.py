## Script (Python) "getContentOverridePage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Return URL of page to override content pages under certain conditions

# Short-circuit: if we're not looking at a top-level Rhaptos object
# then don't monkey around with it.  This prevents our special
# collection subobjects from getting messed up
if not hasattr(context, 'nearestRhaptosObject') or context != context.nearestRhaptosObject():
    return

def add_query(url):
    url = context.absolute_url() + '/' + url
    q = context.REQUEST.QUERY_STRING 
    return q and '?'.join([url, q]) or url

url = context.REQUEST.get('URL')
from_select_lens = url.endswith("module_publish_selectlens")
if context.state == 'published' and not from_select_lens:
    return add_query('content_published')

if context.state == 'pending' and not context.portal_membership.checkPermission('Publish Rhaptos Object', context):
    return add_query('content_pending')

# Guarantee that user enters a title by going to initial metadata entry page if they haven't.
# FIXME: modules now do this with an on-screen message and a publication block.
# Would be nice to do the same for collections.
if context.portal_type == 'Collection':
    title = context.Title()
    if (not title) or title == '(Untitled)':
        return add_query('content_title')

