## Script (Python) "publishBlocked"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=versioninfo
##title= Returns false if no problems with publication, or error dict otherwise
# returned error dict 'failtype' is code for type of failure; 'faildata' addl. info if necessary

err = {'failtype':None, 'faildata':None}  # return value template

# Check moduleness and short-circuit if collection
if not context.portal_type == 'Module':
    return False

# Missing index file check
indexcnxml = versioninfo['indexcnxml']
if not indexcnxml:
    err['failtype'] = 'noindex'
    return err

# Checks to see if there's a published version of this object
pubobj = versioninfo['pubobj']
latest = versioninfo['latest']

# Superseded check
if latest:
    if context.version != latest.version:
        err['failtype'] = 'superseded'
        err['faildata'] = {'thisversion':context.version, 'pubversion':latest.version}
        return err

# Now that we know we have an index file, get its CNXML version
cnxmlvers = versioninfo['cnxmlvers']

# Not-cnxml check
if cnxmlvers == None:
    err['failtype'] = 'notcnxml'
    return err

# Load in list of messages this user has already seen and dismissed for this object
from AccessControl import getSecurityManager
cur_user = getSecurityManager().getUser().getUserName()
allmsgs = getattr(context, 'messagesDismissed', {})
if allmsgs.has_key(cur_user):
  messagesDismissed = allmsgs[cur_user]
else:
  messagesDismissed = []

# Needs-upconversion check
if cnxmlvers == '0.5':
    formednesserrors = context.wellformed()
    if not formednesserrors:  # only on Modules, but we should only be on Modules at this point
        # CNXML 0.5, upgradable
        hasDismissedMsg = 'cnxmlfive' in messagesDismissed
        if not hasDismissedMsg:
            err['failtype'] = 'cnxmlfive'
            return err
        else:
            err['failtype'] = 'cnxmlfivedismissed'
            return err
    else:
        # CNXML 0.5, not upgradable
        err['failtype'] = 'brokencnxmlfive'
        err['faildata'] = {'message':formednesserrors}
        return err

# Older-version check
if cnxmlvers < '0.5':
    err['failtype'] = 'olderversion'
    err['faildata'] = {'cnxmlversion':cnxmlvers}
    return err

# Title check; used to be in getContentOverridePage.py
title = context.Title()
if (not title) or title == '(Untitled)':
    err['failtype'] = 'notitle'
    return err

# Maintainership check
# catentry is defined above, in "superseded check", and tells us whether there's a published version or not
if pubobj:
    haspermission = context.portal_membership.checkPermission('Edit Rhaptos Object', pubobj)
else:
    # cur_user is defined above the upconversion check
    haspermission = cur_user in context.maintainers or context.portal_membership.checkPermission('Edit Rhaptos Object', context)

if not haspermission:
    err['failtype'] = 'notmaint'
    return err

# Latest license present
current_license = context.getProperty('license') or ''

if current_license == '':
    err['failtype'] = 'nolicense'
    return err
elif current_license != context.getDefaultLicense():
    err['failtype'] = 'oldlicense'
    err['faildata'] = {'current_license':current_license,'default_license':context.getDefaultLicense()}
    return err

# Default return in normal case
return False
