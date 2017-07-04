'use strict';
var express = require('express');
var router = express.Router();
var _ = require('lodash');
var moment = require('moment');
var async = require('async');
var db = require('../../settings').DB;

var fault_filter = require('../../models/fault_filter');
var faultCommons = require('../../models/fault_commons');

// var SEVERITY_ALL = ["B - Major","A - Critical","C - Minor"];
var SEVERITY_L1 = ["B - Major","A - Critical"];
// var SEVERITY_L2 = ["C - Minor"];
var names = {month_tar: "Monthly Target", target_cum: "Target Cumulative",
			baseline: "Baseline", ncdr_a: "A-Critical", ncdr_b:"B-Major",
			ncdr_c:"C-Minor", ncdr_ab:"NCDR(A&B)",ncdr_cum_ab: "NCDR Cumulative",
			ncdr_cum_a: "A-Critical Cumulative", ncdr_cum_b: "B-Major Cumulative"};
var BEFOREKEY = "beforeRealBegin";
var GOAL_MAPPING_TYPE_LEN = 5;
var NCDR_ITEMS = ["pdgoal"];
var NCDR_TYPE = "new";
var SEVERITY_A = "A - Critical";
var SEVERITY_B = "B - Major";
var SEVERITY_C = "C - Minor";


/**
 * [calcuNumsOfPrs description]
 * @param  {[type]} arr       [description]
 * @param  {[type]} interval  [description]
 * @param  {[type]} timeBegin [description]
 * @return {[type]}           [[{date:BEFOREKEY, num:7},{date:"2017-02", num: 3},{date:"2017-03", num: 4}]
 */
function calcuNumsOfPrs(arr, interval, timeBegin) {
	var mydata = {};

	(arr || []).forEach(function (d) {
		if (d.createtimestamp < timeBegin) {
			if(_.has(mydata, BEFOREKEY)) {
				mydata[BEFOREKEY]["num"] += 1;
			} else {
				mydata[BEFOREKEY] = {date:BEFOREKEY, num: 1};
			}
		} else {
			var tmpTime = faultCommons.formatDate(d.createtimestamp *1000, interval);
			var tmpFind = _.has(mydata, tmpTime);
			if(tmpFind) {mydata[tmpTime]["num"] += 1;}
			else {
				mydata[tmpTime] = {date:tmpTime, num: 1};
			}
		}

	});

	return _.values(mydata);
}

function handleFilterTime(begin, end,interval) {
	var beginDate = faultCommons.formatDate(begin *1000, interval).replace(/(\d{4})(-.*)/, function (match, p1, p2) {
        var tmp = parseInt(p1) - 1;
        return tmp+p2;
    });
    var endDate = faultCommons.formatDate(end *1000, interval).replace(/(\d{4})(-.*)/, function (match, p1, p2) {
        var tmp = parseInt(p1) - 1;
        return tmp+p2;
    });
	var filterTimeList = {};
	filterTimeList["realBegin"] = begin;
	filterTimeList["realYearBegin"] = +moment(begin*1000).startOf('year').unix();
	filterTimeList["filterBegin"] = +moment(faultCommons.formatDate2TmStamp(beginDate, interval)*1000).startOf(interval).unix(); //consider same day in different year may not same in weeks
	filterTimeList["filterEnd"] = end;
	filterTimeList["ncdrBeginTimeStamp"] = begin;
	filterTimeList["ncdrEndTimeStamp"] = end;

	filterTimeList["bslBeginTimeStamp"] = +moment(faultCommons.formatDate2TmStamp(beginDate, interval)*1000).startOf(interval).unix(); //consider same day in different year may not same in weeks
	filterTimeList["bslEndTimeStamp"] = +moment(faultCommons.formatDate2TmStamp(endDate, interval)*1000).endOf(interval).unix(); //consider same day in different year may not same in weeks

	filterTimeList["bslYearBeginTimeStamp"] = +moment(filterTimeList["bslBeginTimeStamp"]*1000).startOf('year').unix();
	return filterTimeList;
}


/**
 * [uniqFaultId description]
 * @param  {[type]}   arr      [in come arr with all prs]
 * @param  {Function} callback [obj with all groupBy faultId]
 * @return {[type]: object}    [such as: {"faultId1":[{data1},{data2}],
 *                                   	  "faultId2": [{data3}]}]
 */
function uniqFaultId(arr) {
	var ncdrData = {};
	(arr||[]).forEach(function (d) {
		if(_.has(ncdrData, d.faultid)) {
			ncdrData[d.faultid].push(d);
		} else {
			ncdrData[d.faultid] = [d];
		}
	});
	return ncdrData;
}
function removeBeforeKey(arr, keyValue) {
	var removedElement = _.remove(arr, function(n) {
	  return n.date === keyValue;
	});
	if(removedElement.length) {
		return {arr:arr, beforekey_num: removedElement[0].num};
	} else {
		return {arr:arr, beforekey_num: 0};
	}
}

