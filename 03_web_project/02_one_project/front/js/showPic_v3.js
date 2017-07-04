/**
 * Created by changpzh on 2016/6/12.
 */
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
//把一个节点插入到某一个节点之后。
function insertAfter(newElement,targetElement) {
    var parent = targetElement.parentNode;
    if (parent.lastChild == targetElement) {
        parent.appendChild(newElement);
    } else {
        parent.insertBefore(newElement, targetElement.nextSibling);
    }
}
function preparePlaceholder() {
    if (!document.createElement) return false;
    if (!document.createTextNode) return false;
    if (!document.getElementById) return false;
    if (!document.getElementById("imagegallery")) return false;
    var placeholder = document.createElement("img");
    placeholder.setAttribute("id", "placeholder");
    placeholder.setAttribute("src", "../images/placeholder.gif");
    placeholder.setAttribute("alt", "my image gallery");
    var para = document.createElement("p");
    para.setAttribute("id", "description");
    var desctext = document.createTextNode("Choose an image");
    para.appendChild(desctext);
    var gallery = document.getElementById("imagegallery");
    insertAfter(placeholder, gallery);
    insertAfter(para, placeholder);
    //gallery.parentNode.insertBefore(placeholder, gallery);
    //gallery.parentNode.insertBefore(para, gallery);
}

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
        links[i].onkeypress = links[i].onclick;
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
//页面加载完成时会触发一个onload事件。
addLoadEvent(preparePlaceholder);
addLoadEvent(prepareGellery);