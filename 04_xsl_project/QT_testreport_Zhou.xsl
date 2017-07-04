<?xml version="1.0" encoding="gb2312"?><!-- 版本和文件的编码  注释格式--> 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><!--定义样式表的根元素-->

	<xsl:output method="html" encoding="gb2312" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/><!--该段代码可以让你的代码设计可视化-->

	<xsl:template match="/"><!--template元素用于构建模板，match="/" 定义整个文档-->
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></meta><!--页面标题属性-->
				<title>This is QT test Report</title><!--页面标题-->
				<style type="text/css">
				<!--定义页面所用到的样式CCS，默认情况下，用td，而且只能用于td中-->
					p {text-indent: 1cm}
					td {
					height: 20px;
					width: 100px;
					}
					td.hardware {
					width:201px;
					height:20px;
					}
					td.name {
					height:20px;
					width:
					200px;
					}
					td.name2 {
					height:20px;
					width: 200px;
					}
					a {text-decoration: none; color:black;}
				</style>
			</head>
		
			<body>
				<h3>
					ENB Baseline:<xsl:value-of select="cases/@baseline" />
					Time:<xsl:value-of select="cases/@time" />
					<!--<xsl:value-of select="cases/@baseline" />变量是@baseline-->
				</h3>
				
				<!--QT1 information start-->
				<B>QT1</B>
				<xsl:for-each select="cases/case"><!--显示QT测试线的开始时间和结束时间start-->
					<xsl:if test="@name='QT1_Start_End_Time'">
                            <xsl:if test="boolean(FSMFFZFFDM8)">
                                    <li>8Pipe on FZFF Duration: <xsl:value-of select="FSMFFZFFDM8/@start" /> ~ <xsl:value-of select="FSMFFZFFDM8/@end" /></li>
                            </xsl:if>
							<xsl:if test="boolean(FSIHFZHM8)">
									<li>8Pipe on FSIH FZHM Duration: <xsl:value-of select="FSIHFZHM8/@start" /> ~ <xsl:value-of select="FSIHFZHM8/@end" /></li>
							</xsl:if>
					</xsl:if>
				</xsl:for-each><!--显示QT测试线的开始时间和结束时间End-->
				
				<table cellpadding="0" cellspacing="0" border="1" bordercolor="black"
					style="border-collapse: collapse;" rules="all">
				<!--表格标题部分-->	
					<tr>
						<td class="name">
							<B>Case Name</B>
						</td>
						
						<td colspan="2"><!--把td分成两行（tr）start-->
							<table cellpadding="0" cellspacing="0" border="1"
                                bordercolor="black" style="border-collapse: collapse;" width="201px"
                                height="100%" frame="void">
                                <tr><!--第一行测试环境名称start-->
                                    <td colspan="2" align='center' class="hardware">
                                        <xsl:element name="a">
										<!--超链接到<B>显示名称</B>-->
                                        <xsl:attribute name="href">http://10.140.90.25/Trunk/<xsl:value-of select="cases/@baseline" />/8FSMFFZFFDM/</xsl:attribute>
                                        <xsl:attribute name="target">_top</xsl:attribute>
                                        <B>FSMr3-DM FZFF<br/>8Pipe 1Cell</B>
                                        </xsl:element>
                                    </td>
                                </tr><!--第一行测试环境名称End-->
								
                                <tr>
                                    <td>Result</td>
                                    <td>ExecTime</td>
                                </tr>
                            </table>
						</td><!--把td分成两行（tr）End-->
					</tr>
						
					<xsl:for-each select="cases/case">
					<!--表格内容部分，由for循环控制,对文件case进行从头到尾的遍历测试环境start-->
						<xsl:if test="@level='1'"><!--判断是否是QT1case-->	
							<tr>
								<td><xsl:value-of select="@name" /></td>
								<xsl:choose><!--每一个测试环境对应一个choose,FSMFFZFFDM8测试环境Start-->
								<!--<xsl:choose> 元素与 <xsl:when>---True 以及 <xsl:otherwise>----False元素结合，可表达多重条件测试-->
									<xsl:when test="boolean(FSMFFZFFDM8)">
										<xsl:choose>
											<xsl:when test="FSMFFZFFDM8/@res = '-'">
											<!--当测试结果为“-”时，？？？-->
												<td><xsl:value-of select="FSMFFZFFDM8/@res" /></td>
												<td><xsl:value-of select="FSMFFZFFDM8/@exectime" /></td>
											</xsl:when>
											<xsl:otherwise>
											<!--当测试结果不为“-”时，执行otherwise-->
												<xsl:choose>
													<xsl:when test="contains(FSMFFZFFDM8/@res, '(0/')">
													<!--当测试结果fail时，红色字体-->
														<td>
														<!--第一格超链接到@res上-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSMFFZFFDM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='red'>
																<xsl:value-of select="FSMFFZFFDM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--第二格显示执行时间-->
                                                    		<xsl:value-of select="FSMFFZFFDM8/@exectime" />
                                                		</td>
													</xsl:when>
													
													<xsl:otherwise>
													<!--当测试结果Pass时(即前面都为false时)，绿色字体-->
														<td>
														<!--第一格超链接到@res上-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSMFFZFFDM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='green'>
																<xsl:value-of select="FSMFFZFFDM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--第二格显示执行时间-->
                                                    		<xsl:value-of select="FSMFFZFFDM8/@exectime" />
                                                		</td>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:otherwise>
											
										</xsl:choose>
									</xsl:when>
									
									<xsl:otherwise><!--如果都没有没有fail，没有pass，也有“-”时，就填充“-”-->
                                        <td>-</td>
                                        <td>-</td>
                                    </xsl:otherwise>
								</xsl:choose><!--每一个测试环境对应一个choose，FSMFFZFFDM8测试环境End-->
								
								<xsl:choose><!--每一个测试环境对应一个choose,FSIHFZHM8测试环境Start-->
								<!--<xsl:choose> 元素与 <xsl:when>---True 以及 <xsl:otherwise>----False元素结合，可表达多重条件测试-->
									<xsl:when test="boolean(FSIHFZHM8)">
										<xsl:choose>
											<xsl:when test="FSIHFZHM8/@res = '-'">
											<!--当测试结果为“-”时，？？？-->
												<td><xsl:value-of select="FSIHFZHM8/@res" /></td>
												<td><xsl:value-of select="FSIHFZHM8/@exectime" /></td>
											</xsl:when>
											<xsl:otherwise>
											<!--当测试结果不为“-”时，执行otherwise-->
												<xsl:choose>
													<xsl:when test="contains(FSIHFZHM8/@res, '(0/')">
													<!--当测试结果fail时，红色字体-->
														<td>
														<!--第一格超链接到@res上-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSIHFZHM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='red'>
																<xsl:value-of select="FSIHFZHM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--第二格显示执行时间-->
                                                    		<xsl:value-of select="FSIHFZHM8/@exectime" />
                                                		</td>
													</xsl:when>
													
													<xsl:otherwise>
													<!--当测试结果Pass时(即前面都为false时)，绿色字体-->
														<td>
														<!--第一格超链接到@res上-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSIHFZHM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='green'>
																<xsl:value-of select="FSIHFZHM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--第二格显示执行时间-->
                                                    		<xsl:value-of select="FSIHFZHM8/@exectime" />
                                                		</td>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:otherwise>
											
										</xsl:choose>
									</xsl:when>
									
									<xsl:otherwise><!--如果都没有没有fail，没有pass，也有“-”时，就填充“-”-->
                                        <td>-</td>
                                        <td>-</td>
                                    </xsl:otherwise>
								</xsl:choose><!--每一个测试环境对应一个choose，FSIHFZHM8测试环境End-->
							
							</tr>
						</xsl:if>
					</xsl:for-each><!--遍历测试环境End-->
				
				</table>
				<!--QT1 informaion End-->
				
				<!--QT2 informaion Start-->
				<B>QT2</B>
				<xsl:for-each select="cases/case"><!--显示QT测试线的开始时间和结束时间start-->
					<xsl:if test="boolean(FSMFFZFFDM8)">
						<li><!--QT2 每个测试环境时间 Start-->
							8Pipe on FZFF Duration: <xsl:value-of select="FSMFFZFFDM8/@start" /> ~ <xsl:value-of select="FSMFFZFFDM8/@end" />
						</li><!--QT2 每个测试环境时间 End-->
                    </xsl:if>
					
					<xsl:if test="boolean(FSIHFZHM8)">
						<li>
							8Pipe on FSIH FZHM Duration: <xsl:value-of select="FSIHFZHM8/@start" /> ~ <xsl:value-of select="FSIHFZHM8/@end" />
						</li>
					</xsl:if>	
				</xsl:for-each><!--显示QT测试线的开始时间和结束时间End-->
				
				<table cellpadding="0" cellspacing="0" border="1" bordercolor="black"
					style="border-collapse: collapse;" rules="all">
					...
					
				</table>
				
				<!--QT2 informaion End-->
				
				<!--all testline informaion Start-->
				<br/>
				<B>QT ENV description:</B><br/>
					1. Trunk FSMr3 2 Pipe QT1: ConfID =T111-x-52-2TX-2RX: 1 I, RRU Type: FZHA <br />
        			2. Trunk FSMr3 8 Pipe QT1: ConfID = T1-x-30-8TX-8RX: 1 L, RRU Type: FZHA; QT2: ConfID = T111-x-42-8TX-8RX: 1+1+1 L, RRU Type: FZHA <br />   
          			3. Trunk FSIH 8 Pipe QT1: ConfID = T1-L-145-8TX-8RX:1L,RRU Type: FZHA; QT2: ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZHA <br /> 
                <B></B><br/>
				<!--all testline informaion End-->
			</body>
		</html>
	
	</xsl:template>
</xsl:stylesheet>