/**
 * [pickTargetPrs description ]
 	//filter only one issue follow rules
	1: sortBy create time, ascening
	2: get first reported Prs
 * @param  {[type]} arr  [description]
 * @param  {[type]} date [description]
 * @return {[type]: Array}      [description]: [d1, d2, d3, d4]
 */
function pickTargetPrs (arr) {
	var uniqData = [];
	_.forIn(arr, function(value, key) {
		//1: sortBy create time, ascending
		value.sort(function numAscending(index1, index2) {
		    return index1.createtimestamp - index2.createtimestamp;
		});
		// //2: get first reported Prs.
		// uniqData.push(value[0]);
		//2: found vaild Prs.
		var findItem = _.find(value, function (d) {	//returning the first element predicate
			return faultCommons.isInArray(SEVERITY_L1, d.severity);
		});
		if (findItem) {
			uniqData.push(findItem);
		} else {
			uniqData.push(value[0]);
		}
	});
	return uniqData;
}
/**
 * [splitOpenSeriesByYear description]
 * @param  {[type]} arr [description]
 * @return {[type]: Array}     [description]: [{year: "2017", yearSeries: ["2017-02", "2017-03"]}]
 */
function splitOpenSeriesByYear(arr) {
	var myObject = {};
	(arr||[]).forEach(function (d) {
		var year = d.split("-")[0] || "";
		if (_.has(myObject, year)) {
			myObject[year].yearSeries.push(d);
		} else {
			myObject[year] = {year: year, yearSeries: [d]};
		}
	});
	return _.values(myObject);
}

/**
 * [groupPrsByYear description]
 * @param  {[type]} arr [description]
 * @return {[type]:}     [{year1:{date: "year1", data:[{d1}, {d2}]}}]
 */
function groupPrsByYear(arr){
	var mytmpData = {};
	(arr||[]).forEach(function(d) {
		//group data by year.
		var tmpTime = (moment(d.createtimestamp*1000).format('YYYY'));
		var tmpFind = _.has(mytmpData, tmpTime);
		if(tmpFind) {
			mytmpData[tmpTime]["data"].push(d);
		}else {
			mytmpData[tmpTime] = {date:tmpTime, data: [d]};
		}
	});//end (arr||[]).forEach(function(d)
	return mytmpData;
}

function data2UniqFaultidByAll (arr) {
	var myData = []; // will be like [[{},{}],[{},{}]]

	//group prs with faultid by yearly
	var mytmpData = groupPrsByYear(arr);
	_.forIn(mytmpData, function(value,key) {
		var yearly_data = uniqFaultId(value.data);
		myData.push(pickTargetPrs(yearly_data));
	}); //end _.forIn(mytmpData, function(value, key)

	var backData = _(myData).flatten().valueOf(); // will be like [{},{},{},{}]

	return backData;
}


function handleCommonFilters(buBlOpts, orgCatOpts, planeGroupedOpts,
							planeOpts, level4DuOpts, componentOpts, customerOpts) {
	var tmpExpr = {"$and":[]};
	if (buBlOpts) {
		tmpExpr['$and'].push({mapping_bu_bl: {'$in': buBlOpts.split(',')}});
	}
	if (orgCatOpts) tmpExpr['$and'].push({mapping_org_cat: {'$in': orgCatOpts.split(',')}});
	if (planeGroupedOpts) tmpExpr['$and'].push({mapping_plane_grouped: {'$in': planeGroupedOpts.split(',')}});
	if (planeOpts) tmpExpr['$and'].push({mapping_plane: {'$in': planeOpts.split(',')}});
	if (level4DuOpts) tmpExpr['$and'].push({mapping_level4_du: {'$in': level4DuOpts.split(',')}});
	if (componentOpts) tmpExpr['$and'].push({mapping_component: {'$in': componentOpts.split(',')}});
	if (customerOpts) {
					tmpExpr["$and"].push({customer:{'$in': customerOpts.split(',')}});
				}
	return tmpExpr['$and'];
}

