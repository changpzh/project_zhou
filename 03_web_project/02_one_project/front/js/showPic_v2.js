/**
 * Created by changpzh on 2016/6/12.
 */
function prepareGellery() {
    if (!document.getElementsByTagName) return false;
    if (!document.getElementById) return false;
    if (!document.getElementById("imagegallery")) return false;
    var gallery = document.getElementById("imagegallery");
    var links = gallery.getElementsByTagName("a");
    //alert (typeof links)
    for (var i = 0; i < links.length; i++){
        links[i].onclick = function() {
            return showPic(this) ? false : true;
        }
    }
}
function showPic(whichpic){
    if (!document.getElementById("placeholder")) return false;
    var source = whichpic.getAttribute("href");
    var placeholder = document.getElementById("placeholder");
    if (placeholder.nodeName != 'IMG') return false;
    placeholder.setAttribute("src", source);
    if (document.getElementById("description")) {
        var text = whichpic.getAttribute("title") ? whichpic.getAttribute("title") : "";
        var description = document.getElementById("description");
        if (description.firstChild.nodeType == 3) {
            description.firstChild.nodeValue = text;
        }
    }
    return true;
}
function countBodyChildren(){
    var body_element = document.getElementsByTagName("body")[0];
    //alert (body_element.nodeType);
}

//用于多个函数绑定到onload事件中。
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
//页面加载完成时会触发一个onload事件。
//addLoadEvent(countBodyChildren);
addLoadEvent(prepareGellery);