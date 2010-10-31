"""
CMFDiffTool plugin for diff'ing links

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

from zope.interface import implements

from Globals import InitializeClass
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.interfaces.portal_diff import IDifference


class LinksDiff(FieldDiff):
    """Differences between lists of link dictionaries"""

    implements(IDifference)

    meta_type = "Links Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Turn list of diffs into list of items
        l = []
        for d in value:
            l.extend(d.items())
        return l

    def getAllItems(self):
        """Return unique list of items found in oldValue
	   and newValue. The dictionary key 'tag' specifies
	   whether the item has been inserted (i), deleted 
	   (d), or stayed unchanged (u)."""

        rv = []
        
        # check for deleted items
        for i in self.oldValue:
            if i not in self.newValue:
	        i['tag'] = 'd'
            else:
                i['tag'] = 'u'
	    rv.append(i)
        
        # check for inserted items
        for i in self.newValue:
            if i not in self.oldValue:
                i['tag'] = 'i'
		rv.append(i)
            else:
                i['tag'] = 'u'

        return rv 

InitializeClass(LinksDiff)
