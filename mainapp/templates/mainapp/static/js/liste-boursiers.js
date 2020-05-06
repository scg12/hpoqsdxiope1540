$(document).ready(function(){

/*    $("table tr .supprimer-bourse-link").click(function() {
        alert("889812");
        $('#supprimer-bourse-link2').modal('show');
        $('#modal_supprimer_bourse2 .matricule2').text('show');
    
    });*/
        //$('#modal_supprimer_bourse2').modal('show');
       // $('#modal_supprimer_bourse2 .matricule2').text('show');

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_bourse");
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

          if(data.permissions.indexOf("typepayementeleve") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_bourses = data.bourses;
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
                fin = data.bourses.length;
              }
              i = 0;
              if (liste_bourses.length != 0){

                  // for (var i = debut; i < fin; i++) {
                    liste_bourses.forEach( function(element, index){
                      console.log(element);
                      matricule = element.matricule;
                      nom = element.nom                      
                      prenom = element.prenom;
                      sexe = element.sexe;
                      classe_actuelle = element.classe_actuelle;
                      liste_bourses_afficher = element.liste_bourses_afficher;
                      liste_bourses = element.liste_bourses;
                      id = element.id;
                      // alert(nom_etab, nom_sousetab, nom_bourse, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ matricule +'²²'+ nom+ '²²'+ prenom +'²²'+ sexe +'²²'+ classe_actuelle +'²²'+ liste_bourses_afficher +'²²'+ liste_bourses +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-bourse-link-td fix-col1">'+ matricule + '</td><td style="text-transform: capitalize;" class="detail-bourse-link-td">' + nom + '</td><td class="detail-bourse-link-td">'+ prenom + '</td><td style="text-transform: capitalize;" class="detail-bourse-link-td">' + sexe + '</td><td style="text-transform: capitalize;" class="detail-bourse-link-td">' + classe_actuelle + '</td><td style="text-transform: capitalize;" class="detail-bourse-link-td">' + liste_bourses_afficher.trunc(20) +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-bourse-link-td btn" data-toggle="modal" data-target="#modal_detail_bourse"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-bourse-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-bourse-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-bourse-link");
                    // alert(data.permissions.indexOf("bourses"));

                        index_model = data.permissions.indexOf("typepayementeleve")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-bourse-link").remove();
                        }                      
                        if(data.permissions[index_model + 4] ==1 ){
                          nouvelle_ligne += del;
                        }

                        $("table tbody").append(nouvelle_ligne);
                      i++;
                  });

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

      /*Fonction qui permet de truncate le texte en js du genre bonjour...*/
   String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '&hellip;' : this;
      };


/*

    $(".ajouter-bourse-link").click(function() {

        $('#modal_ajouter_bourse').modal('show');

        $(".nom_bourse").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

        $(".nom_bourse").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".age").val("");

    });*/

    $("body").on("click", ".ajouter-bourse-link", function() {
        
        $('#modal_ajouter_bourse').modal('show');

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".classe_actuelle").val(classe_actuelle);
        $(".liste_bourses_afficher").val(liste_bourses_afficher);
        $("#id_modif").val(id);

        $(".matricule").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".sexe").val("");
        $(".classe_actuelle").val("");
        $(".liste_bourses_afficher").val("");

    });


     $("body").on("click", ".detail-bourse-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.nom_bourse }}²²{{ cycl.sous_bourse }}²²{{ cycl.bourse }}"
        $('#modal_detail_bourse').modal('show');

        var classe_actuelle = $(this).parents("tr").attr('class');
        tab_element = classe_actuelle.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[4];
        sexe = tab_element[5];
        classe_actuelle = tab_element[6];
        liste_bourses_afficher = tab_element[7];
      
        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".classe_actuelle").val(classe_actuelle);
        $(".liste_bourses_afficher").val(liste_bourses_afficher);
        $("#id_modif").val(id);

        $(".matricule").attr("disabled", "True");
        $(".nom").attr("disabled", "True");
        $(".prenom").attr("disabled", "True");
        $(".sexe").attr("disabled", "True");
        $(".classe_actuelle").attr("disabled", "True");
        $(".liste_bourses_afficher").attr("disabled", "True");


    });


    $(".modifier-bourse-link").click(function() {
        $('#modal_modifier_bourse').modal('show');

        var classe_actuelle = $(this).parents("tr").attr('class');
        tab_element = classe_actuelle.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[4];
        sexe = tab_element[5];
        classe_actuelle = tab_element[6];
        liste_bourses_afficher = tab_element[7];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".classe_actuelle").val(classe_actuelle);
        $(".liste_bourses_afficher").val(liste_bourses_afficher);
        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".sexe").removeAttr("disabled");
        $(".classe_actuelle").removeAttr("disabled");
        $(".liste_bourses_afficher").removeAttr("disabled");

    });



    $(".supprimer-bourse-link").click(function() {

      $('#modal_supprimer_bourse').modal('show');

      var classe_actuelle = $(this).parents("tr").attr('class');
      tab_element = classe_actuelle.split("²²");
      id = tab_element[0];
      matricule = tab_element[1];
      nom = tab_element[2];
      prenom = tab_element[4];
      sexe = tab_element[5];
      classe_actuelle = tab_element[6];
      liste_bourses_afficher = tab_element[7];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_bourse .matricule").text(matricule);
      $("#modal_supprimer_bourse .nom").text(nom);
      $("#modal_supprimer_bourse .prenom").text(prenom);
      $("#modal_supprimer_bourse .sexe").text(sexe);
      $("#modal_supprimer_bourse .classe_actuelle").text(classe_actuelle);
      $("#modal_supprimer_bourse .liste_bourses_afficher").text(liste_bourses_afficher);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_bourse");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        $("body table thead th span").each(function () {

              var classe_actuelle = String($(this).attr("class"));

              if(classe_actuelle.search("text-primary") != -1){

                  trier_par = $(this).parents("th").attr("class");

                  if (classe_actuelle.search("tri-desc") != -1){
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
      
    $("body").on("click", ".supprimer-bourse-link-ajax", function() {
        
        $('#modal_supprimer_bourse').modal('show');

         var classe_actuelle = $(this).parents("tr").attr('class');
          tab_element = classe_actuelle.split("²²");
          id = tab_element[0];
          matricule = tab_element[1];
          nom = tab_element[2];
          prenom = tab_element[4];
          sexe = tab_element[5];
          classe_actuelle = tab_element[6];
          liste_bourses_afficher = tab_element[7];
          
          $("#id_supp").val(id);
          $("#modal_supprimer_bourse .matricule").text(matricule);
          $("#modal_supprimer_bourse .nom").text(nom);
          $("#modal_supprimer_bourse .prenom").text(prenom);
          $("#modal_supprimer_bourse .sexe").text(sexe);
          $("#modal_supprimer_bourse .classe_actuelle").text(classe_actuelle);
          $("#modal_supprimer_bourse .liste_bourses_afficher").text(liste_bourses_afficher);

    });


    $("body").on("click", ".modifier-bourse-link-ajax", function() {
        
        $('#modal_modifier_bourse').modal('show');

        var classe_actuelle = $(this).parents("tr").attr('class');
        tab_element = classe_actuelle.split("²²");

        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[4];
        sexe = tab_element[5];
        classe_actuelle = tab_element[6];
        liste_bourses_afficher = tab_element[7];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".classe_actuelle").val(classe_actuelle);
        $(".liste_bourses_afficher").val(liste_bourses_afficher);

        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".sexe").removeAttr("disabled");
        $(".classe_actuelle").removeAttr("disabled");
        $(".liste_bourses_afficher").removeAttr("disabled");

    });


      
  /*  $("body").on("click", ".detail-bourse-link-ajax", function() {
        $('#modal_detail_bourse').modal('show');

        var classe_actuelle = $(this).parents("tr").attr('class');
        tab_element = classe_actuelle.split("²²");
        id = tab_element[0];
        nom_bourse = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        age = tab_element[4];
        bp = tab_element[5];
        email = tab_element[6];
        tel = tab_element[7];
        devise = tab_element[8];
        langue = tab_element[9];
        annee_scolaire = tab_element[10];
        site_web = tab_element[11];

        $(".nom_etab").val(nom_bourse);
        $(".date_creation").val(nom);
        $(".nom_fondateur").val(prenom);
        $(".localisation").val(age);
        $(".bp").val(bp);
        $(".email").val(email);
        $(".tel").val(tel);
        $(".devise").val(devise);
        $(".langue").val(langue);
        $(".annee_scolaire").val(annee_scolaire);
        $(".site_web").val(site_web);
        $("#id_modif").val(id);

        $(".nom_etab").attr("disabled", "True");
        $(".date_creation").attr("disabled", "True");
        $(".nom_fondateur").attr("disabled", "True");
        $(".localisation").attr("disabled", "True");
        $(".bp").attr("disabled", "True");
        $(".email").attr("disabled", "True");
        $(".tel").attr("disabled", "True");
        $(".devise").attr("disabled", "True");
        $(".langue").attr("disabled", "True");
        $(".annee_scolaire").attr("disabled", "True");
        $(".site_web").attr("disabled", "True");
        $("#id_modif").attr("disabled", "True");

    });*/




    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_bourse");
          var url_action = form.attr("action");

          var trier_par = "non defini";

          $("body table thead th span").each(function () {

                var classe_actuelle = String($(this).attr("class"));

                if(classe_actuelle.search("text-primary") != -1){

                    trier_par = $(this).parents("th").attr("class");

                    if (classe_actuelle.search("tri-desc") != -1){
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

        var form = $(".recherche_bourse");
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

        var form = $(".recherche_bourse");
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
