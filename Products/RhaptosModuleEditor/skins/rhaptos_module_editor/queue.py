## Script (Python) "queue"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format
##title=Enqueue module exports

qtool = getToolByName(self, 'queue_tool')
repos = getToolByName(self, 'content')
oid = context.objectId or context.getId().replace('.','-')
ver = context.version
repos = repos.absolute_url()

added = []

#rebuildCollectionXml = ( kw.get('collxml') is not None )
#rebuildCompleteZip   = ( kw.get('colcomplete') is not None )
#rebuildCollectionPDF = ( kw.get('colprint') is not None )
#if not rebuildCollectionXml and not rebuildCompleteZip and not rebuildCollectionPDF:
#    rebuildCollectionXml = rebuildCompleteZip = rebuildCollectionPDF = True
script_location = 'SCRIPTSDIR' in os.environ and os.environ['SCRIPTSDIR'] or '.'


key = "modexport_%s" % oid
dictRequest = {'id':oid, 'version':ver, 'repository':repos}
qtool.add(key, dictRequest, "%s/create_and_store_pub_module_export.zctl" % script_location)
added.append('modexport')

return "Enqueued: %s" % added or 'nothing'