function handleTargetFilters(targetOpts, planeGroupedOpts, level4DuOpts,
							productLineOpts,productOpts, systemOpts, entityOpts,
							beginTime, endTime) {
	var targetFilterExpr = {'$and': []};
	if (targetOpts) {
		targetFilterExpr['$and'].push({goal_name: {'$in': targetOpts.split(',')}});
	}
	if (planeGroupedOpts) {
		targetFilterExpr['$and'].push({plane:{'$in':planeGroupedOpts.split(',')}});
	}
	if (level4DuOpts) {
		targetFilterExpr['$and'].push({du:{'$in':level4DuOpts.split(',')}});
	}
	if (productLineOpts) {
		targetFilterExpr['$and'].push({mapping_bl:{'$in':productLineOpts.split(',')}});
	}
	if (productOpts) {
		targetFilterExpr['$and'].push({mapping_product:{'$in':productOpts.split(',')}});
	}
	if (systemOpts) {
		targetFilterExpr['$and'].push({mapping_system_release:{'$in':systemOpts.split(',')}});
	}
	if (entityOpts) {
		targetFilterExpr['$and'].push({mapping_release:{'$in':entityOpts.split(',')}});
	}
	if (beginTime) {
		var reportDay = moment(beginTime * 1000).format('YYYY/MM/DD');
		targetFilterExpr["$and"].push({report_day:{$gte: reportDay}});
	}
	if (endTime) {
		var tmpEndDay = moment(endTime *1000).format('YYYY/MM/DD');
		targetFilterExpr["$and"].push({report_day:{$lte: tmpEndDay}});
	}
	return targetFilterExpr;
}

function getTargetData (arr,interval) {
	var finalResults = [];
	(arr||[]).forEach(function(d) {
		var eachSplit = d.type.split("_");
		var myRegExp = new RegExp(interval, "i");
		if(	eachSplit.length === GOAL_MAPPING_TYPE_LEN &&
			eachSplit[0].toLowerCase() === NCDR_TYPE &&
			myRegExp.test(eachSplit[1]) &&
			faultCommons.isStrInArrList(eachSplit[4].toLowerCase(), NCDR_ITEMS)
		) {
			finalResults.push(d);
		}
	});
	return finalResults;
}

/**
 * [calcuNumsOfTarget description]
 * @param  {[type]} arr       [description]
 * @param  {[type]} interval  [description]
 * @param  {[type]} timeBegin [description]
 * @return {[type]: Array}    [description]: like [{date:"beforeKey", num: 33},{date:"2017-03", num: 32},{}]
 */
function calcuNumsOfTarget(arr, interval, timeBegin) {
	var mydata = {};
	var timeStamp, tmpTime, tmpFind;

	(arr || []).forEach(function (d) {
		timeStamp = +moment(d.report_day, 'YYYY/MM/DD').unix();
		tmpTime = faultCommons.formatDate(timeStamp*1000, interval);
		if (timeStamp < timeBegin) {
			if(_.has(mydata, BEFOREKEY)) {
				mydata[BEFOREKEY]["num"] += d.target;
			} else {
				mydata[BEFOREKEY] = {date:BEFOREKEY, num: d.target};
			}
		} else {
			tmpFind = _.has(mydata, tmpTime);
			if(tmpFind) {mydata[tmpTime]["num"] += d.target;}
			else {
				mydata[tmpTime] = {date:tmpTime, num: d.target};
			}
		}

	});

	return _.values(mydata);
}

/**
 * [megerData2OpenSerials description]: if inData is empty, also retrun formated data.
 * @param  {[type]} inData     [description]
 * @param  {[type]} seriesData [description]
 * @return {[type]: Array}     [description] [{"year":"2017","cumulation":0,"yearData":[{"date":"2017-03","num":12},{"date":"2017-04","num":12}]}]
 */
function megerData2OpenSerials (inData, seriesData){
	var trgOpenSeries = splitOpenSeriesByYear(seriesData); //[{year: "2017", yearSeries: ["2017-02", "2017-03"]},{}]
	var trgOpenSeriesData = []; //[{year: yearly_data.year, cumulation: 0, yearData:[]},{}]

	(trgOpenSeries||[]).forEach(function (yearly_data) {
		var tmpD = {year: yearly_data.year, cumulation: 0, yearData:[]};
		(yearly_data.yearSeries ||[]).forEach(function(dd) {
			var findItem = _.find(inData, function (d) {	//returning the first element predicate
				return d["date"] === dd;
			});
			if (findItem) {
				tmpD.yearData.push(findItem);
			} else {
				tmpD.yearData.push({date:dd, num: 0});
			}
		});
		trgOpenSeriesData.push(tmpD);
	}); //end (trgOpenSeries||[]).forEach
	trgOpenSeriesData = _(trgOpenSeriesData).sortBy(function (a) { //for strong
		return a.year;
	}).flatten().valueOf();
	return trgOpenSeriesData;
}
//interval:day,week,month
router.param('interval', function (req, res, next, interval) {
    req.interval = interval.toLowerCase();
    return next();
});

