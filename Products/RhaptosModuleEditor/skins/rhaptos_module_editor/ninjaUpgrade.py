## Script (Python) "ninjaUpgrade"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=versioninfo
##title=Upgrade CNXML without user action
# used for 0.6 -> 0.7. Takes version info dict from rmeVersionInfo script.

from Products.RhaptosSite import RhaptosMessageFactory as r_

cnxmlvers = versioninfo['cnxmlvers']
indexcnxml = versioninfo['indexcnxml']

# Auto-upgrade for 0.6 to 0.7
if cnxmlvers == '0.6':
    if indexcnxml.upgrade(backupto=context, backupname='index.cnxml.pre-v07'):
        msg = u"""The CNXML in this module has automatically been updated to 0.7, which involves minimal changes.
        See the <a href="/help">CNXML 0.7 page</a> for details."""
        msg = r_('message_06_upgrade', msg)
        #context.plone_utils.addPortalMessage(msg)
        return ('0.6','0.7', msg)
    else:
        msg = u"""An attempt to automatically update the CNXML in this module  to 0.7 failed. Please correct any problems below."""
        msg = r_('message_06_upgrade_failed', msg)
        return False
