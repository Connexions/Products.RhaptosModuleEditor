## Script (Python) "upgrade_cnxml"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contents=''
##title=Run CNXML upgrade on index file

context.getDefaultFile().upgrade(backupto=context, backupname='index.cnxml.pre-v06')
# context.logAction('upgrade')
# psm = context.translate("message_upgraded_06", domain="rhaptos", default="Upgraded to CNXML version 0.6.")
context.logAction('save')
psm = context.translate("message_saved", domain="rhaptos", default="Saved.")
# return state.set(portal_status_message=psm, edit_source=1)
return state.set(portal_status_message=psm)
