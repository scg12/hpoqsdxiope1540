$(document).ready(function(){

/*  document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
});*/


/*    $("table tr .supprimer-sousetab-link").click(function() {
        alert("889812");
        $('#supprimer-sousetab-link2').modal('show');
        $('#modal_supprimer_sousetab2 .matricule2').text('show');
    
    });*/
        //$('#modal_supprimer_sousetab2').modal('show');
       // $('#modal_supprimer_sousetab2 .matricule2').text('show');

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_sous_etablissement");
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

          if(data.permissions.indexOf("sousetab") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_sous_etablissements = data.s_etablissements;
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
                fin = data.s_etablissements.length;
              }

              if (liste_sous_etablissements.length != 0){

                  for (var i = debut; i < fin; i++) {

                      id = liste_sous_etablissements[i].id;
                      nom_sousetab = liste_sous_etablissements[i].nom_sousetab;
                      date_creation = liste_sous_etablissements[i].date_creation;
                      nom_fondateur = liste_sous_etablissements[i].nom_fondateur;
                      localisation = liste_sous_etablissements[i].localisation;
                      // alert(nom_sousetab+" "+date_creation+" "+nom_fondateur+" "+localisation);
                      

                    nouvelle_ligne = "<tr class='"+ id+'²²'+ nom_sousetab+ '²²'+ date_creation +'²²'+ nom_fondateur +'²²' + localisation +"'>" + '<th class="fix-col" scope="row">'+ (i+1) +
                    '</th><td class="nom_sousetab fix-col1" style="text-transform: uppercase;">'+ nom_sousetab + '</td><td style="text-transform: uppercase;">' + date_creation + '</td><td style="text-transform: capitalize;">' + nom_fondateur + '</td><td>'+ localisation +'</td>' + '<td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="btn detail-sousetab-link-ajax" data-toggle="modal" data-target="#modal_detail_sousetab"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="btn modifier-sousetab-link-ajax"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="btn btn-danger supprimer-sousetab-link-ajax"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-sousetab-link");
                    // alert(data.permissions.indexOf("etablissements"));

                        index_model = data.permissions.indexOf("sousetab")
                       /* if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-sousetab-link").remove();
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



    $("body").on("click", ".ajouter-sousetab-link", function() {
        
        $('#modal_ajouter_sousetab').modal('show');

        $("#modal_ajouter_sousetab .nom_sousetab").removeAttr("disabled");
        $("#modal_ajouter_sousetab .date_creation").removeAttr("disabled");
        $("#modal_ajouter_sousetab .nom_fondateur").removeAttr("disabled");
        $("#modal_ajouter_sousetab .localisation").removeAttr("disabled");

        $("#modal_ajouter_sousetab .nom_sousetab").val("");
        $("#modal_ajouter_sousetab .date_creation").val("");
        $("#modal_ajouter_sousetab .nom_fondateur").val("");
        $("#modal_ajouter_sousetab .localisation").val("");

    });

    $(".detail-sousetab-link-td").click(function() {

        $('#modal_detail_sousetab').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        date_creation = tab_element[2];
        nom_fondateur = tab_element[3];
        localisation = tab_element[4];

        $("#modal_detail_sousetab .nom_sousetab").val(nom_sousetab);
        $("#modal_detail_sousetab .date_creation").val(date_creation);
        $("#modal_detail_sousetab .nom_fondateur").val(nom_fondateur);
        $("#modal_detail_sousetab .localisation").val(localisation);

        $("#modal_detail_sousetab .nom_sousetab").attr("disabled", "True");
        $("#modal_detail_sousetab .date_creation").attr("disabled", "True");
        $("#modal_detail_sousetab .nom_fondateur").attr("disabled", "True");
        $("#modal_detail_sousetab .localisation").attr("disabled", "True");

    });


    $(".modifier-sousetab-link").click(function() {

        $('#modal_modifier_sousetab').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        date_creation = tab_element[2];
        nom_fondateur = tab_element[3];
        localisation = tab_element[4];

        $("#modal_modifier_sousetab .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_sousetab .date_creation").val(date_creation);
        $("#modal_modifier_sousetab .nom_fondateur").val(nom_fondateur);
        $("#modal_modifier_sousetab .localisation").val(localisation);
        $("#id_modif").val(id);

        $("#modal_modifier_sousetab .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_sousetab .date_creation").removeAttr("disabled");
        $("#modal_modifier_sousetab .nom_fondateur").removeAttr("disabled");
        $("#modal_modifier_sousetab .localisation").removeAttr("disabled");

    });



    $(".supprimer-sousetab-link").click(function() {

      $('#modal_supprimer_sousetab').modal('show');

      var classe = $(this).parents("tr").attr('class');
      tab_element = classe.split("²²");
      id = tab_element[0];
      nom_sousetab = tab_element[1];
      date_creation = tab_element[2];
      nom_fondateur = tab_element[3];
      localisation = tab_element[4];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_sousetab .nom_sousetab").text(nom_sousetab);
      $("#modal_supprimer_sousetab .date_creation").text(date_creation);
      $("#modal_supprimer_sousetab .nom_fondateur").text(nom_fondateur);
      $("#modal_supprimer_sousetab .localisation").text(localisation);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_sous_etablissement");
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
      
    $("body").on("click", ".supprimer-sousetab-link-ajax", function() {
        
        $('#modal_supprimer_sousetab').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];
        
        $("#id_supp").val(id);
        $("#modal_supprimer_sousetab .matricule").text(matricule);
        $("#modal_supprimer_sousetab .nom").text(nom);
        $("#modal_supprimer_sousetab .prenom").text(prenom);
        $("#modal_supprimer_sousetab .age").text(age);

    });


    $("body").on("click", ".modifier-sousetab-link-ajax", function() {
        
        $('#modal_modifier_sousetab').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        date_creation = tab_element[2];
        nom_fondateur = tab_element[3];
        localisation = tab_element[4];

        $(".nom_sousetab").val(nom_sousetab);
        $(".date_creation").val(date_creation);
        $(".nom_fondateur").val(nom_fondateur);
        $(".localisation").val(localisation);
        $("#id_modif").val(id);

        $(".nom_sousetab").removeAttr("disabled");
        $(".date_creation").removeAttr("disabled");
        $(".nom_fondateur").removeAttr("disabled");
        $(".localisation").removeAttr("disabled");

    });


      
    $("body").on("click", ".detail-sousetab-link-ajax", function() {
        
        $('#modal_detail_sousetab').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        date_creation = tab_element[2];
        nom_fondateur = tab_element[3];
        localisation = tab_element[4];

        $(".nom_sousetab").val(nom_sousetab);
        $(".date_creation").val(date_creation);
        $(".nom_fondateur").val(nom_fondateur);
        $(".localisation").val(localisation);

        $(".nom_sousetab").attr("disabled", "True");
        $(".date_creation").attr("disabled", "True");
        $(".nom_fondateur").attr("disabled", "True");
        $(".localisation").attr("disabled", "True");

    });




    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_sous_etablissement");
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

  //$('table th').click(function(e){e.preventDefault();}).click();


   $("body").on("click", ".tri-asc", function(e) {

        e.stopImmediatePropagation();

        $(".tri").find("img").attr("src", "/static/images/arrow.png");
        $(this).find("img").attr("src", "/static/images/up.png");

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " ";

        var form = $(".recherche_sous_etablissement");
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

        var form = $(".recherche_sous_etablissement");
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
