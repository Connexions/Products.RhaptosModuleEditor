# -*- coding: utf-8 -*-
"""Various utility/helper functions used by the ModuleEditor"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import pkg_resources
from lxml import etree
from rhaptos.cnxmlutils.xml2xhtml import MODULE_BODY_XPATH


def _make_xsl(filename):
    """ Helper that creates a XSLT stylesheet """
    package = 'rhaptos.cnxmlutils'
    sub_package = 'xsl'

    if package != '':
        pkg = package + '.' + sub_package
        path = pkg_resources.resource_filename(pkg, filename)
        xml = etree.parse(path)
        return etree.XSLT(xml)

def cnxml_to_html(cnxml_source):
    """Transform the CNXML source to HTML"""
    source = StringIO(cnxml_source)
    xml = etree.parse(source)
    # Run the CNXML to HTML transform
    xslt = _make_xsl('cnxml-to-html5.xsl')
    content = xslt(xml)
    content = MODULE_BODY_XPATH(content)
    return etree.tostring(content[0])
