#!/usr/bin/python

import libxml2
import libxslt

TAG_FILE = 'tag-help.xml'
XSL_FILE = 'tag-help.xsl'

def parseDoc(filename):
    parser = libxml2.createFileParserCtxt(filename)
    parser.ctxtUseOptions(libxml2.XML_PARSE_NSCLEAN | libxml2.XML_PARSE_DTDLOAD & ~libxml2.XML_PARSE_DTDATTR)
    parser.parseDocument()
    return parser.doc()


def xpathEval(doc, xpath):
    """Evaluate a XPath expression and return the results"""
    try:
        root = doc.getRootElement()
    except libxml2.treeError, e:
        raise ValueError, "CNXMLFile does not parse"

    ctx = doc.xpathNewContext()

    ctx.xpathRegisterNs("m", "http://www.w3.org/1998/Math/MathML")

    ns = root.ns()
    if ns is not None:
        ctx.xpathRegisterNs("xhtml", ns.content)
    try:
        result = ctx.xpathEval(xpath)
    except libxml2.xpathError, e:
        ctx.xpathFreeContext()
        raise XPathError, e

    ctx.xpathFreeContext()
    return result

def _quoteParam(param):
    if type(param) == type(0):
        return "%d" % param
    else:
        return "'%s'" % param
      
def transform(doc, **params):

    # libxslt requires parameters to be quoted
    for key in params.keys():
        params[key] = _quoteParam(params[key])

    styledoc = libxml2.parseFile(XSL_FILE)
    style = libxslt.parseStylesheetDoc(styledoc)
    if not style:
        raise XSLTError, "Error parsing %s" % s
    output = style.applyStylesheet(doc, params)

    result = style.saveResultToString(output)
    style.freeStylesheet()
    
    return result

if __name__ == "__main__":

    doc = parseDoc(TAG_FILE)
    tags = xpathEval(doc, '//body/tag/@name')

    print "Found %d matches" % len(tags)
    for r in tags:
        tagname = r.content
        f = open(tagname+'.html', 'w')
        help = transform(doc, tagname=r.content)
        f.write(help)
        f.close()

    doc.freeDoc()

