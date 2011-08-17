## Script (Python) "module_import"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format, importFile, came_from=None
##title=Import module contents

from Products.CNXMLTransforms.helpers import OOoImportError, doTransform, makeContent
import transaction
from AccessControl import getSecurityManager
from Products.CNXMLDocument import XMLService

psm = context.translate("message_import_completed", domain="rhaptos", default="Import completed.")

text = importFile.read()
if not text:
    message = context.translate("message_must_select_file_to_upload", domain="rhaptos",
                                default="You must select a file to upload.")
    return state.set(status='failure', portal_status_message=message)

## CNXML
if format == 'plain':
    context.getDefaultFile().setSource(text, idprefix='imp-')

## Authentic/XMLSpy
elif format == 'authentic':
    try:
        text = doTransform(context, "authentic_to_cnxml", text)[0]
    except ValueError:
        message = context.translate("message_error_select_correct_format", domain="rhaptos",
                                    default="Error parsing file. Be sure to select the correct import format.")
        return state.set(status='failure', portal_status_message=message)
    context.getDefaultFile().setSource(text, idprefix='au-')

## XHTML (experimental)
elif format == 'xhtml':
    text = doTransform(context, "xhtml_to_cnxml", text)[0]
    context.getDefaultFile().setSource(text, idprefix='xhtml-')

## Word/OpenOffice.org
elif format in ('msword', 'openoffice'):
    prefix = format=='msword' and 'word-' or 'oo-'
    context.manage_delObjects([i.getId() for i in context.listFolderContents(suppressHiddenFiles=1)])
    try:
        kwargs = {'original_file_name':importFile.filename, 'user_name':getSecurityManager().getUser().getUserName()}
        text, subobjs = doTransform(context, "oo_to_cnxml", text, meta=0, **kwargs)
        context.invokeFactory('CNXML Document', context.default_file, file=text, idprefix=prefix)
        makeContent(context, subobjs)
        #for elt in subobjs.items():    # this is from when OO export images had no extension, I think.
        #    context.invokeFactory('Image', elt[0], file=elt[1])
    except OOoImportError, e:
        transaction.abort()
        message = context.translate("message_could_not_import", {"errormsg":e}, domain="rhaptos",
                                    default="Could not import file. %s" % e)
        return state.set(status='failure', portal_status_message=message)

## LaTeX
elif format in ('latex'):
    context.manage_delObjects([i.getId() for i in context.listFolderContents(suppressHiddenFiles=1)])
    try:
        kwargs = {'original_file_name':importFile.filename, 'user_name':getSecurityManager().getUser().getUserName()}
        text, subobjs = doTransform(context, "latex_to_folder", text, meta=0, **kwargs)
        context.invokeFactory('CNXML Document', context.default_file, file=text, idprefix='latex-')  # make index.cnxml
        makeContent(context, subobjs)                                             # make other resources
    except OOoImportError, e:
        transaction.abort()
        message = context.translate("message_could_not_import", {"errormsg":e}, domain="rhaptos",
                                    default="Could not import file. %s" % e)
        return state.set(status='failure', portal_status_message=message)
    # TODO: you can handle LaTeX errors here like OOoImportError above; I didn't set anything up because
    # I don't know the error conditions, but it's easy.
    # TODO: if you need the transform to supply any extra information, set meta=1, provide the data into the
    # meta dict in the transform, and read it here with 'meta.get' as in the zip section below

## Zipped CNXML
elif format in ('zip'):
    #context.manage_delObjects([i.getId() for i in context.listFolderContents(suppressHiddenFiles=1)])
    try:
        text, subobjs, meta = doTransform(context, "zip_to_folder", text, meta=1)
        if text:
            context.manage_delObjects([context.default_file,])
            context.invokeFactory('CNXML Document', context.default_file, file=text, idprefix='zip-')
        makeContent(context, subobjs)

        ignored_subdirs = ['"%s"'% x for x in meta.get('subdirs',[])]
        ignored_files =   ['"%s"'% x for x in meta.get('ignored',[])]
        if ignored_subdirs:
            list_seperator = context.translate("list_seperator", domain="rhaptos", default=", ")
            psm = context.translate("message_zip_subfolders_not_imported",
                                    {"psm":psm, "ignored_subdirs":list_seperator.join(ignored_subdirs)},
                                    domain="rhaptos", default=",".join(ignored_subdirs))
        if ignored_files:
            list_seperator = context.translate("list_seperator", domain="rhaptos", default=", ")
            psm = context.translate("message_zip_files_not_imported",
                                    {"psm":psm, "ignored_subdirs":list_seperator.join(ignored_files)},
                                    domain="rhaptos",
             default=",".join(ignored_files))

    except OOoImportError, e:
        transaction.abort()
        message = context.translate("message_could_not_import", {"errormsg":e}, domain="rhaptos",
                                    default="Could not import file. %s" % e)
        return state.set(status='failure', portal_status_message=message)

