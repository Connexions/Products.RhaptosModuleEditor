## Script (Python) "htmlEditorInfo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Information about the html editor view.
# Used by other editor views to determine if the html editor
# can be used.

from Products.RhaptosSite import RhaptosMessageFactory as r_

# return values...
info = {'enabled': False,
        'why': None,
        }

# Upgrade the module editor object
context.upgrade()

if context.getDefaultFile(format='html') is not None:
    info['enabled'] = True

return info
