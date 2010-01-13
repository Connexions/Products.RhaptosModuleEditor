## Script (Python) "editInPlace"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=displays the CNXML file as part of a module
from Products.RhaptosModuleEditor import MODULE_EIP_XSL
from AccessControl import Unauthorized

if not context.portal_membership.checkPermission('Edit Rhaptos Object', context):
    raise Unauthorized, "You are not allowed to edit this content"
if context.state != 'public':
    raise ValueError, "Edit-In-Place only allowed on published content"
elif context.doctype.find('0.5') == -1:
    raise ValueError, "Edit-In-Place not available for 0.4 modules"
elif context.version != context.latest.version:
    raise ValueError, "Edit-In-Place only available on most recently published version"

return context.module_render(stylesheet=MODULE_EIP_XSL)
