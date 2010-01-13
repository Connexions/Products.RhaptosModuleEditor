## Script (Python) "searchPeople"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=search
##title= Search for members not associated with the module

# Exclude both current and pending users on this content
exclude_names = context.getCollaborators()
exclude_names.extend(context.getPendingCollaborations().keys())

# We assume these are all catalog brains so getUserName is an
# attribute not a method
members = context.portal_membership.searchForMembers(name=search)
return [m for m in members if m.status != "Pending" and m.getUserName not in exclude_names]

