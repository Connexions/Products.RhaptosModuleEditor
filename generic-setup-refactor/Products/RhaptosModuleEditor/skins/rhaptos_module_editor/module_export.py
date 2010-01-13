## Script (Python) "module_export"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format
##title=Export module contents

from Products.CNXMLTransforms.helpers import doTransform
from Products.CMFCore.utils import getToolByName

f = context.getDefaultFile()
source = f.getSource()
objectId = context.objectId or context.getId().replace('.','-')
name = "%s-%s.cnxml" % (objectId, format)
isPublished = ( hasattr(context, 'state') and context.state == 'public' )

if format == 'plain':
    result = source
    if isPublished:
        objectVersion = context.getId() == 'latest' and context.version or context.getId()
        name = "%s_%s.cnxml" % (objectId,objectVersion)
elif format == 'authentic':
    result = doTransform(context, "cnxml_to_authentic", source)[0]
elif format == 'zip':
    if isPublished:
        objectVersion = context.getId() == 'latest' and context.version or context.getId()
        printTool = getToolByName(context,'rhaptos_print')
        result = printTool.getFile(objectId, objectVersion, 'zip')
        if result is None:
            result = doTransform(context, "folder_to_zip", context)[0]
            if result is not None:
                printTool.setFile(objectId, objectVersion, 'zip', result)
        name = "%s_%s.zip" % (objectId,objectVersion)
    else:
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