## Trusted Zipped CNXML
elif format in ('trustedzip') and context.portal_membership.getAuthenticatedMember().has_role('Manager'):
    #FIXME: manager only for now, since can bypass role requests this way.
    try:
        text, subobjs, meta = doTransform(context, "zip_to_folder", text, meta=1)
        if text:
            context.manage_delObjects([context.default_file,])
            context.invokeFactory('CNXML Document', context.default_file, file=text, idprefix='zip-')
        makeContent(context, subobjs)

        ignored_subdirs = ['"%s"'% x for x in meta.get('subdirs',[])]
        ignored_files =   ['"%s"'% x for x in meta.get('ignored',[])]
        if ignored_subdirs:
            list_seperator = context.translate("list_seperator", domain="rhaptos", default=", ")
            psm = context.translate("message_zip_subfolders_not_imported",
                                    {"psm":psm, "ignored_subdirs":list_seperator.join(ignored_subdirs)},
                                    domain="rhaptos", default=",".join(ignored_subdirs))
        if ignored_files:
            list_seperator = context.translate("list_seperator", domain="rhaptos", default=", ")
            psm = context.translate("message_zip_files_not_imported",
                                    {"psm":psm, "ignored_subdirs":list_seperator.join(ignored_files)},
                                    domain="rhaptos",
             default=",".join(ignored_files))

        # The trusted part: set the metadata
        mdata=meta['metadata']

        GoogleAnalyticsTrackingCode = mdata.get('GoogleAnalyticsTrackingCode',None)
        license=mdata.get('license',None)
        objectId = mdata['objectId']

        context.manage_changeProperties(language=mdata['language'])
        context.manage_changeProperties({'title' : mdata['title'],
                                 'abstract' : mdata['abstract'],
                                 'revised' : mdata['revised'],
                                 'created' : mdata['created'],
                                 'subject' : mdata['subject'],
                                 'keywords' : mdata.get('keywords',()),
                                 'collaborators' : mdata['collaborators'],
                                 'authors' : mdata['authors'],
                                 'maintainers' : mdata['maintainers'],
                                 'licensors' : mdata['licensors'],
                                 'pub_authors' : mdata['authors'],
                                 'pub_maintainers' : mdata['maintainers'],
                                 'pub_licensors' : mdata['licensors'],
                                 'editors' : mdata.get('editors',()),
                                 'translators' : mdata.get('translators',())
                                 })
        if objectId and objectId != 'new':
            context.setBaseObject(objectId)

        if license:
            try:
                context.setLicense(license)
            except AttributeError:
                context.manage_changeProperties(license=license)

        if GoogleAnalyticsTrackingCode:
            context.setGoogleAnalyticsTrackingCode(GoogleAnalyticsTrackingCode)

    except OOoImportError, e:
        transaction.abort()
        message = context.translate("message_could_not_import", {"errormsg":e}, domain="rhaptos",
                                    default="Could not import file. %s" % e)
        return state.set(status='failure', portal_status_message=message)


## Sword import (Zip of word doc + mets.xml) (Deprecated, unfortunately)
elif format in ('sword'):
    #context.manage_delObjects([i.getId() for i in context.listFolderContents(suppressHiddenFiles=1)])
    try:
        kwargs = {'original_file_name':importFile.filename, 'user_name':getSecurityManager().getUser().getUserName()}
        text, subobjs, meta = doTransform(context, "sword_to_folder", text, meta=1, **kwargs)
        if text:
            context.manage_delObjects([context.default_file,])
            context.invokeFactory('CNXML Document', context.default_file, file=text, idprefix='zip-')
        makeContent(context, subobjs)
        # Parse the returned mdml and set attributes up on the ModuleEditor object
        context.updateMdmlStr(meta.get('mdml'))

    except OOoImportError, e:
        transaction.abort()
        message = context.translate("message_could_not_import", {"errormsg":e}, domain="rhaptos",
                                    default="Could not import file. %s" % e)
        return state.set(status='failure', portal_status_message=message)

elif format in ('gdocs_url', 'html_url'):
    text = doTransform(context, "gdocs_to_cnxml", text)[0]
    context.getDefaultFile().setSource(text, idprefix='gd-')
    #
    #message = context.translate("message_import_type_not_supported", domain="rhaptos",
    #                            default="Sorry, but we don't support this type of import.")
    #
    #message="Sorry, but my Google Docs import does not work right now."
    #return state.set(status='failure', portal_status_message=message)	
    
elif format in ('gdocs_file', 'html_file'):
    text = doTransform(context, "gdocs_to_cnxml", text)[0]
    context.getDefaultFile().setSource(text, idprefix='gd-')    

## unknown
else:
    message = context.translate("message_import_type_not_supported", domain="rhaptos",
                                default="Sorry, but we don't support this type of import.")
    return state.set(status='failure', portal_status_message=message)

# failures above return, so when we get here, we should always have made a change
context.editMetadata()    # get the current metadata written out
context.logAction('save') # update modification date, reindex

if came_from in ('module_files', 'module_text'):
    state.set(status=came_from)

return state.set(portal_status_message=psm)

