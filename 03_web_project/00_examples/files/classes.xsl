<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method='html' />

  <xsl:template match="/">
    <ur>
      <xsl:apply-templates select="*" />
    </ur>
  </xsl:template>

  <xsl:template match="class">
    <li>
      <em><xsl:value-of select="@name" /></em>,<em>Price: <xsl:value-of select="price" /></em>,<em>Rating: <xsl:value-of select="rating" /></em>
    </li>
  </xsl:template>

</xsl:stylesheet>
