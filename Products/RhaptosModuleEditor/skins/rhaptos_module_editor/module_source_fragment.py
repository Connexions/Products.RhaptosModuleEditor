## Script (Python) "handleEipRequest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=xpath=None
##title=
##

#import zLOG

f = context.getDefaultFile()

#zLOG.LOG("get-cnxml-source-from-xpath", zLOG.INFO, "xpath is : " + xpath)

try:
    if xpath != None:
        source = f.xpathGetTree(xpath)
    else:
        # defensive programming; should never get here
        source = f.getSource()
    #zLOG.LOG("get-cnxml-source-from-xpath", zLOG.INFO, "source fragment is : " + source)

    context.REQUEST.RESPONSE.setHeader('Content-Type', 'application/xhtml+xml; charset=utf-8') 
    context.REQUEST.RESPONSE.setHeader('Pragma','no-cache')
    context.REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0')
    context.REQUEST.RESPONSE.setHeader('Expires', 'Mon, 26, Jul 1997 05:00:00 GMT')

    return source
except Exception, e:
    # Bad, bad, bad.  We should have it raise an XMLError or some such thing...
    return e

