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
    """Helper that creates a XSLT stylesheet """
    package = 'rhaptos.cnxmlutils'
    sub_package = 'xsl'

    if package != '':
        pkg = package + '.' + sub_package
        path = pkg_resources.resource_filename(pkg, filename)
        xml = etree.parse(path)
        return etree.XSLT(xml)

def _transform(xml, xsl_filename):
    """Transforms the xml using the specifiec xsl file."""
    xslt = _make_xsl(xsl_filename)
    xml = xslt(xml)
    return xml

def cnxml_to_html(cnxml_source):
    """Transform the CNXML source to HTML"""
    source = StringIO(cnxml_source)
    xml = etree.parse(source)
    # Run the CNXML to HTML transform
    xml = _transform(xml, 'cnxml-to-html5.xsl')
    xml = MODULE_BODY_XPATH(xml)
    return etree.tostring(xml[0])

def html_to_cnxml(html_source, cnxml_source):
    """Transform the HTML to CNXML. We need the original CNXML content in
    order to preserve the metadata in the CNXML document.
    """
    source = StringIO(html_source)
    xml = etree.parse(source)
    cnxml = etree.parse(StringIO(cnxml_source))
    # Run the HTML to CNXML transform on it
    xml = _transform(xml, 'html5-to-cnxml.xsl')
    # Replace the original content element with the transformed one.
    namespaces = {'c': 'http://cnx.rice.edu/cnxml'}
    xpath = etree.XPath('//c:content', namespaces=namespaces)
    replaceable_node = xpath(cnxml)[0]
    replaceable_node.getparent().replace(replaceable_node, xml.getroot())
    # Set the content into the existing cnxml source
    return etree.tostring(cnxml)
