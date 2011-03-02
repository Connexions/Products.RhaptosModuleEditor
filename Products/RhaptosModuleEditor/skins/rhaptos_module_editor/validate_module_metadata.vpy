## Script (Python) "validate_module_metadata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=title='', keywords=[], GoogleAnalyticsTrackingCode
##title=Validates module metadata

# title presence
if not title:
    errormsg = context.translate("message_this_field_required", domain="rhaptos", default="This field is required.")
    state.setError('title', errormsg)

if title == '(Untitled)':
    errormsg = context.translate("message_must_enter_valid_title", domain="rhaptos", default="You must enter a valid title")
    state.setError('title', errormsg)

existsGoogleAnalyticsTrackingCode = GoogleAnalyticsTrackingCode is not None and len(GoogleAnalyticsTrackingCode) > 0

isValidGoogleAnalyticsTrackingCode = existsGoogleAnalyticsTrackingCode and len(GoogleAnalyticsTrackingCode.split('-')) == 3 and GoogleAnalyticsTrackingCode.split('-')[0] == 'UA' and GoogleAnalyticsTrackingCode.split('-')[1].isdigit() and GoogleAnalyticsTrackingCode.split('-')[2].isdigit()

if existsGoogleAnalyticsTrackingCode and not isValidGoogleAnalyticsTrackingCode:
    errormsg = context.translate("message_must_enter_valid_google_analytics_tracking_code", domain="rhaptos", default="You must enter a valid Google Analytics Tracking Code.")
    state.setError('GoogleAnalyticsTrackingCode', errormsg)

if state.getErrors():
    msg = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=msg)
else:
    return state
