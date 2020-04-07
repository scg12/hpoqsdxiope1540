$(document).ready(function(){

  $(".choix_etab").change(function(){
  // On met la variable position à 1 pour indiquer que c'est etab qui a changé
    etab = $('.choix_etab').val()
    position = "1";
    id_etab = etab.split("_")[1];
    etab = etab.split("_")[0];

    var form = $(".load_specialites_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_etab + "²²~~" + etab;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces2,
             error: gererErreur2,
         });
    });

  $(".choix_sousetab").change(function(){
  // On met la variable position à 2 pour indiquer que c'est sousetab qui a changé
    sousetab = $('.choix_sousetab').val()
    position = "2";
    id_sousetab = sousetab.split("_")[1];
    sousetab = sousetab.split("_")[0];

    var form = $(".load_specialites_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_sousetab + "²²~~" + sousetab;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces2,
             error: gererErreur2,
         });
    });

  $(".choix_niveau").change(function(){
  // On met la variable position à 3 pour indiquer que c'est niveau qui a changé
    niveau = $('.choix_niveau').val()
    position = "3";
    id_niveau = niveau.split("_")[1];
    niveau = niveau.split("_")[0];

    var form = $(".load_specialites_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_niveau + "²²~~" + niveau;

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces2,
             error: gererErreur2,
         });
    });

  function gererSucces2(data) {
        // liste_classes = data.classes;
        
        
        // alert("retour de python");
        console.log(data);
        choix = data.choix;

        if (choix == "etab") {
          liste_sousetabs = data.sousetabs;
          liste_niveaux = data.niveaux;
          nbre_sousetabs = liste_sousetabs.length;
          nbre_niveaux = liste_niveaux.length;
          liste_classes = data.classes;
          nbre_classes = liste_classes.length;

          $('.choix_sousetab').empty();
          $('.choix_niveau').empty();
          $('#liste_classes_niveaux').empty();
          $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`)
           for (var i = 0; i < nbre_sousetabs; i++) {
              nom_sousetab = liste_sousetabs[i].nom_sousetab                      
              id = liste_sousetabs[i].id;
              option = nom_sousetab+"_"+id;
              $('.choix_sousetab').append(`<option value="${option}"> 
                                         ${nom_sousetab} 
                                    </option>`)
              // alert(option);
           }

           for (var i = 0; i < nbre_niveaux; i++) {
              nom_niveau = liste_niveaux[i].nom_niveau;                     
              id = liste_niveaux[i].id;
              option = nom_niveau+"_"+id;
              $('.choix_niveau').append(`<option value="${option}"> 
                                         ${nom_niveau} 
                                    </option>`)
           }

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              $('#liste_classes_niveaux').append(`<input type=checkbox name="${option}" value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)
           }
        } 
        if (choix == "sousetab"){
            liste_niveaux = data.niveaux;
            nbre_niveaux = liste_niveaux.length;
            liste_classes = data.classes;
            nbre_classes = liste_classes.length;
            liste_specialites = data.specialites;
            nbre_specialites = liste_specialites.length;

            $('.choix_niveau').empty();
            $('#liste_classes_niveaux').empty();
            $('#choix_specialite').empty();
            $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);
            for (var i = 0; i < nbre_niveaux; i++) {
              nom_niveau = liste_niveaux[i].nom_niveau;                     
              id = liste_niveaux[i].id;
              option = nom_niveau+"_"+id;
              $('.choix_niveau').append(`<option value="${option}"> 
                                         ${nom_niveau} 
                                    </option>`)
           }

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              $('#liste_classes_niveaux').append(`<input type=checkbox name="${option}" value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`);
           }

           for (var i = 0; i < nbre_specialites; i++) {
              specialite = liste_specialites[i].specialite;                     
              $('#choix_specialite').append(`<option value="${specialite}">`);
           }
        }

        if (choix == "niveau"){
            liste_classes = data.classes;
            nbre_classes = liste_classes.length;

            $('#liste_classes_niveaux').empty();
            $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              $('#liste_classes_niveaux').append(`<input type=checkbox name="${option}" value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`);
           }
        }
        


      }
  function gererErreur2(error) {
        $("#message").text(error);
        console.log(error);
      }

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_classe_specialite");
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
   /*Fonction qui permet de truncate le texte en js du genre bonjour...*/
   String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '&hellip;' : this;
      };

      function gererSucces(data){
        console.log(data);

          if(data.permissions.indexOf("classe") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }else{



            $("table tbody tr").remove();
            //$("table thead").remove();
              
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
              i = 0;
              if (liste_classes.length != 0){
                liste_classes.forEach( function(element, index) {
                    if (index >= debut && index < fin) {
                      nom_etab = element.nom_etab;
                      nom_sousetab = element.nom_sousetab;                      
                      liste_classes_afficher = element.liste_classes_afficher;                      
                      liste_classes = element.liste_classes;                      
                      nom_niveau = element.nom_niveau;
                      specialite = element.specialite;
                      id = element.id_niveau;
                      
                      // alert(nom_etab, nom_sousetab, specialite, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ specialite +'²²'+ liste_classes_afficher +'²²'+ nom_niveau +'²²'+ nom_sousetab +'²²'+ nom_etab+'²²'+ liste_classes +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-classe-link-td fix-col1">'+ specialite + '</td><td style="text-transform: uppercase;" class="detail-classe-link-td">'+ liste_classes_afficher.trunc(20)+ '</td><td style="text-transform: uppercase;" class="detail-classe-link-td">'+ nom_niveau + '</td><td style="text-transform: capitalize;" class="detail-classe-link-td">' + nom_sousetab + '</td><td class="detail-classe-link-td">'+ nom_etab +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-classe-link-td btn" data-toggle="modal" data-target="#modal_detail_classe"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-classe-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-classe-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                    i++;
                    //$("table tbody button:last").addClass("supprimer-classe-link");
                    // alert(data.permissions.indexOf("classes"));

                        index_model = data.permissions.indexOf("classe")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        /*if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }*/  
                        //retirer le bouton add si pas de permission pour ajouter
                        if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-classe-link").remove();
                        }                      
                        if(data.permissions[index_model + 4] ==1 ){
                          nouvelle_ligne += del;
                        }

                        $("table tbody").append(nouvelle_ligne);
                    }    
                  });

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


    $("body").on("click", ".ajouter-classe-link", function() {
        
        $('#modal_ajouter_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');

        tab_element = classe.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        liste_classes_afficher = tab_element[2];
        nom_niveau = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];
        liste_classes = tab_element[6];


        $(".specialite").val(specialite);
        $(".nom_niveau").val(nom_niveau);
        $(".liste_classes_afficher").val(liste_classes_afficher);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $(".liste_classes").val(liste_classes);
        $("#id_modif").val(id);

        $(".specialite").val("");
        $(".nom_niveau").val("");
        $(".liste_classes_afficher").val("");
        $(".nom_sousetab").val("");
        $(".nom_etab").val("");
        $(".liste_classes").val("");

    });

    // $(".detail-classe-link-td").click(function() {
     $("body").on("click", ".detail-classe-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.specialite }}²²{{ cycl.sous_classe }}²²{{ cycl.classe }}"
        $('#modal_detail_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        liste_classes_afficher = tab_element[2];
        nom_niveau = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];
        liste_classes = tab_element[6];
      
        $(".specialite").val(specialite);
        $(".nom_niveau").val(nom_niveau);
        $(".liste_classes_afficher").val(liste_classes_afficher);
        $(".nom_sousetab").val(nom_sousetab);
        $(".nom_etab").val(nom_etab);
        $(".liste_classes").val(liste_classes);
        $("#id_modif").val(id);

        $(".specialite").attr("disabled", "True");
        $(".nom_niveau").attr("disabled", "True");
        $(".liste_classes_afficher").attr("disabled", "True");
        $(".nom_sousetab").attr("disabled", "True");
        $(".nom_etab").attr("disabled", "True");
        $(".liste_classes").val("disabled", "True");

    });


    $(".modifier-classe-link").click(function() {
        $('#modal_modifier_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        liste_classes_afficher = tab_element[2];
        nom_niveau = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];
        liste_classes = tab_element[6];

        $("#modal_modifier_classe .specialite").val(specialite);
        $("#modal_modifier_classe .nom_niveau").val(nom_niveau);
        $("#modal_modifier_classe .liste_classes_afficher").val(liste_classes_afficher);
        $("#modal_modifier_classe .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_classe .nom_etab").val(nom_etab);
        $("#modal_modifier_classe .liste_classes").val(liste_classes);

        $("#id_modif").val(id);

        $("#modal_modifier_classe .specialite").removeAttr("disabled");
        $("#modal_modifier_classe .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_classe .liste_classes_afficher").removeAttr("disabled");
        $("#modal_modifier_classe .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_classe .nom_etab").removeAttr("disabled");
        $("#modal_modifier_classe .liste_classes").removeAttr("disabled");

    });



    $(".supprimer-classe-link").click(function() {

      $('#modal_supprimer_classe').modal('show');

      var classe = $(this).parents("tr").attr('class');
      tab_element = classe.split("²²");
      id = tab_element[0];
      specialite = tab_element[1];
      liste_classes_afficher = tab_element[2];
      nom_niveau = tab_element[3];
      nom_sousetab = tab_element[4];
      nom_etab = tab_element[5];
      liste_classes = tab_element[6];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_classe .specialite").text(specialite);
      $("#modal_supprimer_classe .nom_niveau").text(nom_niveau);
      $("#modal_supprimer_classe .liste_classes_afficher").text(liste_classes_afficher);
      $("#modal_supprimer_classe .nom_sousetab").text(nom_sousetab);
      $("#modal_supprimer_classe .nom_etab").text(nom_etab);
      $("#modal_supprimer_classe .liste_classes").text(liste_classes);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_classe_specialite");
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
          specialite = tab_element[1];
          liste_classes_afficher = tab_element[2];
          nom_niveau = tab_element[3];
          nom_sousetab = tab_element[4];
          nom_etab = tab_element[5];
          liste_classes = tab_element[6];

          
          $("#id_supp").val(id);
          $("#modal_supprimer_classe .specialite").text(specialite);
          $("#modal_supprimer_classe .nom_niveau").text(nom_niveau);
          $("#modal_supprimer_classe .liste_classes_afficher").text(liste_classes_afficher);
          $("#modal_supprimer_classe .nom_sousetab").text(nom_sousetab);
          $("#modal_supprimer_classe .nom_etab").text(nom_etab);
          $("#modal_supprimer_classe .liste_classes").text(liste_classes);

    });


    $("body").on("click", ".modifier-classe-link-ajax", function() {
        
        $('#modal_modifier_classe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        specialite = tab_element[1];
        liste_classes_afficher = tab_element[2];
        nom_niveau = tab_element[3];
        nom_sousetab = tab_element[4];
        nom_etab = tab_element[5];
        liste_classes = tab_element[6];


        $("#modal_modifier_classe .nom_etab").val(nom_etab);
        $("#modal_modifier_classe .nom_sousetab").val(nom_sousetab);
        $("#modal_modifier_classe .liste_classes_afficher").val(liste_classes_afficher);
        $("#modal_modifier_classe .nom_niveau").val(nom_niveau);
        $("#modal_modifier_classe .specialite").val(specialite);
        $("#modal_modifier_classe .liste_classes").val(liste_classes);
        $("#id_modif").val(id);

        $("#modal_modifier_classe .nom_etab").removeAttr("disabled");
        $("#modal_modifier_classe .nom_sousetab").removeAttr("disabled");
        $("#modal_modifier_classe .specialite").removeAttr("disabled");
        $("#modal_modifier_classe .nom_niveau").removeAttr("disabled");
        $("#modal_modifier_classe .liste_classes_afficher").removeAttr("disabled");
        $("#modal_modifier_classe .liste_classes").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_classe_specialite");
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

        var form = $(".recherche_classe_specialite");
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

        var form = $(".recherche_classe_specialite");
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
