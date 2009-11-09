## Script (Python) "downloadPDF"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ids=[]
##title= Returns a PDF version of the module

from Products.CMFCore.utils import getToolByName
pdf_tool = getToolByName(context, 'portal_pdflatex')

objectId = context.objectId
version = context.version
pdf = None
params = {}

if context.isPublic():
    printTool = getToolByName(context,'rhaptos_print')

    if printTool.getStatus(objectId, version, 'pdf') == 'failed':
        return
    else:
        pdf = printTool.getFile(objectId, version, 'pdf')
        if pdf == None:
            pdf = pdf_tool.convertObjectToPDF(context, **params)
            printTool.setFile(objectId, version,'pdf',pdf)
            printTool.setStatus(objectId, version,'pdf','success')
else:
    pdf = pdf_tool.convertObjectToPDF(context, **params)

context.REQUEST.RESPONSE.setHeader('Content-Type', 'application/pdf')
#response.setHeader('Content-Length', len(text))
context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename=%s.pdf' % (objectId or 'New'))
return pdf
