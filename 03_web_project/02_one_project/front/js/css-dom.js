/**
 * Created by changpzh on 2016/6/28.
 */
function test() {
    var paras = document.getElementsByTagName("p");
    console.log("you are here");
    for (var i = 0; i < paras.length; i++) {
        console.log("we are here");
        console.log(paras[i]);
        paras[i].onclick = function() {
            console.log('npwww');
            alert("You clicked on a paragraph.");
        }
    }
}
window.onload = test;