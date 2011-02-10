## Script (Python) "module_import_fetch"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format, fetchURL, came_from=None
##title=Import module contents from a remote URL
# params similar to module_import; format and came_from passed right through

from Products.RhaptosModuleEditor.util import fetchRemoteFile

importFile = fetchRemoteFile(fetchURL)

return context.module_import(format, importFile, came_from=None)
