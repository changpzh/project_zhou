/**
 * Created by changpzh on 2016/6/17.
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