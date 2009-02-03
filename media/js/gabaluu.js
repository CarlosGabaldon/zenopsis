(function(){
/*
 *
 * Copyright (c) 2007 Carlos Gabaldon (gabaluu.com)

 *
 * $Date: 2007-10-05 
 */

    var gabaluu = {};
    

    $(document).ready(function(){

        gabaluu.synopsis.init();
        
        
    });
    
    /**
     * Synopsis application
     * @class gabaluu.synopsis
     */
    gabaluu.synopsis = {
        
        init: function(){
            
            $("form.comment-form").submit(this.addComment);
            $("a.vote-up").click(this.vote);
            
	        $("textarea.link-code").click(function() {
	            $(this).focus();
		        $(this).select();
	        });
	        
	        if (location.pathname  == "/synopsis/new/"){
	           setInterval(this.checkCharCount, 1000);
            }
        },
        
        
        checkCharCount: function(){
            
            gabaluu.synopsis.charCounter($('#id_title'), 50, $('#titleCounter'));
            gabaluu.synopsis.charCounter($('#id_text'), 1000, $('#bodytextCounter'));
        },
        
        charCounter: function(field, maxLength, countTarget){
            var inputLength=field.val().length;
            countTarget.html(maxLength-field.val().length);
            
            if(inputLength>=maxLength){
                countTarget.html("0")
            }
            
        },
        
        charLimit: function(field, maxLength){
            var inputLength=field.val().length;
            if(inputLength>=maxLength){
                field.val(field.val().substring(0, maxLength));
            }
        },
        
        vote: function(){
             var link = $(this)
             $.ajax({
                  type: "POST",
                  url: link.attr("href"),
                  dataType: "json",
                  success: function(json){
                       var voteCountFieldId = "#synopsis-" + json.synopsis + "-vote"
                       $(voteCountFieldId).replaceWith(json.votes)
                       link.hide();
                     
                  }
                });
           
            return false;
        },
          
        addComment: function(){
            
            var comment = $(this).find("textarea.comment").val(); 
            var apiURL = $(this).attr("action");
            
            
            if (comment != "" && comment != "undefined"){
                gabaluu.synopsis.postComment(comment, apiURL, gabaluu.synopsis.refreshComments);
            }
            
            $(this).find("textarea.comment").val("");
            
            return false;
        },
        
        refreshComments: function(comment){
            
            var url = this.url;
            var comment_id = null;
            var id = null;
            var re = /\/synopsis\/(\w+)\/comments\/(\w+)\/create\//;
            var path = re.exec(url);
            
            if (path != null){
                
                comment_id = path[2];
                
                if (comment_id != null){
                
                    commentListId = "#reply_to_comment_list_" + comment_id + " ul";
                    commentFormDivId = "#comment_" + comment_id + "_reply_to";
                    $(commentListId)
                        .append(comment)
                            .find("form")
                                .submit(gabaluu.synopsis.addComment)   
                                    .find("textarea.comment")
                                        .html("");
                    $(commentFormDivId).toggle();
                   
                }
                
            }
            else {
                
                $("#comments-section ul.main-thread").append(comment);
                $("#comments-section")
                    .find("form.comment-form")
                        .submit(gabaluu.synopsis.addComment)
                            .find("textarea.comment")
                                .html("");
      
                
            }
            
        },
        
        postComment: function(comment, url, callback){
            
            $.ajax({
              type: "POST",
              url: url,
              data: $.param({ comment: comment }),
              success: callback
            });
            
        }

    };
        
    
})();