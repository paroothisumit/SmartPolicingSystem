var getStyledString=function(siteObject,message,media_file_name){
    
    var str;
    var styler="<style>"+
    ".outer-safe {"+
        "background-color:rgb(91,175,45);text-align:center;"+
    "}"+
    ".outer-alert {"+
        "background-color:rgb(214,74,74);text-align:center;"+
    "}"+
    "</style>";
    if(message==undefined){
        str='<div class="outer-safe">'+
            '<div style="font-size:30px;font-family:"Lucida Console", Monaco, monospace">'+'Site '+siteObject.siteId+'</div>'+
            '<div style="font-size:30px">'+siteObject.description+'</div>'+
            '<div style="font-size:25px;font-style:italic">'+siteObject.address+'</div>'+
            '<br>'+'<br>'+
            '<div style="font-size:25px;font-style:italic">'+'No suspicious activity detected'+'</div>'+
            '</div>';
                
    }
    else{
        
        console.log(media_file_name);
        media_file_name="uploads//"+media_file_name;
        str='<div class="outer-alert">'+
            '<div style="font-size:30px;font-family:"Lucida Console", Monaco, monospace">'+'Site '+siteObject.siteId+'</div>'+
            '<div style="font-size:30px">'+siteObject.description+'</div>'+
            '<div style="font-size:25px;font-style:italic">'+siteObject.address+'</div>'+
            '<br>'+'<br>'+
            '<div style="font-size:25px;font-style:italic">'+'Suspicious activity detected'+'</div>'+
            '<div style="font-size:25px;font-style:italic">'+message.activity_recognized+' at '+message.Time+'</div>'+
            '<div style="font-size:25px;font-style:italic">'+'<button id="show_btn" onclick="toggleDisplay(\''+media_file_name+'\')">Show Media ' +'</button>'+'</div>'+
            
            '</div>';
        
    }

    return styler+str;
}