$(document).ready(function(){

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_specialite");
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

          if(data.permissions.indexOf("specialite") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_specialites = data.specialites;
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
                fin = data.specialites.length;
              }

              if (liste_specialites.length != 0){

                  for (var i = debut; i < fin; i++) {

                      id_sousetab = liste_specialites[i].id_sousetab;
                      id_etab = liste_specialites[i].id_etab                      
                      nom_sousetab = liste_specialites[i].nom_sousetab;
                      nom_etab = liste_specialites[i].nom_etab;
                      specialite = liste_specialites[i].specialite;
                      id = liste_specialites[i].id;
                      // alert(id_sousetab, id_etab, specialite, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ specialite +'²²'+ nom_sousetab +'²²'+ nom_etab +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-specialite-link-td fix-col1">'+ specialite + '</td><td style="text-transform: uppercase;" class="detail-specialite-link-td">'+ nom_sousetab + '</td><td style="text-transform: uppercase;" class="detail-specialite-link-td">'+ nom_etab + '</td>' + '<td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-specialite-link-td btn" data-toggle="modal" data-target="#modal_detail_specialite"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-specialite-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-specialite-link");
                    // alert(data.permissions.indexOf("specialites"));

                        index_model = data.permissions.indexOf("specialite")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-specialite-link").remove();
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

                resultat_pagination += '<span class="pagination-element" id="1">PREMIER </span>';


                if(possede_page_precedente == true){
                  resultat_pagination += '<span class="pagination-element" id="'+precedent +'">PREC </span>';
                }else{
                  resultat_pagination += '<span class="pagination-element-inactive">PREC </span>';
                }

                for (var num_page= 0; num_page < liste_page.length; num_page++) {

                    if (liste_page[num_page] == numero_page_active){
                     
                      resultat_pagination +='<button class="cursus-btn-pagination pagination-element pagination-element-on" id="'+liste_page[num_page]+'">'+ liste_page[num_page]+'</button>';
                    
                    }else{
                      
                      resultat_pagination +='<button class="cursus-btn-pagination-off pagination-element" id="'+ liste_page[num_page] +'">'+ liste_page[num_page]+'</button>';
                      
                    }
                  
                }

                if(possede_page_suivante == true){
                  resultat_pagination += '<span class="pagination-element" id="'+ suivant +'">SUIV</span>'
                }else{
                  resultat_pagination += '<span class="pagination-element-inactive">SUIV</span>'
                }
                
                resultat_pagination += '<span class="pagination-element" id="'+ liste_page.length +'"> DERNIER </span>';

                resultat_pagination += '</div>';

                $(".pagination").append(resultat_pagination);

                $(".first_item_page").text(data.first_item_page);
                $(".last_item_page").text(data.last_item_page);
                $(".nbre_item").text(data.nbre_item);
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
      // $(".sidebar").addClass(sidebar_class);
      $(".btn").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
      $(".btn-rond").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
      $(".cursus-btn-pagination").removeClass("orange vert violet bleu rose jaune turquoise").addClass(theme_class);

      }

      function gererErreur(error) {
        $("#message").text(error);
        console.log(error);
      }


    $("body").on("click", ".ajouter-specialite-link", function() {
        
        $('#modal_ajouter_specialite').modal('show');

        var specialite = $(this).parents("tr").attr('class');
        tab_element = specialite.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        nom_sousetab = tab_element[2];
        nom_etab = tab_element[3];

        $(".specialite").val(specialite);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $(".specialite").val("");
        $(".nom_sousetab").val("");
        $(".nom_etab").val("");

    });

    // $(".detail-specialite-link-td").click(function() {
     $("body").on("click", ".detail-specialite-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.specialite }}²²{{ cycl.sous_specialite }}²²{{ cycl.specialite }}"
        $('#modal_detail_specialite').modal('show');

        var specialite = $(this).parents("tr").attr('class');
        tab_element = specialite.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        nom_sousetab = tab_element[2];
        nom_etab = tab_element[3];
      
        $(".specialite").val(specialite);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $(".specialite").attr("disabled", "True");
        $(".nom_sousetab").attr("disabled", "True");
        $(".nom_etab").attr("disabled", "True");

    });


    $(".modifier-specialite-link").click(function() {
        $('#modal_modifier_specialite').modal('show');

        var specialite = $(this).parents("tr").attr('class');
        tab_element = specialite.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        nom_sousetab = tab_element[2];
        nom_etab = tab_element[3];

        $("#modal_modifier_specialite .specialite").val(specialite);
        $("#modal_modifier_specialite .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_specialite .nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $("#modal_modifier_specialite .specialite").removeAttr("disabled");
        $("#modal_modifier_specialite .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_specialite .nom_etab").removeAttr("disabled");

    });



    $(".supprimer-specialite-link").click(function() {

      $('#modal_supprimer_specialite').modal('show');

      var specialite = $(this).parents("tr").attr('class');
      tab_element = specialite.split("²²");
      id = tab_element[0];
      specialite = tab_element[1];
      nom_sousetab = tab_element[2];
      nom_etab = tab_element[3];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_specialite .specialite").text(specialite);
      $("#modal_supprimer_specialite .nom_sousetab").text(nom_sousetab);
      $("#modal_supprimer_specialite .nom_etab").text(nom_etab);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_specialite");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var specialite = String($(this).attr("class"));

              if(specialite.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (specialite.search("tri-desc") != -1){
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
      
    $("body").on("click", ".supprimer-specialite-link-ajax", function() {
        
        $('#modal_supprimer_specialite').modal('show');

         var specialite = $(this).parents("tr").attr('class');
          tab_element = specialite.split("²²");
          id = tab_element[0];
          specialite = tab_element[1];
          nom_sousetab = tab_element[2];
          nom_etab = tab_element[3];

          
          $("#id_supp").val(id);
          $("#modal_supprimer_specialite .specialite").text(specialite);
          $("#modal_supprimer_specialite .nom_sousetab").text(nom_sousetab);
          $("#modal_supprimer_specialite .nom_etab").text(nom_etab);

    });


    $("body").on("click", ".modifier-specialite-link-ajax", function() {
        
        $('#modal_modifier_specialite').modal('show');

        var specialite = $(this).parents("tr").attr('class');
        tab_element = specialite.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        nom_sousetab = tab_element[2];
        nom_etab = tab_element[3];

        $("#modal_modifier_specialite .nom_etab").val(nom_etab);
        $("#modal_modifier_specialite .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_specialite .specialite").val(specialite);
        $("#id_modif").val(id);
        
        $("#modal_modifier_specialite .specialite").removeAttr("disabled");
        $("#modal_modifier_specialite .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_specialite .nom_etab").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_specialite");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th").each(function () {

                var specialite = String($(this).attr("class"));

                if(specialite.search("active") != -1){

                    trier_par = $(this).attr("class").split(" ")[0];

                    if (specialite.search("tri-desc") != -1){
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

        var form = $(".recherche_specialite");
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

        var form = $(".recherche_specialite");
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
