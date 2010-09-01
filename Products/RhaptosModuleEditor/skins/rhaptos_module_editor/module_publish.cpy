## atom.cpy : process sword requests
##parameters=

request = context.REQUEST
response = context.REQUEST.RESPONSE 

#context.manage_changeProperties({'license': license})
current_license = context.getProperty('license') or ''
context.plone_log('current license is:\n%s' % current_license)

default_license = context.getDefaultLicense()
context.plone_log('default license is:\n%s' % default_license)

needLicenseAgreement = ( current_license != default_license )
if needLicenseAgreement:
    needNewLicenseAgreement = ( current_license != '' )
    if needNewLicenseAgreement:
        # the default license has changed between the start of editing and publish ...
        license_data = context.getLicenseData(current_license)
        return state.set(status='license', portal_status_message="The publication license agreement has changed since you last agreed to it.  The previous license on this content was the Creative Commons %(name)s License, Version %(version)s. You will need to accept the new license prior to publishing." % license_data)
    else:
        # the license has never been agreed to ...
        return state.set(status='license')
else:
    return state.set(status='success')
