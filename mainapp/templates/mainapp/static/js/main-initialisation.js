$(document).ready(function(){

$(".loader").hide();
          
$(".save").click(function(e) {
        
        //e.stopImmediatePropagation(); 
        
        var isConfig = $('#config').attr('class');
        //alert(isConfig);
        
        if(isConfig == 1){

          var result = confirm("vous allez supprimer l'ancienne configuration. Voulez vous continuer ?");

        }
          if(result == true || isConfig == 0){
              //$("#form").submit();
              $(".loader").show();
              var form = $("#form").submit();
              
             /* var url_action = $("#form").attr("action");

              alert(isConfig + url_action);             

              var donnees = "";

               $.ajax({
                   method: 'POST',
                   url: url_action,
                   data: {
                     form_data : donnees,
                     csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                   },
                   success: gererSucces,
                   error: gererError,
               });*/

            

          }
        
     

    });


     function gererSucces(data){
        console.log(data);
        //$(".loader").hide();
        
     }

     function gererError(error){
        console.log(error);
        //$(".loader").hide();
     }


});
