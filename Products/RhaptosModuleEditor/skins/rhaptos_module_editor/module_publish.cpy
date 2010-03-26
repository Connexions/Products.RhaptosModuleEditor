## atom.cpy : process sword requests
##parameters=

request = context.REQUEST
response = context.REQUEST.RESPONSE 

#context.manage_changeProperties({'license': license})
current_license = context.getProperty('license') or ''
context.plone_log('current license is:\n%s' % current_license)

default_license = context.getDefaultLicense()
context.plone_log('default license is:\n%s' % default_license)

needLicenseAgreement = ( current_license != default_license)
if needLicenseAgreement:
    return state.set(status='license')
else:
    return state.set(status='success')
