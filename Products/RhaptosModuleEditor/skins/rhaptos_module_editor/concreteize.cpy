## Script (Python) "concreteize"
##title=Make portal_factory temp object real
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=oid=None, location=None

# if there is no id specified, keep the current one
if not oid:
    oid = context.getId()

if location:   # created without destination in mind
    # see also addObjectsToWorkspace
    wgprefix = 'GroupWorkspaces/'  # FIXME: get from groups tool
    type_name = getattr(context.aq_explicit, 'archetype_name', getattr(context.aq_explicit, 'portal_type', context.getTypeInfo().getId()))
    if location == '__home__':
        target = context.portal_membership.getHomeFolder()
    elif location.startswith(wgprefix):
        location = location[len(wgprefix):]
        target = context.portal_groups.getGroupareaFolder(location)

    context = target.restrictedTraverse('portal_factory/' + type_name + '/' + oid)

# act here like a content edit script, "concretizing" a FactoryTool-made temp object if we are one
new_context = context.portal_factory.doCreate(context, oid)

#psm = context.translate("message_has_been_created",
#                                          {"type_name":type_name}, domain="rhaptos",
#                                          default=type_name + ' has been created.')

return state.set(context=new_context)
