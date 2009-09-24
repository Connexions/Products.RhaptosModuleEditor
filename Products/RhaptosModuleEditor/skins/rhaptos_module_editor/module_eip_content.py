## Script (Python) "module_preview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Return the module content rendered for EIP
from Products.RhaptosModuleEditor import MODULE_EIP_XSL

# We must prevent the browsers from caching this
context.REQUEST.RESPONSE.setHeader('Pragma','no-cache')
context.REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0')
context.REQUEST.RESPONSE.setHeader('Expires', 'Mon, 26, Jul 1997 05:00:00 GMT')

return context.getDefaultFile().cnxml_view(stylesheet=MODULE_EIP_XSL, wrapper=0)