router.get('/trends/get/:interval', function(req, res) {
	fault_filter.getFilters(req, function(paramsQueryEXpr) {
		var ncdrTime = {begin:paramsQueryEXpr.params.begin, end: paramsQueryEXpr.params.end};
		var interval = paramsQueryEXpr.params.interval;

		var filterTimeList = handleFilterTime(ncdrTime.begin, ncdrTime.end, interval);
		if (filterTimeList.bslYearBeginTimeStamp) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:filterTimeList.bslYearBeginTimeStamp}});}
		if (ncdrTime.end) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: ncdrTime.end}});}

		async.parallel([
			function(cb) {
				paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));
				db.collection('pr_summary')
				.find(paramsQueryEXpr.queryExpr,
					 {mapping_bl: 1, createtimestamp: 1, severity: 1, faultid: 1, _id: 1, prid: 1})
				.toArray(function(err, results) {
					if(err) {
						console.log(err);
					} else {
						var newResults = {ncdr_results_abc: [], ncdr_results_ab: [],
										ncdr_results_a: [], ncdr_results_b: [],
										ncdr_results_c: [], bsl_results_ab: []};

						(results||[]).forEach(function (d) {
							if(	d.createtimestamp < filterTimeList.bslEndTimeStamp &&
								d.createtimestamp >= filterTimeList.bslYearBeginTimeStamp) {
								if(SEVERITY_L1.indexOf(d.severity) !== -1) {newResults.bsl_results_ab.push(d);}
							}
							if (d.createtimestamp >= filterTimeList.realYearBegin &&
								d.createtimestamp < filterTimeList.ncdrEndTimeStamp) {
								newResults.ncdr_results_abc.push(d);
								switch(d.severity) {
									case SEVERITY_A:
										newResults.ncdr_results_a.push(d);
										newResults.ncdr_results_ab.push(d);
										break;
									case SEVERITY_B:
										newResults.ncdr_results_b.push(d);
										newResults.ncdr_results_ab.push(d);
										break;
									case SEVERITY_C:
										newResults.ncdr_results_c.push(d);
										break;
									default:
										console.log("ERROR: wrong data in fault_ncdr_api.js, please check /trends/get/");
								}
							}
						});

						//consiser different bl

						var uniqedResults_ab = data2UniqFaultidByAll(newResults.ncdr_results_ab);
						var uniqedResults_a = [];
						var uniqedResults_b = [];


						(uniqedResults_ab||[]).forEach(function (d) {
							if (d.createtimestamp >= filterTimeList.realYearBegin &&
								d.createtimestamp < filterTimeList.ncdrEndTimeStamp) {
								switch(d.severity) {
									case SEVERITY_A:
										uniqedResults_a.push(d);
										break;
									case SEVERITY_B:
										uniqedResults_b.push(d);
										break;
									default:
										console.log("ERROR: wrong data in fault_ncdr_api.js, please check /trends/get/ of function(cb) ncdr_a");
								}
							}
						});




						async.parallel([
							function(cb) { //ncdr_ab

								var ret = calcuNumsOfPrs(uniqedResults_ab, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_ab, num: dd.num}
											]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //ncdr_a

								// var uniqedResults_a = data2UniqFaultidByAll(newResults.ncdr_results_a);
								var ret = calcuNumsOfPrs(uniqedResults_a, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_a, num: dd.num}
											]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //ncdr_b
								// var uniqedResults_b = data2UniqFaultidByAll(newResults.ncdr_results_b);

								var ret = calcuNumsOfPrs(uniqedResults_b, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_b, num: dd.num}
											]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //ncdr_c

								var uniqedResults_abc = data2UniqFaultidByAll(newResults.ncdr_results_abc);
								var uniqedResults_c = [];
								(uniqedResults_abc||[]).forEach(function (d) {
									if (d.severity === SEVERITY_C) {
										uniqedResults_c.push(d);
									}
								});
								// var uniqedResults_c = data2UniqFaultidByAll(newResults.ncdr_results_c);

								var ret = calcuNumsOfPrs(uniqedResults_c, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_c, num: dd.num}
											]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //baseline
								var uniqedResults_bsl_ab = data2UniqFaultidByAll(newResults.bsl_results_ab);

								var ret = calcuNumsOfPrs(uniqedResults_bsl_ab, interval, filterTimeList.bslBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(filterTimeList.bslBeginTimeStamp),
																			moment.unix(filterTimeList.bslEndTimeStamp), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.baseline, num: dd.num}
											]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								var flat_trgOpenSeriesData = _(trgOpenSeriesData).flatten().valueOf();

								//year add 1
								var tmpRet = (flat_trgOpenSeriesData).map(function(d) {
								    return {
								        date: d.date.replace(/(\d{4})(-.*)/, function (match, p1, p2) {
								            var tmp = parseInt(p1) + 1;
								            return tmp+p2;
								        }),
								        stats: d.stats
								    };
								});
								cb(null, tmpRet);
							},
							function(cb) { //ncdr_cum_ab
								var ret = calcuNumsOfPrs(uniqedResults_ab, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_cum_ab, num: trgOpenSeriesData[i].cumulation}]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //ncdr_cum_a
								var ret = calcuNumsOfPrs(uniqedResults_a, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_cum_a, num: trgOpenSeriesData[i].cumulation}]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},
							function(cb) { //ncdr_cum_b
								var ret = calcuNumsOfPrs(uniqedResults_b, interval, filterTimeList.ncdrBeginTimeStamp);
								var myRet = removeBeforeKey(ret, BEFOREKEY);
								var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																							moment.unix(ncdrTime.end), interval);

								var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

								trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

								trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
									return (d.yearData||[]).map(function (dd) {
										trgOpenSeriesData[i].cumulation += dd.num;
										return {
											date: dd.date,
											stats: [{name: names.ncdr_cum_b, num: trgOpenSeriesData[i].cumulation}]
										};
									});
								});// end (trgOpenSeriesData||[]).map
								cb(null, _(trgOpenSeriesData).flatten().valueOf());
							},

						], function(err, finalResults) {
							if(err) {console.log(err);}
							else {
								var rst = faultCommons.merge8ArrayWithSameItem(finalResults);
								// var rst = faultCommons.merge3ArrayWithSameItem(finalResults);

								cb(null, rst);
								// console.log("%j", rst);

							}
						});//end async.parallel

					}//end else
				}); // end db.collection('pr_summary')
			}, // end outer function(cb)
			function(cb) { //month_tar and target_cum
				var openSeries = faultCommons.generateDateIntervalSeries(moment.unix(ncdrTime.begin),
																		moment.unix(ncdrTime.end), interval);
				if (paramsQueryEXpr.params.targetOpts) {
					var targetFilterExpr = handleTargetFilters( paramsQueryEXpr.params.targetOpts,
															paramsQueryEXpr.params.planeGroupedOpts,
															paramsQueryEXpr.params.level4DuOpts,
															paramsQueryEXpr.params.productLineOpts,
															paramsQueryEXpr.params.productOpts,
															paramsQueryEXpr.params.systemOpts,
															paramsQueryEXpr.params.entityOpts,
															filterTimeList.realYearBegin,
															ncdrTime.end);
					db.collection('pr_goal_mapping').find(targetFilterExpr).toArray(function(err, results) {
						if (err) {
							console.log(err);
						} else {
							var myResult = getTargetData(results, interval);
							var ret = calcuNumsOfTarget(myResult, interval, ncdrTime.begin);
							var myRet = removeBeforeKey(ret, BEFOREKEY);

							var trgOpenSeriesData = megerData2OpenSerials(myRet.arr, openSeries);

							trgOpenSeriesData[0]["cumulation"] = myRet.beforekey_num;

							trgOpenSeriesData = (trgOpenSeriesData||[]).map(function(d, i) {
								return (d.yearData||[]).map(function (dd) {
									trgOpenSeriesData[i].cumulation += dd.num;
									return {
										date: dd.date,
										stats: [{name: names.month_tar, num: dd.num},
												{name: names.target_cum, num: trgOpenSeriesData[i].cumulation}
										]
									};
								});
							});// end (trgOpenSeriesData||[]).map
							cb(null, _(trgOpenSeriesData).flatten().valueOf());
						}
					});
				} else {
					var emptData = [];
					(openSeries||[]).forEach(function (d) {
						emptData.push({
										date: d,
										stats: [{name: names.month_tar, num: 0},
												{name: names.target_cum, num: 0}
										]
									});
					});
					cb(null, emptData);
				}
			},
		], function (err, lastResults) {
			// console.log("=====================================");
			// console.log("%j", lastResults);
			res.send(_.assign(paramsQueryEXpr.params, {results: faultCommons.merge2ArrayWithSameItem(lastResults)}));
		}); // end outer async.parallel
	});//end fault_filter.getFilters
});

