## Script (Python) "updateMetadata"
##title=Edit module metadata
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=title='(Untitled)', keywords=[], abstract='',language='en', subject=[], template_uid='', license=None, GoogleAnalyticsTrackingCode='', message=None

from Products.CMFCore.utils import getToolByName

# Save metadata as object properties
title = title.strip()
abstract = abstract.strip()
keywords = [w.strip() for w in keywords if w.strip()]
GoogleAnalyticsTrackingCode = GoogleAnalyticsTrackingCode.strip()

# Uniqify and remove empty items from list
keywords = filter(None, dict(map(None,keywords,[])).keys())
keywords.sort(lambda x,y: cmp(x.lower(),y.lower()))

context.manage_changeProperties(language=language)
context.manage_changeProperties({'title' : title,
                                 'abstract' : abstract,
                                 'keywords' : keywords,
                                 'revised' : DateTime(),
                                 'subject' : subject
                                 })

if license:
    try:
        context.setLicense(license)
    except AttributeError:
        context.manage_changeProperties(license=license)

if GoogleAnalyticsTrackingCode:
    context.setGoogleAnalyticsTrackingCode(GoogleAnalyticsTrackingCode)

if message:
    context.setMessage(message)

context.editMetadata()

if template_uid:
    rc = getToolByName(context, 'reference_catalog')
    template = rc.lookupObject(template_uid)
    context.getDefaultFile().manage_upload(template.getBody())

context.logAction('save', message)

psm = context.translate("message_metadata_updated", domain="rhaptos", default="Metadata updated.")
return state.set(portal_status_message=psm)

