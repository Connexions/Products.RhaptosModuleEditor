## Script (Python) "handleEipRequest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
action = context.REQUEST.get('action',None)
if not action:
    raise 'Bad Request', 'Action not specified.'

xpath = context.REQUEST.get('xpath',None)
if xpath:
    del context.REQUEST.form['xpath']
position = context.REQUEST.get('position',None)
content = context.REQUEST.get('content',None)

marker = {}
result = marker
newxpath = ''
f = context.getDefaultFile()
try:
    if action=='add' and xpath and position and content:
        if position == 'before':
            newxpath = f.xpathInsertTree(xpath, content, idprefix="eip-")
        else:
            newxpath = f.xpathAppendTree(xpath, content, idprefix="eip-")
    elif action=='update':
        newxpath = f.xpathReplaceTree(xpath, content, idprefix="eip-")
    elif action=='delete' and xpath:
        result = f.xpathDeleteTree(xpath)
    context.logAction('save')

# Bad, bad, bad.  We should have it raise an XMLError or some such thing...
except Exception, e:
    return e

if result is marker:
    contentinplace = f.xpathGetTree(newxpath, namespaces=True)  # because after save we have ids auto-generated
    
    result = context.eip_transform(contentinplace)
    if context.REQUEST.RESPONSE.status in ('Bad Request', 400):
        import transaction
        transaction.abort()
        return result

context.REQUEST.RESPONSE.setHeader('Content-Type', 'application/xhtml+xml; charset=utf-8')

return result