## Script (Python) "handleEipRequest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=file=None
##title=
##

if not file:
    raise 'Bad Request', 'No file given.'

name = file.filename.split('\\')[-1]
if context.meta_type == 'Rhaptos Module View':
    context.addImage(name, file=file)
else:
    context.invokeFactory('Image', name, file=file)

#return context.media_listing()
return "OK"
