<?xml version="1.0" encoding="gb2312"?><!-- �汾���ļ��ı���  ע�͸�ʽ--> 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><!--������ʽ��ĸ�Ԫ��-->

	<xsl:output method="html" encoding="gb2312" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/><!--�öδ����������Ĵ�����ƿ��ӻ�-->

	<xsl:template match="/"><!--templateԪ�����ڹ���ģ�壬match="/" ���������ĵ�-->
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></meta><!--ҳ���������-->
				<title>This is QT test Report</title><!--ҳ�����-->
				<style type="text/css">
				<!--����ҳ�����õ�����ʽCCS��Ĭ������£���td������ֻ������td��-->
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
					<!--<xsl:value-of select="cases/@baseline" />������@baseline-->
				</h3>
				
				<!--QT1 information start-->
				<B>QT1</B>
				<xsl:for-each select="cases/case"><!--��ʾQT�����ߵĿ�ʼʱ��ͽ���ʱ��start-->
					<xsl:if test="@name='QT1_Start_End_Time'">
                            <xsl:if test="boolean(FSMFFZFFDM8)">
                                    <li>8Pipe on FZFF Duration: <xsl:value-of select="FSMFFZFFDM8/@start" /> ~ <xsl:value-of select="FSMFFZFFDM8/@end" /></li>
                            </xsl:if>
							<xsl:if test="boolean(FSIHFZHM8)">
									<li>8Pipe on FSIH FZHM Duration: <xsl:value-of select="FSIHFZHM8/@start" /> ~ <xsl:value-of select="FSIHFZHM8/@end" /></li>
							</xsl:if>
					</xsl:if>
				</xsl:for-each><!--��ʾQT�����ߵĿ�ʼʱ��ͽ���ʱ��End-->
				
				<table cellpadding="0" cellspacing="0" border="1" bordercolor="black"
					style="border-collapse: collapse;" rules="all">
				<!--�����ⲿ��-->	
					<tr>
						<td class="name">
							<B>Case Name</B>
						</td>
						
						<td colspan="2"><!--��td�ֳ����У�tr��start-->
							<table cellpadding="0" cellspacing="0" border="1"
                                bordercolor="black" style="border-collapse: collapse;" width="201px"
                                height="100%" frame="void">
                                <tr><!--��һ�в��Ի�������start-->
                                    <td colspan="2" align='center' class="hardware">
                                        <xsl:element name="a">
										<!--�����ӵ�<B>��ʾ����</B>-->
                                        <xsl:attribute name="href">http://10.140.90.25/Trunk/<xsl:value-of select="cases/@baseline" />/8FSMFFZFFDM/</xsl:attribute>
                                        <xsl:attribute name="target">_top</xsl:attribute>
                                        <B>FSMr3-DM FZFF<br/>8Pipe 1Cell</B>
                                        </xsl:element>
                                    </td>
                                </tr><!--��һ�в��Ի�������End-->
								
                                <tr>
                                    <td>Result</td>
                                    <td>ExecTime</td>
                                </tr>
                            </table>
						</td><!--��td�ֳ����У�tr��End-->
					</tr>
						
					<xsl:for-each select="cases/case">
					<!--������ݲ��֣���forѭ������,���ļ�case���д�ͷ��β�ı������Ի���start-->
						<xsl:if test="@level='1'"><!--�ж��Ƿ���QT1case-->	
							<tr>
								<td><xsl:value-of select="@name" /></td>
								<xsl:choose><!--ÿһ�����Ի�����Ӧһ��choose,FSMFFZFFDM8���Ի���Start-->
								<!--<xsl:choose> Ԫ���� <xsl:when>---True �Լ� <xsl:otherwise>----FalseԪ�ؽ�ϣ��ɱ�������������-->
									<xsl:when test="boolean(FSMFFZFFDM8)">
										<xsl:choose>
											<xsl:when test="FSMFFZFFDM8/@res = '-'">
											<!--�����Խ��Ϊ��-��ʱ��������-->
												<td><xsl:value-of select="FSMFFZFFDM8/@res" /></td>
												<td><xsl:value-of select="FSMFFZFFDM8/@exectime" /></td>
											</xsl:when>
											<xsl:otherwise>
											<!--�����Խ����Ϊ��-��ʱ��ִ��otherwise-->
												<xsl:choose>
													<xsl:when test="contains(FSMFFZFFDM8/@res, '(0/')">
													<!--�����Խ��failʱ����ɫ����-->
														<td>
														<!--��һ�����ӵ�@res��-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSMFFZFFDM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='red'>
																<xsl:value-of select="FSMFFZFFDM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--�ڶ�����ʾִ��ʱ��-->
                                                    		<xsl:value-of select="FSMFFZFFDM8/@exectime" />
                                                		</td>
													</xsl:when>
													
													<xsl:otherwise>
													<!--�����Խ��Passʱ(��ǰ�涼Ϊfalseʱ)����ɫ����-->
														<td>
														<!--��һ�����ӵ�@res��-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSMFFZFFDM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='green'>
																<xsl:value-of select="FSMFFZFFDM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--�ڶ�����ʾִ��ʱ��-->
                                                    		<xsl:value-of select="FSMFFZFFDM8/@exectime" />
                                                		</td>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:otherwise>
											
										</xsl:choose>
									</xsl:when>
									
									<xsl:otherwise><!--�����û��û��fail��û��pass��Ҳ�С�-��ʱ������䡰-��-->
                                        <td>-</td>
                                        <td>-</td>
                                    </xsl:otherwise>
								</xsl:choose><!--ÿһ�����Ի�����Ӧһ��choose��FSMFFZFFDM8���Ի���End-->
								
								<xsl:choose><!--ÿһ�����Ի�����Ӧһ��choose,FSIHFZHM8���Ի���Start-->
								<!--<xsl:choose> Ԫ���� <xsl:when>---True �Լ� <xsl:otherwise>----FalseԪ�ؽ�ϣ��ɱ�������������-->
									<xsl:when test="boolean(FSIHFZHM8)">
										<xsl:choose>
											<xsl:when test="FSIHFZHM8/@res = '-'">
											<!--�����Խ��Ϊ��-��ʱ��������-->
												<td><xsl:value-of select="FSIHFZHM8/@res" /></td>
												<td><xsl:value-of select="FSIHFZHM8/@exectime" /></td>
											</xsl:when>
											<xsl:otherwise>
											<!--�����Խ����Ϊ��-��ʱ��ִ��otherwise-->
												<xsl:choose>
													<xsl:when test="contains(FSIHFZHM8/@res, '(0/')">
													<!--�����Խ��failʱ����ɫ����-->
														<td>
														<!--��һ�����ӵ�@res��-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSIHFZHM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='red'>
																<xsl:value-of select="FSIHFZHM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--�ڶ�����ʾִ��ʱ��-->
                                                    		<xsl:value-of select="FSIHFZHM8/@exectime" />
                                                		</td>
													</xsl:when>
													
													<xsl:otherwise>
													<!--�����Խ��Passʱ(��ǰ�涼Ϊfalseʱ)����ɫ����-->
														<td>
														<!--��һ�����ӵ�@res��-->
															<xsl:element name="a">
															<xsl:attribute name="href"><xsl:value-of select="FSIHFZHM8/@resulturl" /></xsl:attribute>
															<xsl:attribute name="target">_top</xsl:attribute>
															<font color='green'>
																<xsl:value-of select="FSIHFZHM8/@res" />
															</font>
															</xsl:element>
                                                		</td>
														<td><!--�ڶ�����ʾִ��ʱ��-->
                                                    		<xsl:value-of select="FSIHFZHM8/@exectime" />
                                                		</td>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:otherwise>
											
										</xsl:choose>
									</xsl:when>
									
									<xsl:otherwise><!--�����û��û��fail��û��pass��Ҳ�С�-��ʱ������䡰-��-->
                                        <td>-</td>
                                        <td>-</td>
                                    </xsl:otherwise>
								</xsl:choose><!--ÿһ�����Ի�����Ӧһ��choose��FSIHFZHM8���Ի���End-->
							
							</tr>
						</xsl:if>
					</xsl:for-each><!--�������Ի���End-->
				
				</table>
				<!--QT1 informaion End-->
				
				<!--QT2 informaion Start-->
				<B>QT2</B>
				<xsl:for-each select="cases/case"><!--��ʾQT�����ߵĿ�ʼʱ��ͽ���ʱ��start-->
					<xsl:if test="boolean(FSMFFZFFDM8)">
						<li><!--QT2 ÿ�����Ի���ʱ�� Start-->
							8Pipe on FZFF Duration: <xsl:value-of select="FSMFFZFFDM8/@start" /> ~ <xsl:value-of select="FSMFFZFFDM8/@end" />
						</li><!--QT2 ÿ�����Ի���ʱ�� End-->
                    </xsl:if>
					
					<xsl:if test="boolean(FSIHFZHM8)">
						<li>
							8Pipe on FSIH FZHM Duration: <xsl:value-of select="FSIHFZHM8/@start" /> ~ <xsl:value-of select="FSIHFZHM8/@end" />
						</li>
					</xsl:if>	
				</xsl:for-each><!--��ʾQT�����ߵĿ�ʼʱ��ͽ���ʱ��End-->
				
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