# -*- coding: utf-8 -*-
"""Various utility/helper functions used by the ModuleEditor"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from lxml import etree
from rhaptos.cnxmlutils.xml2xhtml import MODULE_BODY_XPATH
from rhaptos.cnxmlutils.xml2xhtml import makeXsl


def cnxml_to_html(cnxml_source):
    """Transform the CNXML source to HTML"""
    source = StringIO(cnxml_source)
    xml = etree.parse(source)
    # Run the CNXML to HTML transform
    xslt = makeXsl('cnxml2xhtml.xsl')
    content = xslt(xml)
    content = MODULE_BODY_XPATH(content)
    return etree.tostring(content[0])
