## Script (Python) "validate_module_import"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=validates import of module contents

validator = context.portal_form.createForm()
errors = validator.validate(context.REQUEST)

filename=getattr(context.REQUEST['importFile'], 'filename', None)

#raise "BadRequest", 'Filename is %s' % filename
if not filename:
    errormsg = context.translate("message_must_upload_file", domain="rhaptos", default="You must upload a file")
    errors['file']=errormsg

if errors:
    psm = context.translate("message_must_select_file_to_upload", domain="rhaptos", default="You must select a file to upload.")
    return ('failure', errors, {'portal_status_message':psm})
return ('success', errors, {})
