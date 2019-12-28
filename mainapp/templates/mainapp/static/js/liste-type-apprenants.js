$(document).ready(function(){

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_type_apprenant");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces,
             error: gererErreur,
         });

    });

      function gererSucces(data){
        console.log(data);

          if(data.permissions.indexOf("typeapprenant") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_type_apprenants = data.type_apprenants;
              nbre_element_par_page = data.nbre_element_par_page;
              numero_page_active = data.numero_page_active;
              liste_page = data.liste_page;

              trier_par = data.trier_par;
              ordre = data.ordre;

              data_color = data.data_color;
              sidebar_class = data.sidebar_class;
              theme_class = data.theme_class;

      /* initialise debut et la fin des elements du tableau(resultat de la recherche) pour une meilleure pagination*/
              debut = parseInt((numero_page_active-1) * nbre_element_par_page);
              fin = parseInt(numero_page_active * nbre_element_par_page);

      /* gere l'affichage des elements de la derniere page*/
              if (liste_page[liste_page.length-1] == numero_page_active){
                debut = (numero_page_active-1)*nbre_element_par_page; 
                fin = data.type_apprenants.length;
              }

              if (liste_type_apprenants.length != 0){

                  for (var i = debut; i < fin; i++) {

                      nom_sousetab = liste_type_apprenants[i].nom_sousetab                      
                      type_apprenant = liste_type_apprenants[i].nom_type_apprenant;
                      id = liste_type_apprenants[i].id;
                      // alert(nom_etab, nom_sousetab, type_apprenant, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ type_apprenant +'²²'+ nom_sousetab +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-type-apprenant-link-td fix-col1">'+ type_apprenant + '</td><td style="text-transform: uppercase;" class="detail-type-apprenant-link-td">'+ nom_sousetab +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-type-apprenant-link-td btn" data-toggle="modal" data-target="#modal_detail_type_apprenant"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-type-apprenant-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-type-apprenant-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-type-apprenant-link");
                    // alert(data.permissions.indexOf("type_apprenants"));

                        index_model = data.permissions.indexOf("typeapprenant")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-type-apprenant-link").remove();
                        }                      
                        if(data.permissions[index_model + 4] ==1 ){
                          nouvelle_ligne += del;
                        }

                        $("table tbody").append(nouvelle_ligne);
                      
                    
                    
                    

                  }

                possede_page_precedente = data.possede_page_precedente;
                possede_page_suivante = data.possede_page_suivante;
                
                suivant = numero_page_active + 1;
                precedent = numero_page_active - 1;


                $(".pagination .contenu").remove();

                resultat_pagination = '<div class="contenu">';

                if(possede_page_precedente == true){
                  resultat_pagination += '<button class="btn btn-white btn-sm pagination-element" id="'+precedent +'"><i class="material-icons">arrow_back_ios</i></button>';
                }else{
                  resultat_pagination += '<button class="btn btn-sm btn-white pagination-element" id="" disabled><i class="material-icons">arrow_back_ios</i></button>';
                }

                for (var num_page= 0; num_page < liste_page.length; num_page++) {

                    if (liste_page[num_page] == numero_page_active){
                     
                      resultat_pagination +='<button class="btn btn-sm pagination-element" id="'+liste_page[num_page]+'">'+ liste_page[num_page]+'</button>';
                    
                    }else{
                      
                      resultat_pagination +='<button class="btn btn-sm pagination-element" id="'+ liste_page[num_page] +'">'+ liste_page[num_page]+'</button>';
                      
                    }
                  
                }

                if(possede_page_suivante == true){
                  resultat_pagination += '<button class="btn btn-white btn-sm pagination-element" id="'+ suivant +'"><i class="material-icons">arrow_forward_ios</i></button>'
                }else{
                  resultat_pagination += '<button class="btn btn-white btn-sm pagination-element" id="" disabled><i class="material-icons">arrow_forward_ios</i></button>'
                }
            
                resultat_pagination += '</div>';

                $(".pagination").append(resultat_pagination);

              }
              else{
                /* aucun resultat de la recherche*/

                  nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Aucun élément(s) ne correspond à votre recherche</td></tr>';                
                  
                  $("table tbody").append(nouvelle_ligne);
                 

                  $(".pagination .contenu").remove();
              }

            //affiche le message en cas d'erreur
              if (data.message_resultat != ""){
                  $("#message").text(data.message_resultat).css('color',"red");
              }

        }

      /* mettre a jour le nouveau theme de l'utilisateur */
      $(".sidebar").attr("data-color", data_color);
      $(".sidebar").addClass(sidebar_class);
      $(".btn").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
      $(".btn-rond").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);

      }

      function gererErreur(error) {
      $("#message").text(error);
      console.log(error);
      }


    $("body").on("click", ".ajouter-type-apprenant-link", function() {
        
        $('#modal_ajouter_type_apprenant').modal('show');

        $("#modal_ajouter_type_apprenant .type_apprenant").val(type_apprenant);
        $("#modal_ajouter_type_apprenant .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_ajouter_type_apprenant .type_apprenant").val("");
        $("#modal_ajouter_type_apprenant .nom_sousetab").val("");

    });

    // $(".detail-type-apprenant-link-td").click(function() {
     $("body").on("click", ".detail-type-apprenant-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.type_apprenant }}²²{{ cycl.sous_type_apprenant }}²²{{ cycl.type_apprenant }}"
        $('#modal_detail_type_apprenant').modal('show');

        var type_apprenant = $(this).parents("tr").attr('class');
        tab_element = type_apprenant.split("²²");
        id = tab_element[0];
        type_apprenant = tab_element[1];
        nom_sousetab = tab_element[2];
      
        $("#modal_detail_type_apprenant .type_apprenant").val(type_apprenant);
        $("#modal_detail_type_apprenant .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_detail_type_apprenant .type_apprenant").attr("disabled", "True");
        $("#modal_detail_type_apprenant .nom_sousetab").attr("disabled", "True");

    });


    $(".modifier-type-apprenant-link").click(function() {
        $('#modal_modifier_type_apprenant').modal('show');

        var type_apprenant = $(this).parents("tr").attr('class');
        tab_element = type_apprenant.split("²²");
        id = tab_element[0];
        type_apprenant = tab_element[1];
        nom_sousetab = tab_element[2];

        $("#modal_modifier_type_apprenant .type_apprenant").val(type_apprenant);
        $("#modal_modifier_type_apprenant .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_modifier_type_apprenant .type_apprenant").removeAttr("disabled");
        $("#modal_modifier_type_apprenant .nom_sousetab").removeAttr("disabled");

    });



    $(".supprimer-type-apprenant-link").click(function() {

      $('#modal_supprimer_type_apprenant').modal('show');

      var type_apprenant = $(this).parents("tr").attr('class');
      tab_element = type_apprenant.split("²²");
      id = tab_element[0];
        type_apprenant = tab_element[1];
        nom_sousetab = tab_element[2];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_type_apprenant .type_apprenant").text(type_apprenant);
      $("#modal_supprimer_type_apprenant .nom_sousetab").text(nom_sousetab);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_type_apprenant");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var type_apprenant = String($(this).attr("class"));

              if(type_apprenant.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (type_apprenant.search("tri-desc") != -1){
                      trier_par = "-" + trier_par; 
                  }

              }


        });

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces,
             error: gererErreur,
         });

    });
      
    $("body").on("click", ".supprimer-type-apprenant-link-ajax", function() {
        
        $('#modal_supprimer_type_apprenant').modal('show');

         var type_apprenant = $(this).parents("tr").attr('class');
          tab_element = type_apprenant.split("²²");
          id = tab_element[0];
          type_apprenant = tab_element[1];
          nom_sousetab = tab_element[2];

          $("#id_supp").val(id);
          $("#modal_supprimer_type_apprenant .type_apprenant").text(type_apprenant);
          $("#modal_supprimer_type_apprenant .nom_sousetab").text(nom_sousetab);

    });


    $("body").on("click", ".modifier-type-apprenant-link-ajax", function() {
        
        $('#modal_modifier_type_apprenant').modal('show');

        var type_apprenant = $(this).parents("tr").attr('class');
        tab_element = type_apprenant.split("²²");
        id = tab_element[0];
        type_apprenant = tab_element[1];
        nom_sousetab = tab_element[2];

        $("#modal_modifier_type_apprenant .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_type_apprenant .type_apprenant").val(type_apprenant);
        $("#id_modif").val(id);

        $("#modal_modifier_type_apprenant .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_type_apprenant .type_apprenant").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_type_apprenant");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th span").each(function () {

                var type_apprenant = String($(this).attr("class"));

                if(type_apprenant.search("text-primary") != -1){

                    trier_par = $(this).parents("th").attr("class");

                    if (type_apprenant.search("tri-desc") != -1){
                        trier_par = "-" + trier_par; 
                    }

                }


          });
 

          var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par;

           $.ajax({
               method: 'POST',
               url: url_action,
               data: {
                 form_data : donnees,
                 csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
               },
               success: gererSucces,
               error: gererErreur,
           });       
  
    });

  //$('table th').click(function(e){e.preventDefault();}).click();


   $("body").on("click", ".tri-asc", function(e) {

        e.stopImmediatePropagation();

        $(".tri").find("img").attr("src", "/static/images/arrow.png");
        $(this).find("img").attr("src", "/static/images/up.png");

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " ";

        var form = $(".recherche_type_apprenant");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class").split(" ")[0];
        

        $(this).attr("class", trier_par + " tri tri-desc");

      
        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces,
             error: gererErreur,
         });



    });


   $("body").on("click", ".tri-desc", function(e) {

        e.stopImmediatePropagation();

        $(".tri").find("img").attr("src", "/static/images/arrow.png");
        $(this).find("img").attr("src", "/static/images/down.png");        

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_type_apprenant");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class").split(" ")[0];
        

        $(this).attr("class", trier_par + " tri tri-asc");


        // tri decroissant 
        trier_par = "-" + trier_par;
      
        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par ;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces,
             error: gererErreur,
         });

          
    });



});
