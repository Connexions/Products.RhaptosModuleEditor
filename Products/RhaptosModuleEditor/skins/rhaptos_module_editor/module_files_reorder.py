##parameters=seq, b_size=100,suppressHiddenFiles=0

content=[]

for x in seq:
  id = x.getId
  if id == context.getDefaultFile().getId(): #x.portal_type == "CNXML Document":
      content.insert(0,x)
  elif not (suppressHiddenFiles and (id[:1]=='.' or id == 'CVS')):
      content.append(x)

from Products.CMFPlone import Batch
b_start = context.REQUEST.get('b_start', 0)
batch = Batch(content, b_size, int(b_start), orphan=0)
return batch
