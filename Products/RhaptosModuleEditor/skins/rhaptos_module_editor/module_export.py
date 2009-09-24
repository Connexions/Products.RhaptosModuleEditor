## Script (Python) "module_export"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format
##title=Export module contents

from Products.CNXMLTransforms.helpers import doTransform

f = context.getDefaultFile()
source = f.getSource()
objectId = context.objectId or context.getId().replace('.','-')
name = "%s-%s.cnxml" % (objectId, format)

if format == 'plain':
    result = source
elif format == 'authentic':
    result = doTransform(context, "cnxml_to_authentic", source)[0]
elif format == 'zip':
    result = doTransform(context, "folder_to_zip", context)[0]
    name = "%s.zip" % objectId
elif format == 'xhtml':
    result = doTransform(context, "module_to_xhtmlzip", context)[0]
    #name = "%s.zip" % objectId
    name = "%s.zip" % objectId
elif format == 'ims':
    result = doTransform(context, "folder_to_ims", context)[0]
    name = "%s.pif.zip" % objectId

context.REQUEST.RESPONSE.setHeader("Content-Disposition", "attachment; filename=%s" % name)
context.REQUEST.RESPONSE.setHeader("Content-Type", "mozilla-ignores-content-disposition")

return result
