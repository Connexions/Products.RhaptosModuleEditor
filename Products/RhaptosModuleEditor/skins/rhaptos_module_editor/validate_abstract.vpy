## Script (Python) "validate_abstract"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=abstract=''
##title=Validates CNXML-containing abstract

from Products.CNXMLDocument.XMLService import validate
#from Products.CNXMLDocument import XMLService    # by itself causes permission problems on validate until
                                                  # first import of Products.CNXMLDocument.XMLService!

# validate CNXML pieces
versioninfo = context.rmeVersionInfo()
cnxmlvers = versioninfo['cnxmlvers'] or '0.7'
wrappedabstract = """<md:abstract xmlns="http://cnx.rice.edu/cnxml"
                           xmlns:bib="http://bibtexml.sf.net/"
                           xmlns:m="http://www.w3.org/1998/Math/MathML"
                           xmlns:md="http://cnx.rice.edu/mdml"
                           xmlns:q="http://cnx.rice.edu/qml/1.0">%s</md:abstract>""" % abstract
#wrappedabstract = autoIds(wrappedabstract, force=True)
results = validate(wrappedabstract, "http://cnx.rice.edu/technology/cnxml/schema/rng/%s/cnxml-fragment.rng" % cnxmlvers)
if results:
    state.setError('abstract', context.translate("message_abstract_invalid", domain="rhaptos",
                                                 default="Summary contains invalid CNXML."))
    state.setError('abstractmsg', results)

if state.getErrors():
    msg = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=msg)
else:
    return state
