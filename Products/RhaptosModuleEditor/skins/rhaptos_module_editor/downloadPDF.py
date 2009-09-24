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
objectId = context.objectId or 'New'

params = {}

pdf = pdf_tool.convertObjectToPDF(context, **params)
context.REQUEST.RESPONSE.setHeader('Content-Type', 'application/pdf')
#response.setHeader('Content-Length', len(text))
context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename=%s.pdf' % objectId) 
return pdf
