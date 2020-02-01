$(document).ready(function(){

    var is_nb_matformat_ok = $('#is_nb_matformat_ok').attr('class');
    // alert(is_nb_matformat_ok);
    if (is_nb_matformat_ok == "ok"){
      // $('.terminer').prop("disabled", false);
      // alert("Ok");
      $('.terminer').removeAttr("disabled")
    }
    else{
      // alert("disabled");
      $('.terminer').prop("disabled", true);
    }

    $(".loader").hide();

    $(".terminer").click(function(e) {
      $(".loader").show();
      $(".table-responsive").css('display', 'none');
      $(".pagination").css('display', 'none');

            
            //e.stopImmediatePropagation(); 
                  //$("#form").submit();
                  $(".loader").show();
                  // var form = $("#form").submit();
                  
                  var url_action = $("#form").attr("action");

                  // alert(isConfig + url_action);             

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
                   });
            
    });
              
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

    $(".modifier-sousetab-link").click(function() {
        $('#modal_modifier_sousetab').modal('show');

        var sousetab = $(this).parents("tr").attr('class');
        tab_element = sousetab.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        format_matricule = tab_element[2];

        $("#modal_modifier_sousetab .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_sousetab .format_matricule").val(format_matricule);
        $("#id_modif").val(id);

        $("#modal_modifier_sousetab .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_sousetab .format_matricule").removeAttr("disabled");

        // sessionStorage.setItem("id_modif", id);
        $.session.set('id_modif', id);

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
