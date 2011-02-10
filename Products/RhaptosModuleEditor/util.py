"""Utils for RhaptosModuleEditor, mostly for import.

Author: J Cameron Cooper (jccooper@gmail.com)

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

import urllib2
from StringIO import StringIO

def fetchRemoteFile(url):
    """Given a URL, return its contents as a file-like object.
    Useful to be called from a Python Script where urllib2 is illegal.
    """
    response = urllib2.urlopen(url)
    sio = StringIO(response.read())
    sio.filename = url[url.rfind("/")+1:]  # we fake a file upload obj
    return sio
