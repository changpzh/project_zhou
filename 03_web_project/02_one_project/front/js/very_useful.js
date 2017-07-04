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
//页面加载完成时会触发一个onload事件。
//addLoadEvent(countBodyChildren);
addLoadEvent(prepareGellery);
