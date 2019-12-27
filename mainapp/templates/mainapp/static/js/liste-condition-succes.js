$(document).ready(function(){

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_condition_succes");
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

          if(data.permissions.indexOf("conditionsucces") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_c_succes = data.c_success;
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
                fin = data.c_success.length;
              }

              if (liste_c_succes.length != 0){

                  for (var i = debut; i < fin; i++) {
                      moyenne = liste_c_succes[i].moyenne;
                      nom_niveau = liste_c_succes[i].nom_niveau                      
                      nom_sousetab = liste_c_succes[i].nom_sousetab                      
                      id = liste_c_succes[i].id;
                      // alert(nom_etab, nom_sousetab, nb_heures_max, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+moyenne +'²²'+ nom_niveau +'²²'+ nom_sousetab +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-condition-succes-link-td fix-col1">'+ moyenne +'</td><td style="text-transform: uppercase;" class="detail-condition-succes-link-td">'+ nom_niveau + '</td><td style="text-transform: uppercase;" class="detail-condition-succes-link-td">'+ nom_sousetab +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-condition-succes-link-td btn" data-toggle="modal" data-target="#modal_detail_condition_succes"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-condition-succes-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-condition-succes-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-condition-succes-link");
                    // alert(data.permissions.indexOf("disciplines"));

                        index_model = data.permissions.indexOf("conditionsucces")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-condition-succes-link").remove();
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


    $("body").on("click", ".ajouter-condition-succes-link", function() {
        
        $('#modal_ajouter_condition_succes').modal('show');

        
        $("#modal_ajouter_condition_succes .moyenne").val(moyenne);
        $("#modal_ajouter_condition_succes .nom_niveau").val(nom_niveau);
        $("#modal_ajouter_condition_succes .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_ajouter_condition_succes .moyenne").val("");
        $("#modal_ajouter_condition_succes .nom_niveau").val("");
        $("#modal_ajouter_condition_succes .nom_sousetab").val("");

    });

    // $(".detail-condition-succes-link-td").click(function() {
     $("body").on("click", ".detail-condition-succes-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.nb_heures_max }}²²{{ cycl.sous_condition_succes }}²²{{ cycl.discipline }}"
        $('#modal_detail_condition_succes').modal('show');

        var discipline = $(this).parents("tr").attr('class');
        tab_element = discipline.split("²²");
        id = tab_element[0];
        moyenne = tab_element[1];
        nom_niveau = tab_element[2];
        nom_sousetab = tab_element[3];
      
        $("#modal_detail_condition_succes .moyenne").val(moyenne);
        $("#modal_detail_condition_succes .nom_niveau").val(nom_niveau);
        $("#modal_detail_condition_succes .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_detail_condition_succes .moyenne").attr("disabled", "True");
        $("#modal_detail_condition_succes .nom_niveau").attr("disabled", "True");
        $("#modal_detail_condition_succes .nom_sousetab").attr("disabled", "True");

    });


    $(".modifier-condition-succes-link").click(function() {
        $('#modal_modifier_condition_succes').modal('show');

        var discipline = $(this).parents("tr").attr('class');
        tab_element = discipline.split("²²");
        id = tab_element[0];
        moyenne = tab_element[1];
        nom_niveau = tab_element[2];
        nom_sousetab = tab_element[3];

        $("#modal_modifier_condition_succes .moyenne").val(moyenne);
        $("#modal_modifier_condition_succes .nom_niveau").val(nom_niveau);
        $("#modal_modifier_condition_succes .nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $("#modal_modifier_condition_succes .moyenne").removeAttr("disabled");
        $("#modal_modifier_condition_succes .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_condition_succes .nom_sousetab").removeAttr("disabled");

    });



    $(".supprimer-condition-succes-link").click(function() {

      $('#modal_supprimer_condition_succes').modal('show');

      var discipline = $(this).parents("tr").attr('class');
      tab_element = discipline.split("²²");
      id = tab_element[0];
      moyenne = tab_element[1];
      nom_niveau = tab_element[2];
      nom_sousetab = tab_element[3];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_condition_succes .moyenne").text(moyenne);
      $("#modal_supprimer_condition_succes .nom_niveau").text(nom_niveau);
      $("#modal_supprimer_condition_succes .nom_sousetab").text(nom_sousetab);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_condition_succes");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var discipline = String($(this).attr("class"));

              if(discipline.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (discipline.search("tri-desc") != -1){
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
      
    $("body").on("click", ".supprimer-condition-succes-link-ajax", function() {
        
        $('#modal_supprimer_condition_succes').modal('show');

         var discipline = $(this).parents("tr").attr('class');
          tab_element = discipline.split("²²");
          id = tab_element[0];
          moyenne = tab_element[1];
          nom_niveau = tab_element[2];
          nom_sousetab = tab_element[3];

          $("#id_supp").val(id);
          $("#modal_supprimer_condition_succes .moyenne").text(moyenne);
          $("#modal_supprimer_condition_succes .nom_niveau").text(nom_niveau);
          $("#modal_supprimer_condition_succes .nom_sousetab").text(nom_sousetab);

    });


    $("body").on("click", ".modifier-condition-succes-link-ajax", function() {
        
        $('#modal_modifier_condition_succes').modal('show');

        var discipline = $(this).parents("tr").attr('class');
        tab_element = discipline.split("²²");
        id = tab_element[0];
        moyenne = tab_element[1];
        nom_niveau = tab_element[2];
        nom_sousetab = tab_element[3];

        $("#modal_modifier_condition_succes .nom_niveau").val(nom_niveau);
        $("#modal_modifier_condition_succes .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_condition_succes .moyenne").val(moyenne);
        $("#id_modif").val(id);

        $("#modal_modifier_condition_succes .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_condition_succes .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_condition_succes .moyenne").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_condition_succes");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th span").each(function () {

                var discipline = String($(this).attr("class"));

                if(discipline.search("text-primary") != -1){

                    trier_par = $(this).parents("th").attr("class");

                    if (discipline.search("tri-desc") != -1){
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

        var form = $(".recherche_condition_succes");
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

        var form = $(".recherche_condition_succes");
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