router.get('/ncdr_details/ncdr_ab/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));
		// var ncdr_ab_severity = {"severity":{"$in":["A - Critical","B - Major"]}};
		// paramsQueryEXpr.queryExpr['$and'].push(ncdr_ab_severity);

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_ab/get/ ERROR!");}
			else {
				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});

				var uniqedResults = data2UniqFaultidByAll(ncdr_results_ab);
				var finalResults = _.filter(uniqedResults, function(d) {
					return d.createtimestamp >=intervalbegin && d.createtimestamp < intervalend;
				});

				res.send({results: finalResults});
			}
		});

	});
});
router.get('/ncdr_details/ncdr_a/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_ab/get/ ERROR!");}
			else {

				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});

				var uniqedResults_ab = data2UniqFaultidByAll(ncdr_results_ab);

				var uniqedResults_a = [];
				//filter SEVERITY_A
				(uniqedResults_ab||[]).forEach(function (d) {
					if(d.severity === SEVERITY_A) {
						uniqedResults_a.push(d);
					}
				});

				var finalResults = _.filter(uniqedResults_a, function(d) {
					return d.createtimestamp >= intervalbegin && d.createtimestamp < intervalend;
				});

				res.send({results: finalResults});
			}
		});

	});
});
router.get('/ncdr_details/ncdr_b/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_ab/get/ ERROR!");}
			else {
				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});

				var uniqedResults_ab = data2UniqFaultidByAll(ncdr_results_ab);

				var uniqedResults_b = [];
				//filter SEVERITY_A
				(uniqedResults_ab||[]).forEach(function (d) {
					if(d.severity === SEVERITY_B) {
						uniqedResults_b.push(d);
					}
				});

				var finalResults = _.filter(uniqedResults_b, function(d) {
					return d.createtimestamp >= intervalbegin && d.createtimestamp < intervalend;
				});


				res.send({results: finalResults});
			}
		});

	});
});
router.get('/ncdr_details/ncdr_c/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_ab/get/ ERROR!");}
			else {

				var uniqedResults_abc = data2UniqFaultidByAll(results);
				var uniqedResults_c = [];
				(uniqedResults_abc||[]).forEach(function (d) {
					if (d.severity === SEVERITY_C) {
						uniqedResults_c.push(d);
					}
				});

				var finalResults = _.filter(uniqedResults_c, function(d) {
					return d.createtimestamp >= intervalbegin && d.createtimestamp < intervalend;
				});

				res.send({results: finalResults});
			}
		});

	});
});

