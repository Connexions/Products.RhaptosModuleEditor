## event handling: Zope 3-style event management
from Products.CMFCore.utils import getToolByName

def moduleContentsModified(obj, evt):
    """When module contents are updated, tell the containing Module it is modified.
    Be careful to check if what changed was in a Module, as Files, etc, can live outside
    a module.
    """
    factorytool = getToolByName(obj, 'portal_factory')
    nro = getattr(obj, 'nearestRhaptosObject', None)
    if nro and not factorytool.isTemporary(obj):
        mod = nro()
        if mod.state not in ('published') and not getattr(mod, 'batchAdd', None):
            # don't update in mass situations, like checkout/discard, or import (batchAdd set by CNXMLTransforms)
            mod.logAction('save')        # update modification date, reindex
