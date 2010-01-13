## Script (Python) "sendPatch"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=message=''
##title= Send a patch to the module's maintainer

obj = context.getBaseObject()
patch = context.portal_patch.createPatch(obj, context, exclude=context.excludedIds())
context.portal_workflow.doActionFor(patch, 'submit', comment=message)

psm = context.translate("message_patch_submitted", domain="rhaptos", default="Suggested edits submitted.")
return state.set(portal_status_message=psm)
