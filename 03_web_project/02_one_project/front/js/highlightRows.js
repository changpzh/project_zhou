/**
 * Created by changpzh on 2016/6/28.
 */
function highlightRows() {
    if(!document.getElementsByTagName) return false;
    var rows = document.getElementsByTagName("tr");
    console.log("row_length: " + rows.length);
    console.log(rows);
    for (var i=0; i<rows.length; i++) {
        var backColor;
        rows[i].onmouseover = function() {
            this.style.fontWeight = "bold";
            console.log(this.style.backgroundColor);
            backColor = this.style.backgroundColor;
            this.style.backgroundColor = "#acbad4"
        };
        rows[i].onmouseout = function() {
            this.style.fontWeight = "normal";
            this.style.backgroundColor = backColor
        };
    }
}
addLoadEvent(highlightRows);