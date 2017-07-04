Settings.dataServerUrl="http://" + window.location.hostname + ":3000/";
Settings.apiUrl = Settings.dataServerUrl + "api";

function Settings() {	
	this.allStages = ["Commit", "UT", "MT", "SCT", "PCI SCM", "QT1", "QT2", "CACRT1", "CACRT2"];
	this.__donutColors = ["#6b486b", "#a05d56", "#d0743c", "#ff8c00", "#ffee00", "#9848c5", "#7664c5", "#88aba6", "#98abc5", "#8a89a6", "#7b6888"];
	this.issueSCNames = [{
		"PS": ["PS_LFS", "PS_CCS", "PS_MCUHWAPI", "PS_DSPHWAPI","PS_FPGA"]
	}, {
		"BM": []
	}, {
		"BTSSM_TDD": []
	}, {
	        "CPLANE": []
	}, {
		"TDDCPRI": []
	}, {
		"DSP_COMMON": []
	}, {
		"HW": []
	}, {
		"LOM": []
	}, {
		"LTEL2": []
	}, {
		"MAC_PS_TDD": []
	},
	{
		"OAM": []
	},
	{
		"PDDB": []
	},
	{
		"PHY_RX_TDD": []
	},
	{
		"PHY_TX": []
	},
	{
		"PHY_TX_TDD": []
	},
	{
		"RFSW": []
	},
	{
		"SACK": []
	},
	{
		"SCM": []
	},
	{
		"SPEC": []
	},
	{
		"TRS": []
	},
	{
		"IT": []
	},
	{
		"LAB": []
	},
	{
		"OTHERS": []
	}];

	this.SCNames= ['tddcpri','mac_ps_tdd','phy_rx_tdd','phy_tx_tdd'];
	this.lineCount = 20;
	this.donutChartWidth = 300;
	this.donutChartHeight = 150;
	this.donutColor = d3.scale.ordinal()
		.domain(this.allStages)
		.range(this.__donutColors);


}

Settings.prototype.getInstance=function(){
	return new Settings();
};

