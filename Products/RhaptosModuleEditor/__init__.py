"""
Initialize RhaptosModuleEditor Product

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

import sys
import os.path

from Globals import package_home
from AccessControl import ModuleSecurityInfo

from Products.CMFDefault import Portal
from Products.CMFCore import utils, CMFCorePermissions
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFDiffTool import CMFDiffTool

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

import ModuleEditor
import LinksDiff
import permissions

this_module = sys.modules[ __name__ ]

contentConstructors = (ModuleEditor.addModuleEditor,)
contentClasses = (ModuleEditor.ModuleEditor,)

product_globals = globals()

z_bases = utils.initializeBasesPhase1(contentClasses, this_module)

# XSL transform paths for EIP
MODULE_EIP_XSL =  os.path.join(package_home(globals()), 'www/editInPlace.xsl')
ModuleSecurityInfo('Products.RhaptosModuleEditor').declarePublic('MODULE_EIP_XSL')

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

# Allow access to transaction.abort, for import script
from AccessControl import allow_module
import transaction
allow_module('transaction')

CMFDiffTool.registerDiffType(LinksDiff.LinksDiff)

def initialize(context):
    utils.initializeBasesPhase2( z_bases, context )
    utils.ContentInit(ModuleEditor.ModuleEditor.meta_type,
                      content_types = contentClasses,
                      permission = CMFCorePermissions.AddPortalContent,
                      extra_constructors = contentConstructors).initialize(context)
    