router.get('/ncdr_details/ncdr_cumulative/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_cumulative/get/ ERROR!");}
			else {
				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});
				var uniqedResults = data2UniqFaultidByAll(ncdr_results_ab);
				res.send({results: uniqedResults});

			}
		});

	});
});
router.get('/ncdr_details/ncdr_cumulative_a/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_cumulative/get/ ERROR!");}
			else {
				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});

				var uniqedResults_ab = data2UniqFaultidByAll(ncdr_results_ab);

				var uniqedResults_a = [];
				//filter SEVERITY_A
				(uniqedResults_ab||[]).forEach(function (d) {
					if(d.severity === SEVERITY_A) {
						uniqedResults_a.push(d);
					}
				});


				// var uniqedResults = data2UniqFaultidByAll(results);
				res.send({results: uniqedResults_a});

			}
		});

	});
});
router.get('/ncdr_details/ncdr_cumulative_b/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		if (intervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:intervalbeginOfYearBegin}});}
		if (intervalend) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: intervalend}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/ncdr_cumulative/get/ ERROR!");}
			else {
				var ncdr_results_ab = [];
				//filter A&B severity
				(results||[]).forEach(function (d) {
					if(SEVERITY_L1.indexOf(d.severity) !== -1) {
						ncdr_results_ab.push(d);
					}
				});

				var uniqedResults_ab = data2UniqFaultidByAll(ncdr_results_ab);

				var uniqedResults_b = [];
				//filter SEVERITY_B
				(uniqedResults_ab||[]).forEach(function (d) {
					if(d.severity === SEVERITY_B) {
						uniqedResults_b.push(d);
					}
				});

				res.send({results: uniqedResults_b});

			}
		});

	});
});


