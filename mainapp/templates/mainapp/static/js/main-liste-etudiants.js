$(document).ready(function(){

/*    $("table tr .supprimer-eleve-link").click(function() {
        alert("889812");
        $('#supprimer-eleve-link2').modal('show');
        $('#modal_supprimer_eleve2 .matricule2').text('show');
    
    });*/
        //$('#modal_supprimer_eleve2').modal('show');
       // $('#modal_supprimer_eleve2 .matricule2').text('show');

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_etudiant");
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

          if(data.permissions.indexOf("eleve") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_etudiants = data.etudiants;
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
                fin = data.etudiants.length;
              }

              if (liste_etudiants.length != 0){

                  for (var i = debut; i < fin; i++) {
                      id = liste_etudiants[i].id;
                      matricule = liste_etudiants[i].matricule;
                      nom = liste_etudiants[i].nom;
                      prenom = liste_etudiants[i].prenom;
                      age = liste_etudiants[i].age;
                      

                    nouvelle_ligne = "<tr class='"+ id+'²²'+ matricule+ '²²'+ nom +'²²'+ prenom +'²²' + age +"'>" + '<th scope="row">'+ (i+1) +
                    '</th><td><img src="/static/assets/img/faces/avatar.jpg" width="25px" height="25px"></td><td style="text-transform: uppercase;">'+ matricule + '</td><td style="text-transform: uppercase;">' + nom + '</td><td style="text-transform: capitalize;">' + prenom + '</td><td>'+ age +'</td>' + '<td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="btn detail-eleve-link-ajax" data-toggle="modal" data-target="#modal_detail_eleve"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="btn modifier-eleve-link-ajax"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="btn btn-danger supprimer-eleve-link-ajax"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-eleve-link");
                    // alert(data.permissions.indexOf("etudiants"));

                        index_model = data.permissions.indexOf("eleve")
                        if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        }                      
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-eleve-link").remove();
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




    $(".ajouter-eleve-link").click(function() {

        $('#modal_ajouter_eleve').modal('show');

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

        $(".matricule").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".age").val("");

    });

    $("body").on("click", ".ajouter-eleve-link", function() {
        
        $('#modal_ajouter_eleve').modal('show');

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

        $(".matricule").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".age").val("");

    });

    $(".detail-eleve-link-td").click(function() {

        $('#modal_detail_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".age").val(age);

        $(".matricule").attr("disabled", "True");
        $(".nom").attr("disabled", "True");
        $(".prenom").attr("disabled", "True");
        $(".age").attr("disabled", "True");

    });


    $(".modifier-eleve-link").click(function() {

        $('#modal_modifier_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".age").val(age);
        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

    });



    $(".supprimer-eleve-link").click(function() {

      $('#modal_supprimer_eleve').modal('show');

      var classe = $(this).parents("tr").attr('class');
      tab_element = classe.split("²²");
      id = tab_element[0];
      matricule = tab_element[1];
      nom = tab_element[2];
      prenom = tab_element[3];
      age = tab_element[4];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_eleve .matricule").text(matricule);
      $("#modal_supprimer_eleve .nom").text(nom);
      $("#modal_supprimer_eleve .prenom").text(prenom);
      $("#modal_supprimer_eleve .age").text(age);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_etudiant");
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
      
    $("body").on("click", ".supprimer-eleve-link-ajax", function() {
        
        $('#modal_supprimer_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];
        
        $("#id_supp").val(id);
        $("#modal_supprimer_eleve .matricule").text(matricule);
        $("#modal_supprimer_eleve .nom").text(nom);
        $("#modal_supprimer_eleve .prenom").text(prenom);
        $("#modal_supprimer_eleve .age").text(age);

    });


    $("body").on("click", ".modifier-eleve-link-ajax", function() {
        
        $('#modal_modifier_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".age").val(age);
        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

    });


      
    $("body").on("click", ".detail-eleve-link-ajax", function() {
        
        $('#modal_detail_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".age").val(age);

        $(".matricule").attr("disabled", "True");
        $(".nom").attr("disabled", "True");
        $(".prenom").attr("disabled", "True");
        $(".age").attr("disabled", "True");

    });




    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_etudiant");
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

        var form = $(".recherche_etudiant");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class");

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

        var form = $(".recherche_etudiant");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class")

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
