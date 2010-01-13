## Script (Python) "rmeVersionInfo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Returns info about version state of RhaptosModuleEditor
# return dict with default file, versionfolder, latest published object, and text version, if known
# any or all may be None, if not found

pubobj = None
latest = None
indexcnxml = None
cnxmlvers = None

if context.portal_type == 'Module':
    pubobj = context.getPublishedObject()
    latest = pubobj and pubobj.latest or None
    
    indexcnxml = context.getDefaultFile()
    if indexcnxml:
        cnxmlvers = indexcnxml.getVersion()

return {'pubobj':pubobj,
        'latest':latest,
        'indexcnxml':indexcnxml,
        'cnxmlvers':cnxmlvers}