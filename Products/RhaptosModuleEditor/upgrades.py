# -*- coding: utf-8 -*-
"""
Upgrade step functions for module editor objects. The basic format of
these upgrades are as follows:

def upgrade_<current-version>_to_<next-version>(module_editor):
    '''Description of the upgrade'''
    <upgrade-logic>
    return <successful?>
"""
import logging

NEWEST = 2
logger = logging.getLogger('RhaptosModuleEditor upgrades')

_upgrades = {}


class UpgradeError(Exception):
    """Occures when the upgrade was unsuccessful. This exception captures
    information about why the upgrade was not sucessful.
    """
    def __init__(self, message, reason=None):
        Exception(self, message)
        self.reason = reason

def set_version(obj, ver):
    """Set the module editor version in the object's propertysheet."""
    setattr(obj, 'editor_version', ver)

def upgrade(module_editor):
    """Upgrade the module editor object"""
    # The editor_version property was introduced in version 1.
    current_version = getattr(module_editor, 'editor_version', 0)
    # Upgrade to the newest version.
    if current_version != NEWEST:
        for i in xrange(current_version, NEWEST):
            next_version = i + 1
            func = _upgrades[(i, next_version)]
            # An UpgradeError will be raised if there are issues.
            logger.debug("Upgrading '%s' from %s to %s" \
                             % (module_editor, i, next_version))
            func(module_editor)
            set_version(module_editor, next_version)
    return True

def upgrade_0_to_1(module_editor):
    """Upgrades the module editor to use a basic object versioning setup."""
    pass

_upgrades[(0,1,)] = upgrade_0_to_1

def upgrade_1_to_2(module_editor):
    """Upgrades the module editor object's data formatting.
    With this change, it can use the dual format (cnxml and html)
    formatting and storage.
    """
    # Run the CNXML to HTML transform

    # TODO Roll over all index.<lang>.cnxml files

    # Store the transformed content to the index.html file


_upgrades[(1,2,)] = upgrade_1_to_2
