## Script (Python) "diff"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Display differences from the published module

cs = context.computeChanges()
cs.manage_changeProperties(title="Changes to: %s" % context.title)
return cs()