router.get('/ncdr_details/baseline/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function
		var interval = paramsQueryEXpr.params.interval;

		paramsQueryEXpr.queryExpr['$and'] = paramsQueryEXpr.queryExpr['$and'].concat(handleCommonFilters(paramsQueryEXpr.params.buBlOpts,
																	paramsQueryEXpr.params.orgCatOpts,
																	paramsQueryEXpr.params.planeGroupedOpts,
																	paramsQueryEXpr.params.planeOpts,
																	paramsQueryEXpr.params.level4DuOpts,
																	paramsQueryEXpr.params.componentOpts,
																	paramsQueryEXpr.params.customerOpts));

		var beginDate = faultCommons.formatDate(intervalbegin *1000, interval).replace(/(\d{4})(-.*)/, function (match, p1, p2 ) {
	        var tmp = parseInt(p1) - 1;
	        return tmp+p2;
	    });
	    var endDate = faultCommons.formatDate(intervalend *1000, interval).replace(/(\d{4})(-.*)/, function (match, p1, p2) {
	        var tmp = parseInt(p1) - 1;
	        return tmp+p2;
	    });

		var bslBeginTimeStamp = +moment(faultCommons.formatDate2TmStamp(beginDate, interval)*1000).startOf(interval).unix(); //consider same day in different year may not same in weeks
		var bslEndTimeStamp = +moment(faultCommons.formatDate2TmStamp(endDate, interval)*1000).endOf(interval).unix(); //consider same day in different year may not same in weeks

		var bslintervalbeginOfYearBegin = +moment(bslBeginTimeStamp*1000).startOf('year').unix();
		if (bslintervalbeginOfYearBegin) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$gte:bslintervalbeginOfYearBegin}});}
		if (bslEndTimeStamp) {paramsQueryEXpr.queryExpr["$and"].push({createtimestamp:{$lt: bslEndTimeStamp}});}


		db.collection('pr_summary').find(paramsQueryEXpr.queryExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/baseline/get/ ERROR!");}
			else {

				var uniqedResults = data2UniqFaultidByAll(results);
				var finalResults = _.filter(uniqedResults, function(d) {
					return d.createtimestamp >= bslBeginTimeStamp && d.createtimestamp < bslEndTimeStamp;
				});

				res.send({results: finalResults});
			}
		});

	});
});
router.get('/ncdr_details/monthly_target/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function
		var interval = paramsQueryEXpr.params.interval;

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		var targetFilterExpr = handleTargetFilters( paramsQueryEXpr.params.targetOpts,
															paramsQueryEXpr.params.planeGroupedOpts,
															paramsQueryEXpr.params.level4DuOpts,
															paramsQueryEXpr.params.productLineOpts,
															paramsQueryEXpr.params.productOpts,
															paramsQueryEXpr.params.systemOpts,
															paramsQueryEXpr.params.entityOpts,
															intervalbeginOfYearBegin, intervalend);


		db.collection('pr_goal_mapping').find(targetFilterExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/monthly_target/get/ ERROR!");}
			else {
				var myResult = getTargetData(results, interval);
				var beginDate = moment(intervalbegin * 1000).format('YYYY/MM/DD');
				var endDate = moment(intervalend * 1000).format('YYYY/MM/DD');

				var finalResults = _.filter(myResult, function(d) {
					return d.report_day >= beginDate && d.report_day <= endDate;
				});

				res.send({results: finalResults});

			}
		});

	});
});


router.get('/ncdr_details/target_cumulative/get', function(req, res) {
	fault_filter.getFiltersFaultDetail(req, function(paramsQueryEXpr) {
		var intervalbegin = paramsQueryEXpr.params.intervalbegin;
		var intervalend = paramsQueryEXpr.params.intervalend; //generate by father function
		var interval = paramsQueryEXpr.params.interval;

		var intervalbeginOfYearBegin = +moment(intervalbegin*1000).startOf('year').unix();

		var targetFilterExpr = handleTargetFilters( paramsQueryEXpr.params.targetOpts,
															paramsQueryEXpr.params.planeGroupedOpts,
															paramsQueryEXpr.params.level4DuOpts,
															paramsQueryEXpr.params.productLineOpts,
															paramsQueryEXpr.params.productOpts,
															paramsQueryEXpr.params.systemOpts,
															paramsQueryEXpr.params.entityOpts,
															intervalbeginOfYearBegin, intervalend);

		db.collection('pr_goal_mapping').find(targetFilterExpr).toArray(function (err, results){
			if (err) { console.log("ERROR: fault_ncdr_api.js/ncdr_details/target_cumulative/get/ ERROR!");}
			else {
				var myResult = getTargetData(results, interval);
				res.send({results: myResult});
			}
		});

	});
});

//get all bls from pr_mapping_release
router.get('/all_bl/get', function(req, res) {
    db.collection('pr_mapping_release').distinct('bl', function(err, results) {
        if (err) console.log(err);
        else {
        	res.send({results: results});
        }
    });
});

// router.get('/bl_yearly/get', function(req, res) {

// 	// var params = {};
// 	// _(req.query).forEach(function(value, key) {
// 	// 	params[key] = decodeURIComponent(value);
// 	// 	if (params[key]==='null') {params[key]=null;}
// 	// });
// 	var timeList = {};
// 	var yearUnixTimeStamp = moment(req.query.year, "YYYY").unix();

// 	timeList["yearBeginUnixTimeStamp"] = +moment(yearUnixTimeStamp*1000).startOf('year').unix();
// 	timeList["yearEndUnixTimeStamp"] = +moment(yearUnixTimeStamp*1000).endOf('year').unix();

// 	var mapping_bl_name = req.query.mapping_bl.replace('_', " ");

