/**
 * Created by changpzh on 2016/6/17.
 */
function displayAbbreviations () {
    if (!document.getElementsByTagName || !document.createElement || !document.createTextNode) return false;
    //get all abbreviation words.
    var abbreviation = document.getElementsByTagName("abbr");
    if (abbreviation.length < 1) return false;
    var defs = new Array;
    //遍历缩略词
    for (var i = 0; i < abbreviation.length; i++) {
        var current_abbr = abbreviation[i];
        if (current_abbr.childNodes.length < 1) continue; //如果当前元素没有子节点，就立刻开始下一次循环。
        var definition = current_abbr.getAttribute("title");
        var key = current_abbr.lastChild.nodeValue;
        console.log("key:" + key);
        defs[key] = definition;
    }
    //创建定义列表
    var dlist = document.createElement("dl");
    //遍历定义
    for (key in defs) {
        var definitionN = defs[key];
        //创建定义标题
        var dtitle = document.createElement("dt");
        var dtitle_text = document.createTextNode(key);
        dtitle.appendChild(dtitle_text);
        //创建定义描述
        var ddesc = document.createElement("dd");
        var ddesc_text = document.createTextNode(definitionN);
        ddesc.appendChild(ddesc_text);
        //把他们添加到定义列表
        dlist.appendChild(dtitle);
        dlist.appendChild(ddesc);
    }
    if (dlist.childNodes.length < 1) return false;
    //创建标题
    var header = document.createElement("h2");
    var header_text = document.createTextNode("Abbreviation");
    header.appendChild(header_text);

    //把标题添加到页面主体
    document.body.appendChild(header);
    //把定义列表添加到页面主体
    document.body.appendChild(dlist);
}

addLoadEvent(displayAbbreviations);
