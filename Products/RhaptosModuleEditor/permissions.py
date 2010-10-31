"""
Permissions for RhaptosModuleEditor Product

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.permissions import setDefaultRoles
# We put these here; refactoring.

# Permissions
AddModuleEditor = 'Add ModuleEditor'
ChangeModuleEditor = 'Change ModuleEditor Content'

# Set up default roles for permissions
setDefaultRoles(AddModuleEditor, ('Manager', 'Owner'))
setDefaultRoles(ChangeModuleEditor, ('Manager', 'Owner','Maintainer'))

