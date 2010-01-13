<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:param name="tagname" value="0" />

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="/">
    <html>
      <head>
	<title>Help on using the &lt;<xsl:value-of 
	  select="source/body/tag[@name=$tagname]/@name" />&gt; 
	  tag
	</title>
	<link rel="stylesheet" type="text/css" href="../stylesheets/plone/document.css" />
	<link rel="stylesheet" type="text/css"  href="./eip-help.css" />
	<script type="text/javascript" src="../js/exercise.js"><xsl:text> </xsl:text></script>
      </head>
      <body>
	<div class="close-this-window">
	  <a href="javascript:window.close()">Close this window</a>
	</div>
        <div id="cnx_module_header">
          <h1 id="cnx_eip_help_title">Using the 
            &lt;<xsl:value-of 
	    select="source/body/tag[@name=$tagname]/@name" />&gt; tag
          </h1>
        </div>
	<div class="reference-link">
	  <div><a href="help">Introduction to CNXML tags</a></div>
	  <div><a href="terminology">Understanding XML terminology</a></div>
	  <div><a href="tags">Complete CNXML tag list</a></div>
	</div>
	<xsl:apply-templates select="source/body/tag[@name=$tagname]" />
	<div class="close-this-window">
	  <a href="javascript:window.close()">Close this window</a>
	</div>
        <xsl:comment> Google Analytics tracking. Only for CNX. This will need to edited out for Rhaptos installs. </xsl:comment>
        <script type="text/javascript">
          var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
          document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
        </script>
        <script type="text/javascript">
          try {
            var benchmarkTracker = _gat._getTracker("UA-7903479-1");
            benchmarkTracker._setDomainName('cnx.org');
            benchmarkTracker._trackPageview();                
            var overallTracker = _gat._getTracker("UA-5033010-1");
            overallTracker._setDomainName('cnx.org');
            overallTracker._trackPageview();
          } catch(err) {}
        </script>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="tag">
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="description">
    <h2 class="para-header">
      <strong class="name">Description</strong>
    </h2>
    <div class="para" id="cnx_eip_help_description">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="nameoftag">
    <code class="codeline"><xsl:apply-templates /></code>
  </xsl:template>

  <xsl:template match="exampleexample">
    <div class="example" id="cnx_eip_help_example">
      <h2 class="example-header">
        <span class="cnx_label">Example</span>
      </h2>
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="input">
    <p class="para">
      <xsl:if test="../input and ../output">This CNXML:</xsl:if>
    </p>
    <div class="code">
      <pre class="codeblock">
        <code>
          <xsl:apply-templates />
        </code>
      </pre>
    </div>
  </xsl:template>

  <xsl:template match="output">
    <p class="para">
      <xsl:if test="../input and ../output">Results in this display:</xsl:if>
    </p>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="attributes">
    <div id="cnx_eip_help_attributes_list" class="list">
      <h2 class="list-header">
        <strong class="title">Attributes</strong>
        <span class="whats-this">(<a href="terminology#cnx_eip_help_define_attribute_section">what's this?</a>)</span>
      </h2>
      <ul class="bullet">
        <xsl:apply-templates select="attribute|linkingattributes" />
        <li class="item">
          <b>id</b>
          <xsl:text> </xsl:text>
          <i>(<xsl:value-of select="@id" />)</i>: 
          A unique identifier, whose value must begin with a letter and contain only letters, 
          numbers, hyphens, underscores, colons, and/or periods (no spaces).
        </li>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="attribute">
    <li class="item">
      <b><xsl:value-of select="@name" /></b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="@required" />)</i>: 
      <xsl:apply-templates />
    </li>
  </xsl:template>

  <xsl:template match="linkingattributes">
    <xsl:choose>
      <xsl:when test="ancestor::tag[@name='link']">
        <xsl:call-template name="linkingattributeshelper">
          <xsl:with-param name="tag">link</xsl:with-param>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <li>
          <i>Optional linking attributes (<xsl:apply-templates select="linkingattributesdescription"/>):</i>
          <div id="cnx_eip_help_linking_attributes_list" class="list">
            <ul class="bullet">
              <xsl:call-template name="linkingattributeshelper">
                <xsl:with-param name="tag">other</xsl:with-param>
              </xsl:call-template>
            </ul>
          </div>
        </li>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="linkingattributeshelper">
    <xsl:param name="tag">other</xsl:param>
    <xsl:variable name="required">
      <xsl:choose>
        <xsl:when test="$tag='link'">conditional</xsl:when>
        <xsl:otherwise>optional</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <li class="item">
      <b>url</b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="$required" />)</i>: 
      A Web path being linked to.  Verify that the location is stable and will not change.  You cannot use the "url" attribute in 
      combination with the "document", "target-id", "resource", or "version" attributes.
    </li>
    <li class="item">
      <b>document</b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="$required" />)</i>: 
      The id of the module or collection being linked to (default is the present module).
    </li>
    <li class="item">
      <b>target-id</b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="$required" />)</i>: 
      The id of an element in a module or collection, such as a section or an image (default is the root element of the target module 
      or collection).  Can refer to an element in the present module or, alternately, an element on a seperate module if the 
      "document" attribute has been specified.  You cannot use the "target-id" attribute in combination with the "resource" attribute.
    </li>
    <li class="item">
      <b>resource</b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="$required" />)</i>: 
      The name of a resource, such as a supplemental PDF or text document (default is nothing).  The resource must be a part of the 
      present module or, if the "document" attribute has been specified, must be part of the target module.
    </li>
    <li class="item">
      <b>version</b>
      <xsl:text> </xsl:text>
      <i>(<xsl:value-of select="$required" />)</i>: 
      The version of the module or collection being linked to (default is the latest version of the module or collection).  Can refer 
      to the module you are on or, alternately, a seperate module or collection if the "document" attribute has been specified.
    </li>
    <li class="item">
      <b>window</b>
      <xsl:text> </xsl:text>
      <i>(optional)</i>: 
      <div>
        <i>Possible values:</i>
      </div>
      <div class="list">
        <ul class="bullet">
          <li class="item">replace - The code will navigate to the reference URL in the same current window (default).</li>
          <li class="item">new - The code will be navigate to the reference URL in a new window</li>
        </ul>
      </div>
    </li>
  </xsl:template>

  <xsl:template match="values">
    <div>
      <i>Possible values:</i>
    </div>
    <div class="list">
      <ul class="bullet">
        <xsl:apply-templates />
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="value">
    <li class="item">
      <xsl:value-of select="@name" />
      <xsl:if test="node()"> - </xsl:if> 
      <xsl:apply-templates />
    </li>
  </xsl:template>

  <xsl:template match="tagsets" />

  <xsl:template match="children|parents">
    <h2 class="para-header">
      <xsl:choose>
	<xsl:when test="self::children">
	  <strong class="title">Children</strong>
	  <span class="whats-this">(<a href="terminology#cnx_eip_help_define_child_parent_section">what's this?</a>)</span>
	</xsl:when>
	<xsl:when test="self::parents">
	  <span class="title">Parents</span>
	  <span class="whats-this">(<a href="terminology#cnx_eip_help_define_child_parent_section">what's this?</a>)</span>
	</xsl:when>
      </xsl:choose>
    </h2>
    <div class="para" id="cnx_eip_help_{name()}">
      <xsl:for-each select="tagref">
	<xsl:choose>
	  <xsl:when test="contains(node(),'document')">
	    <xsl:value-of select="node()" />
	  </xsl:when>
	  <xsl:otherwise>
	    <a class="cnxn" href="{node()}">
	      <xsl:value-of select="node()" />
	    </a>
	  </xsl:otherwise>
	</xsl:choose>
	<xsl:if test="@note"> (<xsl:value-of select="@note" />)</xsl:if>
	<xsl:if test="position()!=last()">, </xsl:if>
      </xsl:for-each>
      <xsl:if test="tagsetref and tagref">, </xsl:if>
      <xsl:for-each select="tagsetref">
	<xsl:apply-templates select="." />
	<xsl:if test="position()!=last()">, </xsl:if>
      </xsl:for-each>
      <xsl:if test="text"> <!-- Unicode text -->
	<xsl:text>, Unicode text</xsl:text>
      </xsl:if>
      <xsl:apply-templates select="note" />
    </div>
  </xsl:template>

  <xsl:template match="tagsetref">
    <xsl:variable name="tagsetname" select="@name" />
    <xsl:for-each select="//tagset[@name=$tagsetname]/tag">
      <a class="cnxn" href="{node()}">
	<xsl:value-of select="node()" />
      </a>
      <xsl:if test="position()!=last()">, </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="link[not(@src)]">
    <a href="{node()}" class="cnxn">
      <xsl:value-of select="node()"/>
    </a>
  </xsl:template>

  <xsl:template match="link[@src]">
    <a href="{@src}" target="_blank" class="link">
      <xsl:value-of select="node()" />
    </a>
  </xsl:template>

  <xsl:template match="note|linkingattributesdescription">
    <xsl:apply-templates />
  </xsl:template>

</xsl:stylesheet>

