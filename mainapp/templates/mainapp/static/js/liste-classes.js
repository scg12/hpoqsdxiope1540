$(document).ready(function(){

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_classe");
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

          if(data.permissions.indexOf("classe") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_classes = data.classes;
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
                fin = data.classes.length;
              }

              if (liste_classes.length != 0){

                  for (var i = debut; i < fin; i++) {

                      nom_etab = liste_classes[i].nom_etab;
                      nom_sousetab = liste_classes[i].nom_sousetab                      
                      nom_niveau = liste_classes[i].nom_niveau;
                      nom_cycle = liste_classes[i].nom_cycle;
                      nom_classe = liste_classes[i].nom_classe;
                      id = liste_classes[i].id;
                      // alert(nom_etab, nom_sousetab, nom_classe, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ nom_classe +'²²'+ nom_niveau +'²²'+ nom_cycle + '²²'+ nom_sousetab +'²²'+ nom_etab +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-classe-link-td fix-col1">'+ nom_classe + '</td><td style="text-transform: uppercase;" class="detail-classe-link-td">'+ nom_niveau + '</td><td style="text-transform: uppercase;" class="detail-classe-link-td">'+ nom_cycle + '</td><td style="text-transform: capitalize;" class="detail-classe-link-td">' + nom_sousetab + '</td><td class="detail-classe-link-td">'+ nom_etab +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-classe-link-td btn" data-toggle="modal" data-target="#modal_detail_classe"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-classe-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-classe-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-classe-link");
                    // alert(data.permissions.indexOf("classes"));

                        index_model = data.permissions.indexOf("classe")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-classe-link").remove();
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
      $(".sidebar").addClass(sidebar_class);
      $(".btn").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
      $(".btn-rond").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);

      }

      function gererErreur(error) {
        $("#message").text(error);
        console.log(error);
      }


    $("body").on("click", ".ajouter-classe-link", function() {
        
        $('#modal_ajouter_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_classe = tab_element[1];
        nom_niveau = tab_element[2];
        nom_cycle = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];

        $(".nom_classe").val(nom_classe);
        $(".nom_niveau").val(nom_niveau);
        $(".nom_cycle").val(nom_cycle);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $(".nom_classe").val("");
        $(".nom_niveau").val("");
        $(".nom_cycle").val("");
        $(".nom_sousetab").val("");
        $(".nom_etab").val("");

    });

    // $(".detail-classe-link-td").click(function() {
     $("body").on("click", ".detail-classe-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.nom_classe }}²²{{ cycl.sous_classe }}²²{{ cycl.classe }}"
        $('#modal_detail_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_classe = tab_element[1];
        nom_niveau = tab_element[2];
        nom_cycle = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];
      
        $(".nom_classe").val(nom_classe);
        $(".nom_niveau").val(nom_niveau);
        $(".nom_cycle").val(nom_cycle);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $(".nom_classe").attr("disabled", "True");
        $(".nom_niveau").attr("disabled", "True");
        $(".nom_cycle").attr("disabled", "True");
        $(".nom_sousetab").attr("disabled", "True");
        $(".nom_etab").attr("disabled", "True");

    });


    $(".modifier-classe-link").click(function() {
        $('#modal_modifier_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_classe = tab_element[1];
        nom_niveau = tab_element[2];
        nom_cycle = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];

        $("#modal_modifier_classe .nom_classe").val(nom_classe);
        $("#modal_modifier_classe .nom_niveau").val(nom_niveau);
        $("#modal_modifier_classe .nom_cycle").val(nom_cycle);
        $("#modal_modifier_classe .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_classe .nom_etab").val(nom_etab);
        $("#id_modif").val(id);

        $("#modal_modifier_classe .nom_classe").removeAttr("disabled");
        $("#modal_modifier_classe .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_classe .nom_cycle").removeAttr("disabled");
        $("#modal_modifier_classe .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_classe .nom_etab").removeAttr("disabled");

    });



    $(".supprimer-classe-link").click(function() {

      $('#modal_supprimer_classe').modal('show');

      var classe = $(this).parents("tr").attr('class');
      tab_element = classe.split("²²");
      id = tab_element[0];
      nom_classe = tab_element[1];
      nom_niveau = tab_element[2];
      nom_cycle = tab_element[3];
      nom_sousetab = tab_element[4];
      nom_etab = tab_element[5];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_classe .nom_classe").text(nom_classe);
      $("#modal_supprimer_classe .nom_niveau").text(nom_niveau);
      $("#modal_supprimer_classe .nom_cycle").text(nom_cycle);
      $("#modal_supprimer_classe .nom_sousetab").text(nom_sousetab);
      $("#modal_supprimer_classe .nom_etab").text(nom_etab);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_classe");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var classe = String($(this).attr("class"));

              if(classe.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (classe.search("tri-desc") != -1){
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
      
    $("body").on("click", ".supprimer-classe-link-ajax", function() {
        
        $('#modal_supprimer_classe').modal('show');

         var classe = $(this).parents("tr").attr('class');
          tab_element = classe.split("²²");
          id = tab_element[0];
          nom_classe = tab_element[1];
          nom_niveau = tab_element[2];
          nom_cycle = tab_element[3];
          nom_sousetab = tab_element[4];
          nom_etab = tab_element[5];

          
          $("#id_supp").val(id);
          $("#modal_supprimer_classe .nom_classe").text(nom_classe);
          $("#modal_supprimer_classe .nom_niveau").text(nom_niveau);
          $("#modal_supprimer_classe .nom_cycle").text(nom_cycle);
          $("#modal_supprimer_classe .nom_sousetab").text(nom_sousetab);
          $("#modal_supprimer_classe .nom_etab").text(nom_etab);

    });


    $("body").on("click", ".modifier-classe-link-ajax", function() {
        
        $('#modal_modifier_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_classe = tab_element[1];
        nom_niveau = tab_element[2];
        nom_cycle = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];


        $("#modal_modifier_classe .nom_etab").val(nom_etab);
        $("#modal_modifier_classe .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_classe .nom_cycle").val(nom_cycle);
        $("#modal_modifier_classe .nom_niveau").val(nom_niveau);
        $("#modal_modifier_classe .nom_classe").val(nom_classe);
        $("#id_modif").val(id);

        $("#modal_modifier_classe .nom_etab").removeAttr("disabled");
        $("#modal_modifier_classe .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_classe .nom_classe").removeAttr("disabled");
        $("#modal_modifier_classe .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_classe .nom_cycle").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_classe");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th").each(function () {

                var classe = String($(this).attr("class"));

                if(classe.search("active") != -1){

                    trier_par = $(this).attr("class").split(" ")[0];

                    if (classe.search("tri-desc") != -1){
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

        var form = $(".recherche_classe");
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

        var form = $(".recherche_classe");
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
