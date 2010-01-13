## Script (Python) "dismiss_blockmsg"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contents=''
##title= Put the user in messagesDismissed because they're postponing the CNXML upgrade

from AccessControl import getSecurityManager
cur_user = getSecurityManager().getUser().getUserName()

if not hasattr(context, 'messagesDismissed'):
  context.manage_addProperty('messagesDismissed', {cur_user: ['cnxmlfive']}, 'dict')
else:
  dismissed = context.messagesDismissed
  seenlist = dismissed.has_key(cur_user) and dismissed[cur_user] or []
  if cur_user not in seenlist:
    seenlist.append(cur_user)
  dismissed[cur_user] = seenlist
  context.manage_changeProperties({'messagesDismissed': dismissed})

psm = 'CNXML 0.7 upgrade postponed.'
return state.set(portal_status_message=psm)
