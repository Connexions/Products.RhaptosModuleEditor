## Script (Python) "uploadss"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

import zLOG

f = context.getDefaultFile()

listWorkFiles = f.findReferencedWorkFiles(context)

if len(listWorkFiles) > 0:
    zLOG.LOG("uploadWorkFiles", zLOG.INFO, "number of workarea files found referenced in the module: " + str(len(listWorkFiles)))

listUploadedFiles = []

for pathWorkFile in listWorkFiles:
    zLOG.LOG("uploadWorkFiles", zLOG.INFO, "processing: " + str(pathWorkFile))
    try:
        objWorkFile = context.restrictedTraverse(pathWorkFile)
    except e:
        zLOG.LOG("uploadWorkFiles", zLOG.INFO, "context.restrictedTraverse(" + str(pathWorkFile) + ") failed.")
        objWorkFile = None
    if objWorkFile:
        # if file is already in module, we need to delete it
        if objWorkFile.getId() in context.contentIds():
            context.manage_delObjects(objWorkFile.getId())

        # cut and paste workarea file into module
        workarea = objWorkFile.aq_parent
        objCopiedWorkFile = workarea.manage_copyObjects(objWorkFile.getId())
        context.manage_pasteObjects(objCopiedWorkFile)

        strBaseFile = str(pathWorkFile).split('/')[-1]
        listUploadedFiles.append(strBaseFile)

if len(listUploadedFiles) > 0:
    strMsg = 'The following file(s) have copied into the module during the publish process:'
    bFirstTime = True
    for strFile in listUploadedFiles:
        if bFirstTime:
            strMsg += ' ' + strFile
        else:
            strMsg += ', ' + strFile
        bFirstTime = False
    strMsg += '.'
    zLOG.LOG("uploadWorkFiles", zLOG.INFO, "return the following status message:\n" + strMsg)
else:
    strMsg = ''

return strMsg