// 	// console.log(mapping_bl_name);
// 	var filterExpr = {'$and': [{mapping_bl: mapping_bl_name}]};
// 	if (req.query.year) {
// 		filterExpr['$and'].push({createtimestamp:{'$gte': timeList.yearBeginUnixTimeStamp,
// 													'$lt': timeList.yearEndUnixTimeStamp}});
// 	}

// 	db.collection('pr_summary').find(filterExpr, {_id: 0}).toArray(function (err, yearly_results){

// 		// filter customer issue and initial mapping_cal
// 		var yearData = {customer:[], nonecustomer:[]};
// 		(yearly_results||[]).forEach(function(d){
// 			if (_.has(d, "from_electra") && d.from_electra === "YES") {
// 				d['mapping_cal_ab'] = false;
// 				d['mapping_cal_a'] = false;
// 				d['mapping_cal_b'] = false;
// 				d['mapping_cal_c'] = false;
// 				yearData.customer.push(d);
// 			} else {
// 				d['mapping_cal_ab'] = null;
// 				d['mapping_cal_a'] = null;
// 				d['mapping_cal_b'] = null;
// 				d['mapping_cal_c'] = null;
// 				yearData.nonecustomer.push(d);

// 			}
// 		});


// 		var uniqData = uniqFaultId(yearData.customer);
// 		yearData.customer = markMappingTag(uniqData);
// 		var results = yearData.customer.concat(yearData.nonecustomer);

// 		res.send({results: results});
// 	});
// });

router.get('/bl_yearly/get', function(req, res) {

	// var params = {};
	// _(req.query).forEach(function(value, key) {
	// 	params[key] = decodeURIComponent(value);
	// 	if (params[key]==='null') {params[key]=null;}
	// });
	var timeList = {};
	var yearUnixTimeStamp = moment(req.query.year, "YYYY").unix();

	timeList["yearBeginUnixTimeStamp"] = +moment(yearUnixTimeStamp*1000).startOf('year').unix();
	timeList["yearEndUnixTimeStamp"] = +moment(yearUnixTimeStamp*1000).endOf('year').unix();

	var mapping_bl_name = req.query.mapping_bl.replace('_', " ");

	// console.log(mapping_bl_name);
	var filterExpr = {'$and': [{mapping_bl: mapping_bl_name}]};
	if (req.query.year) {
		filterExpr['$and'].push({createtimestamp:{'$gte': timeList.yearBeginUnixTimeStamp,
													'$lt': timeList.yearEndUnixTimeStamp}});
	}

	db.collection('pr_summary').find(filterExpr, {_id: 0}).toArray(function (err, yearly_results){

		// filter customer issue and initial mapping_cal
		var yearData = {customer:[], nonecustomer:[]};
		(yearly_results||[]).forEach(function(d){
			if (_.has(d, "from_electra") && d.from_electra === "YES") {
				d['mapping_cal_ab'] = false;
				d['mapping_cal_a'] = false;
				d['mapping_cal_b'] = false;
				d['mapping_cal_c'] = false;
				yearData.customer.push(d);
			} else {
				d['mapping_cal_ab'] = null;
				d['mapping_cal_a'] = null;
				d['mapping_cal_b'] = null;
				d['mapping_cal_c'] = null;
				yearData.nonecustomer.push(d);

			}
		});


		var uniqData = uniqFaultId(yearData.customer);
		yearData.customer = markMappingTag(uniqData);
		var results = yearData.customer.concat(yearData.nonecustomer);

		res.send({results: results});
	});
});

/**
 * [markMappingTag description]
 * @param  {[type]: object} obj [description][such as: {"faultId1":[{data1},{data2}],
 *                                   	  				"faultId2": [{data3}]}]
 * @return {[type]: Array}      [description]
 */
function markMappingTag (obj) {
	var tmpArray = [];
	_.forIn(obj, function(values) {
		//1: sortBy create time for every faultid, ascending
		values.sort(function numAscending(index1, index2) {
		    return index1.createtimestamp - index2.createtimestamp;
		});

		//2: found vaild Prs.
		var findItem_ab = _.find(values, function (d) {	//returning the first element predicate
			return faultCommons.isInArray(SEVERITY_L1, d.severity);
		});

		if (findItem_ab) {
			(values||[]).forEach(function(d) {
				if(d.prid === findItem_ab.prid) {
					d['mapping_cal_ab'] = true;
					(d.severity === SEVERITY_A) ? d['mapping_cal_a'] = true : d['mapping_cal_b'] = true;
				}
				tmpArray.push(d);
			});
		} else { //not find severity_a/b
			(values||[]).forEach(function(d, i) {
				if(i === 0) {
					d['mapping_cal_c'] = true;
				}
				tmpArray.push(d);
			});
		}
	});
	return tmpArray;
}


module.exports = router;