Settings.productConfigs={
		"macrotdd":{
			"BRANCHES":["trunk"],
                        "CRT_BUILD_TYPE":["FVHZ CIT","RRMCIT","SISOCIT","PETCIT"],
			"QT_ISSUE_URL":"http://hzlinb01.china.nsn-net.net:8000/qt/issue/",
			"APIS":{
				"BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index",
				"DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=macrotdd",
                "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=macrotdd",
				"STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=macrotdd",
				"STAGE_COMMIT_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcommit",
				"STAGE_SCCI_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscci",
				"STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=macrotdd",
				"STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=macrotdd",
				"STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=macrotdd",
				"STAGE_CRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt1?product=macrotdd",
				"STAGE_CRT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt2?product=macrotdd",
				"STAGE_RRMCRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexrrmcrt1?product=macrotdd",
				"STAGE_RRMCRT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexrrmcrt2?product=macrotdd",
				"STAGE_SISOCRT_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexsisocrt?product=macrotdd",
			    "STAGE_PETCRT_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexpetcrt?product=macrotdd",
				"STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=macrotdd",
				"FEEDBACK_CYCLE": Settings.apiUrl+"/trunk_fb",
                                "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
				"TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=macrotdd",
                "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=macrotdd",
                "COMMIT_CIRCLE":Settings.apiUrl+"/commits/search/sccivisualization?product=macrotdd"
			},
			"STAGE_CONFIG":{
							"COMMIT": {
								url: "html/stages/commit.html"
							},
							"SCCI": {
								url: "html/stages/scci.html"
							},
							"SCM": {
								url: "html/stages/scm.html"
							},
							"QT1": {
								url: "html/stages/qt1.html"
							},
							"QT2": {
								url: "html/stages/qt2.html"
							},
							"CRT1": {
								url: "html/stages/crt.html?stage=crt1",
								newName: "EV</br>CRT1"
							},
							"CRT2": {
								url: "html/stages/crt.html?stage=crt2",
								newName: "EV</br>CRT2"
							},
							"RRM-CRT1": {
								url: "html/stages/crt.html?stage=rrmcrt1",
								newName: "RRM</br>CRT1"
							},
							"RRM-CRT2": {
								url: "html/stages/crt.html?stage=rrmcrt2",
								newName: "RRM</br>CRT2"
							},
							"SISO-CRT": {
								url: "html/stages/crt.html?stage=sisocrt",
								newName: "SISO</br>CRT"
							},
							"PET-CRT": {
								url: "html/stages/crt.html?stage=petcrt",
								newName: "PET</br>CIT"
							},
							"CI-PET": {
								url: "html/stages/ci-pet.html",
								rules:{
									"green":"100%",
									"yellow":"equal or above 60%,below 100%",
									"red":"below 60%",
								}
							}
			},
			"DASH_BOARDS":{
				"TRUNK_AVAILABLITY":{
					url:"html/dashboard/trunkAvailability.html",
					desc:"Trunk Availability Dashboard"
				},
                                "CRT_AVAILABLITY":{
                                        url:"html/dashboard/crtAvailability.html",
                                        desc:"CRT Availability Dashboard"
                                },
				"TOBE":{
					url:"html/dashboard/new.html",
					desc:"TO BE Dashboard"
				}
			}
		},
		"fzmtdd":{
			"QT_ISSUE_URL":"http://hzlinb01.china.nsn-net.net:8000/qt/issue/",
			"BRANCHES":["trunk","fl15a","fb14.07"],
                        "CRT_BUILD_TYPE":["FVHZ CIT", "PETCIT"],
			"APIS":{
				 "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=fzmtdd",
				 "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=fzmtdd",
				 "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=fzmtdd",
				 "STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=fzmtdd",
				 "STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=fzmtdd",
				 "DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=fzmtdd",
                                 "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=fzmtdd",
                                 "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
				 "STAGE_CRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt1?product=fzmtdd",
				 "STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=fzmtdd",
				 "TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=fzmtdd",
                 "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=fzmtdd"
			},
			"STAGE_CONFIG":{
							"COMMIT": {
								url: "html/stages/commit.html"
							},
							"SCCI": {
								url: "html/stages/scci.html"
							},
							"SCM": {
								url: "html/stages/scm.html"
							},
							"QT1": {
								url: "html/stages/qt1.html"
							},
							"QT2": {
								url: "html/stages/qt2.html"
							},
							"CRT1": {
								url: "html/stages/crt.html?stage=crt1"
							},
							"CI-PET": {
								url: "html/stages/crt.html?stage=cipet",
								newName: "PET"
							},
							"TOBE": {
								url: "html/stages/tobe.html"
							}
			},
			"DASH_BOARDS":{
				"TRUNK_AVAILABLITY":{
					url:"html/dashboard/trunkAvailability.html",
					desc:"Trunk Availability Dashboard"
				},
                                "CRT_AVAILABLITY":{
                                        url:"html/dashboard/crtAvailability.html",
                                        desc:"CRT Availability Dashboard"
                                },
				"TOBE":{
					url:"html/dashboard/new.html",
					desc:"TO BE Dashboard"
				}
			}
		},
		"fzmfdd":{
			"BRANCHES":["trunk","fl15a","fb14.07"],
		        "CRT_BUILD_TYPE":["FVHZ CIT", "PETCIT"],	
			"APIS":{
                "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=fzmfdd",
                "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=fzmfdd",
                "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=fzmfdd",
                "STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=fzmfdd",
				"STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=fzmfdd",
				"DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=fzmfdd",
                                "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=fzmfdd",
                                "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
				"STAGE_CRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt1?product=fzmfdd",
				"STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=fzmfdd",
				"TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=fzmfdd",
                "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=fzmfdd"
			},
			"STAGE_CONFIG":{
							"COMMIT": {
								url: "html/stages/commit.html"
							},
							"SCCI": {
								url: "html/stages/scci.html"
							},
							"SCM": {
								url: "html/stages/scm.html"
							},
							"QT1": {
								url: "html/stages/qt1.html"
							},
							"QT2": {
								url: "html/stages/qt2.html"
							},
							"CRT1": {
								url: "html/stages/crt.html?stage=crt1"
							},
							"CI-PET": {
								url: "html/stages/crt.html?stage=cipet",
								newName: "PET"
							},
							"TOBE": {
								url: "html/stages/tobe.html"
							}
			},
			"DASH_BOARDS":{
			    "TRUNK_AVAILABLITY":{
					url:"html/dashboard/trunkAvailability.html",
					desc:"Trunk Availability Dashboard"
				},
                                "CRT_AVAILABLITY":{
                                        url:"html/dashboard/crtAvailability.html",
                                        desc:"CRT Availability Dashboard"
                                },
				"TOBE":{
					url:"html/dashboard/new.html",
					desc:"TO BE Dashboard"
				}
			}
		},
		"fzcfdd":{
            "BRANCHES":["trunk","fl15a"],
            "CRT_BUILD_TYPE":["FVHZ CIT", "PETCIT"],
            "APIS":{
                "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=fzcfdd",
                "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=fzcfdd",
                "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=fzcfdd",
                "STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=fzcfdd",
                "STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=fzcfdd",
                "DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=fzcfdd",
                "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=fzcfdd",
                "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
                "STAGE_CRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt1?product=fzcfdd",
                "STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=fzcfdd",
                "TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=fzcfdd",
                "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=fzcfdd"
            },
            "STAGE_CONFIG":{
                            "COMMIT": {
                                        url: "html/stages/commit.html"
                            },
                            "SCCI": {
                                    url: "html/stages/scci.html"
                            },
                            "SCM": {
                                    url: "html/stages/scm.html"
                            },
                            "QT1": {
                                    url: "html/stages/qt1.html"
                            },
                            "QT2": {
                                    url: "html/stages/qt2.html"
                            },
                            "CRT1": {
                                    url: "html/stages/crt.html?stage=crt1"
                            },
                            "CI-PET": {
								url: "html/stages/crt.html?stage=cipet",
								newName: "PET"
							},
            },
            "DASH_BOARDS":{
                                "TRUNK_AVAILABLITY":{
                                        url:"html/dashboard/trunkAvailability.html",
                                        desc:"Trunk Availability Dashboard"
                                },
                                "CRT_AVAILABLITY":{
                                        url:"html/dashboard/crtAvailability.html",
                                        desc:"CRT Availability Dashboard"
                                },
                                "TOBE":{
                                        url:"html/dashboard/new.html",
                                        desc:"TO BE Dashboard"
                                }
            }
        },
                
        "fzctdd":{
        "BRANCHES":["trunk","fl15a"],
        "CRT_BUILD_TYPE":["FVHZ CIT", "PETCIT"],
        "APIS":{
                "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=fzctdd",
                "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=fzctdd",
                "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=fzctdd",
                "STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=fzctdd",
                "STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=fzctdd",
                "DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=fzctdd",
                "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=fzctdd",
                "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
                "STAGE_CRT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcrt1?product=fzctdd",
                "STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=fzctdd",
                "TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=fzctdd",
                "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=fzctdd"
            },
            "STAGE_CONFIG":{
                            "COMMIT": {
                                        url: "html/stages/commit.html"
                            },
                            "SCCI": {
                                    url: "html/stages/scci.html"
                            },
                            "SCM": {
                                    url: "html/stages/scm.html"
                            },
                            "QT1": {
                                    url: "html/stages/qt1.html"
                            },
                            "QT2": {
                                    url: "html/stages/qt2.html"
                            },
                            "CRT1": {
                                    url: "html/stages/crt.html?stage=crt1"
                            },
                            "CI-PET": {
								url: "html/stages/crt.html?stage=cipet",
								newName: "PET"
							},
            },
            "DASH_BOARDS":{
                                "TRUNK_AVAILABLITY":{
                                        url:"html/dashboard/trunkAvailability.html",
                                        desc:"Trunk Availability Dashboard"
                                },
                                "CRT_AVAILABLITY":{
                                        url:"html/dashboard/crtAvailability.html",
                                        desc:"CRT Availability Dashboard"
                                },
                                "TOBE":{
                                        url:"html/dashboard/new.html",
                                        desc:"TO BE Dashboard"
                                }
            }
        },

		"macror4tdd":{
			"BRANCHES":["trunk"],
                        "CRT_BUILD_TYPE":["SISOCRT_CPRI", "SISOCRT_OBSAI"],
			"QT_ISSUE_URL":"http://hzlinb01.china.nsn-net.net:8000/qt/issue/",
			"APIS":{
					 "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=macror4tdd",
					 "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=macror4tdd",
					 "STAGE_QT1_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=macror4tdd",
					 "STAGE_QT2_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=macror4tdd",
					 "DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=macror4tdd",
					 "DASHBOARD_CRT_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardCrt?product=macror4tdd",
					 "CRT_METRICS": Settings.apiUrl+"/crt_metrics",
					 "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=macror4tdd",
					 "STAGE_SISOCRT_CPRI_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexsisocrt_cpri?product=macror4tdd",
					 "STAGE_SISOCRT_OBSAI_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexsisocrt_obsai?product=macror4tdd",
					 
					 "STAGE_CIPET_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexcipet?product=macror4tdd",
					 "TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=macror4tdd",
					 "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=macror4tdd"
			},
			"STAGE_CONFIG":{
							"COMMIT": {
								url: "html/stages/commit.html"
							},
							"SCCI": {
								url: "html/stages/scci.html"
							},
							"SCM": {
								url: "html/stages/scm.html"
							},

							"SISOCRT_CPRI": {
								newName: 	"SISO CRT</br>(CPRI)",
								url: 	 	"html/stages/crt.html?stage=sisocrt_cpri",
								columns: 	['stage_name', 'total_count', 'pass_count', 'fail_count', 'resulturl', 'pass_rate'],
								issueUrl: 	"http://hzlinb01.china.nsn-net.net:8000/qt/issueei/"
							},
							"SISOCRT_OBSAI": {
								newName: 	"SISO CRT</br>(OBSAI)",
								url: 		"html/stages/crt.html?stage=sisocrt_obsai",
								columns: 	['stage_name', 'total_count', 'pass_count', 'fail_count', 'resulturl', 'pass_rate']
							},

							"QT1": {
								url: "html/stages/qt1.html"
							},
							"QT2": {
								url: "html/stages/qt2.html"
							},
			},
			"DASH_BOARDS":{
				"TRUNK_AVAILABLITY":{
					url:"html/dashboard/trunkAvailability.html",
					desc:"Trunk Availability Dashboard"
				},
                "CRT_AVAILABLITY":{
                        url:"html/dashboard/crtAvailability.html",
                        desc:"CRT Availability Dashboard"
                },
				"TOBE":{
					url:"html/dashboard/new.html",
					desc:"TO BE Dashboard"
				}
			}
		},
		
		"btssm":{
        "BRANCHES":["wbts17","fl00"],
        "APIS":{
                "BUILL_LIST":Settings.apiUrl + "/trunkbuilds/search/index?product=btssm",
                "STAGE_SCM_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexscm?product=btssm",
                "STAGE_OVERVIEW_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexoverview?product=btssm",
                "STAGE_SCBT_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt1?product=btssm",
                "STAGE_PROMOTION_DETAIL": Settings.apiUrl+"/trunkbuilds/search/indexqt2?product=btssm",
                "DASHBOARD_TRUNK_AVAILABLITY":Settings.apiUrl+"/trunkbuilds/search/dashboardqt?product=btssm",
                "TIMESPAMP_URL": Settings.apiUrl+"/trunkbuilds/search/timestamp?product=btssm",
                "PROMOTED_URL": Settings.apiUrl+"/trunk_scs_day/search/promoted?product=btssm"
            },
            "STAGE_CONFIG":{
                            "COMMIT": {
                                        url: "html/stages/commit.html"
                            },
                            "SCCI": {
                                    url: "html/stages/scci.html"
                            },
                            "SCM": {
                                    url: "html/stages/scm.html"
                            },
                            "SCBT": {
                                    url: "html/stages/qt1.html"
                            },
                            "MANUALCHECKING": {
                                    url: "html/stages/qt2.html",
                                    newName: "MANUAL CHECKING"
                            },
                            "PROMOTION": {
								url: "html/stages/PROMOTION",
								newName: "PROMOTION"
							},
            },
            "DASH_BOARDS":{
                                "TRUNK_AVAILABLITY":{
                                        url:"html/dashboard/trunkAvailability.html",
                                        desc:"Trunk Availability Dashboard"
                                },
                                "TOBE":{
                                        url:"html/dashboard/new.html",
                                        desc:"TO BE Dashboard"
                                }
            }
        },
};

Settings.currentProduct=localStorage.getItem("CoopProduct")||"macrotdd";
var exist=false;
_.keys(Settings.productConfigs).forEach(function(key){
	if(key===Settings.currentProduct){
		exist=true;
	}		
});
if(exist===false)
Settings.currentProduct=_.keys(Settings.productConfigs)[0];

Settings.CONSTANT_WEEKSTART=1;
if(window.moment)
moment.locale('zh-cn', {
    week : {
        dow : Settings.CONSTANT_WEEKSTART // Monday is the first day of the week
    }
});
