## Script (Python) "module_preview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Display the module, either as PDF or using the index.cnxml display method

# Before previewing, validate
errors = context.validate()
if errors:
    return context.module_invalid(error_validity=errors)

if context.REQUEST.get('format', None) == 'pdf':
    return context.downloadPDF()
else:
    return context.module_render()
