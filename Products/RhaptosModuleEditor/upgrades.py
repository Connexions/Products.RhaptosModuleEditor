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


def upgrade(module_editor):
    """Upgrade the module editor object"""
    # The editor_version property was introduced in version 1.
    current_version = getattr(module_editor, 'editor_version', 0)
    # Upgrade to the newest version.
    if current_version != NEWEST:
        for i in xrange(current_version, NEWEST):
            next_version = current_version + 1
            func = _upgrades[(current_version, next_version)]
            # An UpgradeError will be raised if there are issues.
            logger.debug("Upgrading '%s' from %s to %s" \
                             % (module_editor, current_version, next_version))
            func(module_editor)
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
    pass

_upgrades[(1,2,)] = upgrade_1_to_2
