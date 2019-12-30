$(document).ready(function(){

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_paiement");
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

          if(data.permissions.indexOf("typepayementadminstaff") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_paiements = data.paiements;
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
                fin = data.paiements.length;
              }

              if (liste_paiements.length != 0){

                  for (var i = debut; i < fin; i++) {

                      libelle = liste_paiements[i].libelle;
                      date_deb = liste_paiements[i].date_deb;
                      date_fin = liste_paiements[i].date_fin;
                      entree_sortie_caisee = liste_paiements[i].entree_sortie_caisee;
                      date_fin = liste_paiements[i].date_fin                                          
                      id = liste_paiements[i].id;
                      // alert(nom_etab, classe, libelle, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ libelle +'²²'+ date_deb +'²²'+ date_fin +'²²'+ entree_sortie_caisee +'²²'+"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-paiement-link-td fix-col1">'+ libelle + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ date_deb + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ date_fin + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ entree_sortie_caisee +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-paiement-link-td btn" data-toggle="modal" data-target="#modal_detail_paiement"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-paiement-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-paiement-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-paiement-link");
                    // alert(data.permissions.indexOf("paiements"));

                        index_model = data.permissions.indexOf("typepayementadminstaff")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-paiement-link").remove();
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


    $("body").on("click", ".ajouter-paiement-link", function() {
        
        $('#modal_ajouter_paiement').modal('show');

        // $("#modal_ajouter_paiement .libelle").val(libelle);
        // $("#modal_ajouter_paiement .date_deb").val(date_deb);
        // $("#modal_ajouter_paiement .date_fin").val(date_fin);
        // $("#modal_ajouter_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        // $("#modal_ajouter_paiement .montant").val(montant);
        // $("#id_modif").val(id);

        $("#modal_ajouter_paiement .libelle").val("");
        $("#modal_ajouter_paiement .date_deb").val("");
        $("#modal_ajouter_paiement .date_fin").val("");
        $("#modal_ajouter_paiement .entree_sortie_caisee").val("");
        $("#modal_ajouter_paiement .montant").val("");

    });

    // $(".detail-paiement-link-td").click(function() {
     $("body").on("click", ".detail-paiement-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.libelle }}²²{{ cycl.sous_paiement }}²²{{ cycl.paiement }}"
        $('#modal_detail_paiement').modal('show');

        var paiement = $(this).parents("tr").attr('class');
        tab_element = paiement.split("²²");
        id = tab_element[0];
        libelle = tab_element[1];
        date_deb = tab_element[2];
        date_fin = tab_element[3];
        entree_sortie_caisee = tab_element[4];
        montant = parseFloat(tab_element[5]);
      
        $("#modal_detail_paiement .libelle").val(libelle);
        $("#modal_detail_paiement .date_deb").val(date_deb);
        $("#modal_detail_paiement .date_fin").val(date_fin);
        $("#modal_detail_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_detail_paiement .montant").val(montant);
        $("#id_modif").val(id);

        $("#modal_detail_paiement .libelle").attr("disabled", "True");
        $("#modal_detail_paiement .date_deb").attr("disabled", "True");
        $("#modal_detail_paiement .date_fin").attr("disabled", "True");
        $("#modal_detail_paiement .entree_sortie_caisee").attr("disabled", "True");
        $("#modal_detail_paiement .montant").attr("disabled", "True");

    });


    $(".modifier-paiement-link").click(function() {
        $('#modal_modifier_paiement').modal('show');

        var paiement = $(this).parents("tr").attr('class');
        tab_element = paiement.split("²²");
        id = tab_element[0];
        libelle = tab_element[1];
        date_deb = tab_element[2];
        date_fin = tab_element[3];
        entree_sortie_caisee = tab_element[4];
        montant = parseFloat(tab_element[5]);

        $("#modal_modifier_paiement .libelle").val(libelle);
        $("#modal_modifier_paiement .date_deb").val(date_deb);
        $("#modal_modifier_paiement .date_fin").val(date_fin);
        $("#modal_modifier_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_modifier_paiement .montant").val(montant);
        $("#id_modif").val(id);

        $("#modal_modifier_paiement .libelle").removeAttr("disabled");
        $("#modal_modifier_paiement .date_deb").removeAttr("disabled");
        $("#modal_modifier_paiement .date_fin").removeAttr("disabled");
        $("#modal_modifier_paiement .entree_sortie_caisee").removeAttr("disabled");
        $("#modal_modifier_paiement .montant").removeAttr("disabled");

    });



    $(".supprimer-paiement-link").click(function() {

      $('#modal_supprimer_paiement').modal('show');

      var paiement = $(this).parents("tr").attr('class');
      tab_element = paiement.split("²²");
      id = tab_element[0];
      libelle = tab_element[1];
      date_deb = tab_element[2];
      date_fin = tab_element[3];
      entree_sortie_caisee = tab_element[4];
      montant = parseFloat(tab_element[5]);
      
      $("#id_supp").val(id);
      $("#modal_supprimer_paiement .libelle").text(libelle);
      $("#modal_supprimer_paiement .date_deb").text(date_deb);
      $("#modal_supprimer_paiement .date_fin").text(date_fin);
      $("#modal_supprimer_paiement .entree_sortie_caisee").text(entree_sortie_caisee);
      $("#modal_supprimer_paiement .montant").text(montant);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_paiement");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var paiement = String($(this).attr("class"));

              if(paiement.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (paiement.search("tri-desc") != -1){
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
      
    $("body").on("click", ".supprimer-paiement-link-ajax", function() {
        
        $('#modal_supprimer_paiement').modal('show');

         var paiement = $(this).parents("tr").attr('class');
          tab_element = paiement.split("²²");
          id = tab_element[0];
          libelle = tab_element[1];
          date_deb = tab_element[2];
          date_fin = tab_element[3];
          entree_sortie_caisee = tab_element[4];
          montant = parseFloat(tab_element[5]);

          $("#id_supp").val(id);
          $("#modal_supprimer_paiement .libelle").text(libelle);
          $("#modal_supprimer_paiement .date_deb").text(date_deb);
          $("#modal_supprimer_paiement .date_fin").text(date_fin);
          $("#modal_supprimer_paiement .entree_sortie_caisee").text(entree_sortie_caisee);
          $("#modal_supprimer_paiement .montant").text(montant);

    });


    $("body").on("click", ".modifier-paiement-link-ajax", function() {
        
        $('#modal_modifier_paiement').modal('show');

        var paiement = $(this).parents("tr").attr('class');
        tab_element = paiement.split("²²");
        id = tab_element[0];
        libelle = tab_element[1];
        date_deb = tab_element[2];
        date_fin = tab_element[3];
        entree_sortie_caisee = tab_element[4];
        montant = parseFloat(tab_element[5]);

        $("#modal_modifier_paiement .montant").val(montant);
        $("#modal_modifier_paiement .date_deb").val(date_deb);
        $("#modal_modifier_paiement .libelle").val(libelle);
        $("#modal_modifier_paiement .date_fin").val(date_fin);
        $("#modal_modifier_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#id_modif").val(id);

        $("#modal_modifier_paiement .montant").removeAttr("disabled");
        $("#modal_modifier_paiement .libelle").removeAttr("disabled");
        $("#modal_modifier_paiement .date_fin").removeAttr("disabled");
        $("#modal_modifier_paiement .entree_sortie_caisee").removeAttr("disabled");
        $("#modal_modifier_paiement .date_deb").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_paiement");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th span").each(function () {

                var paiement = String($(this).attr("class"));

                if(paiement.search("text-primary") != -1){

                    trier_par = $(this).parents("th").attr("class");

                    if (paiement.search("tri-desc") != -1){
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

        var form = $(".recherche_paiement");
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

        var form = $(".recherche_paiement");
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
