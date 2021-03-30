var allCodes = document.getElementsByClassName("code");

var seeCode = function(){
	var code = this.getAttribute("data-code");
	alert("Show your lot attendant the following code:\n" + code);
};

for(var i = 0; i < allCodes.length; i++){
	allCodes[i].addEventListener('click', seeCode);
}