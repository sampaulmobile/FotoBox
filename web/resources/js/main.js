$(document).ready(function() {
    
    $(".star_power")
        .mouseover(function() {
            console.log($(this).attr("src"))
            if ($(this).attr("src")=="/resources/img/star_pushed.png") {
                
            } else {
                var src = $(this).attr("src").match(/[^\.]+/) + "_hover.png";
                $(this).attr("src",src);
            }
        })
        
        .mouseout(function() {
            if ($(this).attr("src")[-5]=='d') {
            } else {
                var src = $(this).attr("src").replace("_hover", "");
                $(this).attr("src", src);
            }
        })
        
        .click(function() {
            if ($(this).attr("src")=="/resources/img/star_pushed.png") {
                var src = $(this).attr("src").replace("pushed", "hover");
                $(this).attr("src",src);
            } else {
                var src = $(this).attr("src").replace("_hover", "_pushed");
                $(this).attr("src",src);
            }  
            $.post("/profiles/toggle_favorite", { 
                stardr: $(this).attr("id")
            }, function(data){
                console.log(help);
   
            },"json"
            );   
        });
        
});