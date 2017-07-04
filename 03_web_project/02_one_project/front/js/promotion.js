/**
 * Created by changpzh on 2016/6/12.
 */
var tabletiles = ["zhou", "chang", "ping"];
var data = ["20160601", "TL00_ENB_9999_160601_046160", "auto", "qt",2];
var testphase = {1: "QT", 2: "CIT"};

function preparePromotionTable(){
    var html = "";
    html += "<table class='gridtable'>";
    html += "<caption>" + tabletiles[0] + "</caption>";
    html += "<tr><th>Date</th><th>QT</th></tr>";
    ////动态创建多个列
    //for (var i = 0; i < date[-1]; i++) {
    //    html += "<th>testphase['i']</th>";
    //}
    html +=  "<tr><td>" + data[0] + "</td><td>" + data[1] + "</td><td>" + data[2] + "</td></tr>";

    html += "</table>";
    return html
}

function promotionHead() {

}

function preparePromotionTable(tabletiles, data) {
    if (!document.createElement) return false;
    if (!document.createTextNode) return false;
    if (!document.getElementById) return false;
    if (!document.getElementById("scmenu")) return false;

    //1：添加一个table
    var promotiontable = document.createElement("table");
    //2：设置table的class属性 为promotiontable
    promotiontable.setAttribute("class", "gridtable");


    var phasenum = data[data.length];
    for (var i = 0; i < phasenum; i++) {
        //3：添加第一个 tr，
        var firttr = document.createElement("tr");
        //4：设置第一个 tr的属性为tableth
        firttr.setAttribute("class", "tableth");
        //5：添加第一个tr的th，根据post的数据data[-1]，决定添加几个th。最少两个。
        for(var j=1;j<=list;j++){}

    }

    //6：添加第二个 tr，
    //7：设置第二个tr的class属性tablethsub
    //8：添加第二个tr的th，根据post的数据data[-1]，决定添加几个th。最少一个。
    //9：添加第三个tr，---数据信息。
    //10：设置第三个tr的class属性为promotiondata
    //11：添加第三个tr的td。根据post的数据data[-1]，决定添加几个td，最少3个td。




    //create title of table.
    var promotioncaption = document.createElement("caption");
    var tabletitle = document.createTextNode(tabletiles[0]);
    promotioncaption.appendChild(tabletitle);

    //create th in table
    var tr = document.createElement("tr");
    tr.setAttribute("class", "title_tr");

    var th = document.createElement("th");
    var dtime = document.createTextNode(data[0]);
    para.appendChild(desctext);
    var gallery = document.getElementById("imagegallery");
    insertAfter(placeholder, gallery);
    insertAfter(para, placeholder);
    //gallery.parentNode.insertBefore(placeholder, gallery);
    //gallery.parentNode.insertBefore(para, gallery);
}

function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != "function") {
        window.onload = func;
    } else {
        window.onload = function() {
            oldonload();
            func();
        }
    }
}
addLoadEvent(preparePromotionTable);
