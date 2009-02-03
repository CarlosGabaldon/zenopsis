var site = "http://zenopsis.com/";
var previewUrl = site+"synopsis/"+zenopsis_name+"/preview";
document.write("<div><table style='border-collapse: collapse; border-spacing: 0pt; margin: 0px; padding: 0px;'><tbody><tr><td><img id='zenopsis-preview-img' src='"+site+"site_media/images/down-arrow.gif' alt='Zenopsis preview' onclick='loadPreview();'/></td><td><div style='float: left; margin-top: 2px; text-align: left; width: 100%;'><span style='font-family: "+'Trebuchet MS'+", Arial, sans-serif; font-weight: bold; font-size: 14px; color: #a0cc7a;'>Zenopsis</span>: "+zenopsis_name+"</div></td></tr><tr><td colspan='2'><div id='zenopsis-preview'></div></td></tr></tbody></table></div>");

function loadPreview() {
    var div = document.getElementById("zenopsis-preview");
    var img = document.getElementById("zenopsis-preview-img");
    if (div.innerHTML == "") {	
        div.innerHTML = "<iframe frameborder='1' scrolling='auto' width='100%' src='"+previewUrl+"'></iframe>";
	img.setAttribute("src", site+"site_media/images/up-arrow.gif");
    }
    else {
        div.innerHTML = "";
	img.setAttribute("src", site+"site_media/images/down-arrow.gif");	
    }
}
