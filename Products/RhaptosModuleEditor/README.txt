RhaptosModuleEditor

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  RhaptosModuleEditor is a content object that provides editing for
  modules (self-contained nuggets of information).  It uses
  RhaptosRepository for version control.

  Each module is a folderish object containing an XML index file (by
  default a CNXMLFile instance) as well as any additional files
  (images, etc) required by the author.

  The Product also provides a LinksDiff plugin for CMFDiffTool that
  takes differences between link objects as provided by LinkMapTool.

Future plans

  - New Edit-In-Place editing view (in development on branch)

  - Various content importers (also on branch)

  - Refactor some common Rhaptos functionality out into RhaptosContent

  - Possibly reimplement using Archetypes

  - Use DCWorkflow once RhaptosRepository supports it