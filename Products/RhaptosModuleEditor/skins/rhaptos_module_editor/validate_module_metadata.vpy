## Script (Python) "validate_module_metadata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=title='', keywords=[], abstract='', GoogleAnalyticsTrackingCode
##title=Validates module metadata

from Products.CNXMLDocument.XMLService import validate
#from Products.CNXMLDocument import XMLService    # by itself causes permission problems on validate until
                                                  # first import of Products.CNXMLDocument.XMLService!
from Products.CNXMLDocument.CNXMLFile import autoIds

# title presence
if not title:
    errormsg = context.translate("message_this_field_required", domain="rhaptos", default="This field is required.")
    state.setError('title', errormsg)
    
if title == '(Untitled)':
    errormsg = context.translate("message_must_enter_valid_title", domain="rhaptos", default="You must enter a valid title")
    state.setError('title', errormsg)

# validate CNXML pieces
#wrappedabstract = """<md:abstract xmlns="http://cnx.rice.edu/cnxml"
#                           xmlns:bib="http://bibtexml.sf.net/"
#                           xmlns:m="http://www.w3.org/1998/Math/MathML"
#                           xmlns:md="http://cnx.rice.edu/mdml/0.4"
#                           xmlns:q="http://cnx.rice.edu/qml/1.0">%s</md:abstract>""" % abstract
#wrappedabstract = autoIds(wrappedabstract, force=True)
#results = validate(wrappedabstract)
#if results:
#    state.setError('abstract', context.translate("message_abstract_invalid", domain="rhaptos",
#                                                  default="Summary contains invalid CNXML."))
#    state.setError('abstractmsg', results)

existsGoogleAnalyticsTrackingCode = GoogleAnalyticsTrackingCode is not None and len(GoogleAnalyticsTrackingCode) > 0

isValidGoogleAnalyticsTrackingCode = existsGoogleAnalyticsTrackingCode and len(GoogleAnalyticsTrackingCode.split('-')) == 3 and GoogleAnalyticsTrackingCode.split('-')[0] == 'UA' and GoogleAnalyticsTrackingCode.split('-')[1].isdigit() and GoogleAnalyticsTrackingCode.split('-')[2].isdigit()

if existsGoogleAnalyticsTrackingCode and not isValidGoogleAnalyticsTrackingCode:
    errormsg = context.translate("message_must_enter_valid_google_analytics_tracking_code", domain="rhaptos", default="You must enter a valid Google Analytics Tracking Code.")
    state.setError('GoogleAnalyticsTrackingCode', errormsg)

if state.getErrors():
    msg = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=msg)
else:
    return state.set()
