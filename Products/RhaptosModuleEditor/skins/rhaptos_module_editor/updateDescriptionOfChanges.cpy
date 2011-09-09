## Script (Python) "updateDescriptionOfChanges"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=description_of_changes
##title= Update the description_of_changes field


psm = context.translate(
    "message_description_of_changes_updated",
    domain="rhaptos",
    default="Description of changes updated.")

context.updateProperties({'description_of_changes': description_of_changes})

return state.set(status='success', portal_status_message=psm)
