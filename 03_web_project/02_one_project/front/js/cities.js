/**
 * Created by changpzh on 2016/6/28.
 */
function stripeTables() {
    if (!document.getElementsByTagName) return false;
    var tables = document.getElementsByTagName("table");
    console.log("table length: " + tables.length);
    var odd, rows;
    for (var i=0; i<tables.length; i++) {
        odd = false;
        rows = tables[i].getElementsByTagName("tr");
        console.log("I'm here! rows_length" + rows.length);
        for (var j=0; j<rows.length; j++) {
            if (odd == true) {
                rows[j].style.backgroundColor = "#ffc";
                odd = false;
            }else {
                odd = true;
            }
        }
    }
}

function addClass(element, value) {

}

//页面加载完成时会触发一个onload事件。
addLoadEvent(stripeTables);