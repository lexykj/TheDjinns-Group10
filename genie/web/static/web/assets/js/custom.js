var allCodes = document.getElementsByClassName("code");

var seeCode = function(){
	var code = this.getAttribute("data-code");
	alert("Show your lot attendant the following code:\n" + code);
};

for(var i = 0; i < allCodes.length; i++){
	allCodes[i].addEventListener('click', seeCode);
}

var collapsible = document.getElementsByClassName("collapsible");
var j;

for (j = 0; j < collapsible.length; j++){
    collapsible[j].addEventListener("click", function(){
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
            content.style.maxHeight = null;
        }else{
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
}