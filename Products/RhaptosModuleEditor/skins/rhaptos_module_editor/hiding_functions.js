function showId(elementId){
    var elem = document.getElementById(elementId);
    elem.style.display=''
}
function hideId(elementId){
    var elem = document.getElementById(elementId);
    elem.style.display='none'
}
	
function getElementsByClassName(classname){
        var rl = new Array();
        var re = new RegExp('(^| )'+classname+'( |$)');
        var ael = document.all ? document.all : document.getElementsByTagName('*');
        for (i=0, j=0 ; i<ael.length ; i++) {
                if(re.test(ael[i].className)) {
                        rl[j] = ael[i];
                        j++;
                }
        }
        return rl;
}

document.getElementsByClassName=getElementsByClassName;

function hide(clName) {
        var x = document.getElementsByClassName(clName);
        for (var i = 0; i < x.length; i++) {
                x[i].style.display = 'none';
        }
}

function show(clName) {
        var x = document.getElementsByClassName(clName);
        for (var i = 0; i < x.length; i++) {
                x[i].style.display = '';
        }
}

function toggleExpand(clickedElement, clName){
    var x = document.getElementsByClassName(clName);
    var text = document.getElementById('expand_collapse_label');
    if (clickedElement.hasAttribute("iscollapsed")) {
        show(clName);
        clickedElement.removeAttribute("iscollapsed");
        text.innerHTML = 'Collapse All';
    }
    else {
        hide(clName);
        clickedElement.setAttribute("iscollapsed", "1");
        text.innerHTML = 'Expand All';
    }
}

function toggleExpandId(clickedElement, id){
    var x = document.getElementById(id);
    if (x.style.display == 'none') {
        showId(id);
    }
    else {
        hideId(id);
    }
}
