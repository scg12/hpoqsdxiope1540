$(document).ready(function(){
 
// var validator = $("#creation_eleve_form").validate(options);
// var completed = false;
// var firstNonBlankedValue = "";
// var nbre_complet
// $(".text-foo").each(function(){
//     if($(this).length > 0){
//         firstNonBlankedValue = $(this).val();
//         return;
//     }
// });
// console.log(firstNonBlankedValue);
var nbre_ok = 0;

$('.terminer').prop("disabled", true);


// $("input[text]").keyup(function()
 $("body").on("click", ".radio_classe", function() {
 // $(":radio").on("click", function(){
    continuer = false;

    // $(":checkbox"). prop("checked", true);
    // $(":checkbox"). prop("checked", false);

    nb_checkbox_selected = $(":checkbox:checked").length;
    nb_classe_selected = $(":radio:checked").length;
    if (nb_checkbox_selected > 0)
       continuer = true;
    else if (nb_classe_selected > 0)
       continuer = true;

    var validator = $("#creation_eleve_form").validate({ ignore: "" });
    // alert(validator.form()+"__"+continuer);
    if (validator.form() && continuer) {
        $('.terminer').removeAttr("disabled");
        // alert("YOOO");
    }
    else
       $('.terminer').prop("disabled", true);
    });

$( ":text" ).keyup(function(){
  //  On s'assure qu'une classe est sélectionnée
  continuer = false;
  nb_checkbox_selected = $(":checkbox:checked").length;
  nb_classe_selected = $(":radio:checked").length;
  if (nb_checkbox_selected > 0)
     continuer = true;
  else if (nb_classe_selected > 0)
     continuer = true;

  var validator = $("#creation_eleve_form").validate({ ignore: "" });
  // alert(validator.form()+"__"+continuer);
  if (validator.form() && continuer) {
      $('.terminer').removeAttr("disabled");
      // alert("YOOO");
  }
  else
     $('.terminer').prop("disabled", true);

    // $("input").css("background-color", "pink");
  // Si nbre_ok = 6 alors le formulaire est valide
  
  // name = $(this).attr("name");
  // if (name == "nom" || name == "adresse" || name == "date_naissance" || name == "lieu_naissance" || name == "date_entree" || name == "redouble")
  //    {
  //     if($(this).length > 0){
  //       nbre_ok ++;
  //       alert(name+"  nbre_ok :"+nbre_ok+" val "+$(this).val());
  //       }
  //     else
  //       nbre_ok--;

  //     if (nbre_ok == 6)
  //     {
  //      alert("c'est ok"); 
  //      $('.terminer').removeAttr("disabled");
  //     }
  //    else
  //      $('.terminer').prop("disabled", true);
  //    }



  // $(":text").each(function(){
  //   name = $(this).attr("name");
  //   if (name == "nom" || name == "adresse" || name == "date_naissance" || name == "lieu_naissance" || name == "date_entree" || name == "redouble")
  //    {
  //     if($(this).length > 0){
  //       nbre_ok ++; alert(name+"  nbre_ok :"+nbre_ok+" val "+$(this).val());
  //       }
  //    }    
  //  });
    
});

$("#datetimepicker").datetimepicker();

// var is_nb_matformat_ok = $('#is_nb_matformat_ok').attr('class');
//     // alert(is_nb_matformat_ok);
//     if (is_nb_matformat_ok == "ok"){
//       // $('.terminer').prop("disabled", false);
//       // alert("Ok");
//       $('.terminer').removeAttr("disabled")
//     }
//     else{
//       // alert("disabled");
//       $('.terminer').prop("disabled", true);
//     }



  $(".choix_etab").on("change", function(){
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

  $(":checkbox").on("click", function(){
    // alert("yesss");
    var checkBoxes = $(":checkbox[son]");
        checkBoxes.prop("checked", checkBoxes.prop("checked"));
        // alert($(":checkbox[son]:checked").length > 0);
        if ($(":checkbox[son]:checked").length > 0) {
         $(":radio[sa]").attr("disabled", true);
         // alert($(":radio:disabled").length+" "+$(":radio:checked").length);

        }
        else {
          checkBoxes.prop("disabled", checkBoxes.prop(false));
          $(":radio[sa]").removeAttr("disabled");
        }

        //  On s'assure qu'une classe est sélectionnée
        continuer = false;
        nb_checkbox_selected = $(":checkbox:checked").length;
        nb_classe_selected = $(":radio:checked").length;
        if (nb_checkbox_selected > 0)
           continuer = true;
        else if (nb_classe_selected > 0)
           continuer = true;

    var validator = $("#creation_eleve_form").validate({ ignore: "" });
    // if ($(":checkbox:checked").length <= 0 || $(":radio:checked").length <= 0) 
    //    $('.terminer').prop("disabled", true);
    // else if (validator.form() && $(":checkbox:checked").length > 0)
    //     $('.terminer').removeAttr("disabled");
     if ($(":checkbox:checked").length > 0){
       if (validator.form() && $(":radio").length > 0)
          $('.terminer').removeAttr("disabled");
       }
     else 
       {
        if ($(":radio:checked").length > 0 && validator.form())
           $('.terminer').removeAttr("disabled");
        else 
           $('.terminer').prop("disabled", true);
       }
    });
    //  $(":radio[sa]").on("click", function(){
    // alert("ya");
    // var checkBoxes = $(":radio[sa]");
    //     if ($(":checkbox[son]:checked").length > 0) {
    //      checkBoxes.prop("checked", !checkBoxes.prop("checked"));
    //      $(this).prop("checked", !checkBoxes.prop("checked"));
    //     }
    //     else {
    //       checkBoxes.prop("disabled", checkBoxes.prop(false));
    //       $(":radio[sa]").removeAttr("disabled");
    //     }
    // });

  $(".choix_sousetab").on("change", function(){
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

  $(".choix_niveau").on("change", function(){
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

  $(".specialite").on("change", function(){
  // On met la variable position à 3 pour indiquer que c'est niveau qui a changé
    specialite = $('.specialite').val()
    position = "4";
    id_specialite = specialite.split("_")[1];
    specialite = specialite.split("_")[0];

    var form = $(".load_specialites_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_specialite + "²²~~" + specialite;

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
          liste_specialites = data.specialites;
          nbre_specialites = liste_specialites.length;
          liste_classes = data.classes;
          nbre_classes = liste_classes.length;

          $('.choix_sousetab').empty();
          $('.choix_niveau').empty();
          $('.specialite').empty();
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
           option = "Aucune_"+0;
           specialite = "Aucune"
            id = 0;
            $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)

           for (var i = 0; i < nbre_niveaux; i++) {
              nom_niveau = liste_niveaux[i].nom_niveau;                     
              id = liste_niveaux[i].id;
              option = nom_niveau+"_"+id;
              $('.choix_niveau').append(`<option value="${option}"> 
                                         ${nom_niveau} 
                                    </option>`)
           }

            for (var i = 0; i < nbre_specialites; i++) {
              specialite = liste_specialites[i].specialite;                     
              id = liste_specialites[i].id_niveau;
              option = specialite+"_"+id;
              $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)
           }
           
           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
            if ($(":checkbox[son]:checked").length > 0)
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe disabled  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)
            else
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)

           }

           var validator = $("#creation_eleve_form").validate({ ignore: "" });
            // alert($(":checkbox:checked").length+"_"+$(":radio").length+"_"+validator.form())
            if ($(":radio").length > 0 && validator.form() && $(":checkbox:checked").length > 0)
              $('.terminer').removeAttr("disabled");
            else 
              $('.terminer').prop("disabled", true);
        } 
        if (choix == "sousetab"){
            liste_niveaux = data.niveaux;
            nbre_niveaux = liste_niveaux.length;
            liste_classes = data.classes;
            nbre_classes = liste_classes.length;
            liste_specialites = data.specialites;
            nbre_specialites = liste_specialites.length;

            $('.choix_niveau').empty();
            $('.specialite').empty();
            $('#liste_classes_niveaux').empty();
            // $('#choix_specialite').empty();
            $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);

            for (var i = 0; i < nbre_niveaux; i++) {
              nom_niveau = liste_niveaux[i].nom_niveau;                     
              id = liste_niveaux[i].id;
              option = nom_niveau+"_"+id;
              $('.choix_niveau').append(`<option value="${option}"> 
                                         ${nom_niveau} 
                                    </option>`)
           }
           option = "Aucune_"+0;
           specialite = "Aucune"
            id = 0;
            $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)
            
            for (var i = 0; i < nbre_specialites; i++) {
              specialite = liste_specialites[i].specialite;                     
              id = liste_specialites[i].id_niveau;
              option = specialite+"_"+id;
              $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)
           }

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              if ($(":checkbox[son]:checked").length > 0)
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe disabled  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)
            else
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)

           }

           var validator = $("#creation_eleve_form").validate({ ignore: "" });
            // alert($(":checkbox:checked").length+"_"+$(":radio").length+"_"+validator.form())
            if ($(":radio").length > 0 && validator.form() && $(":checkbox:checked").length > 0)
              $('.terminer').removeAttr("disabled");
            else 
              $('.terminer').prop("disabled", true);
          
        }

        if (choix == "niveau"){
            liste_classes = data.classes;
            nbre_classes = liste_classes.length;
            liste_specialites = data.specialites;
            nbre_specialites = liste_specialites.length;

            $('.specialite').empty();
            $('#liste_classes_niveaux').empty();
            $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);
            option = "Aucune_"+0;
            specialite = "Aucune"
            id = 0;
            $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)

           for (var i = 0; i < nbre_specialites; i++) {
              specialite = liste_specialites[i].specialite;                     
              id = liste_specialites[i].id_niveau;
              option = specialite+"_"+id;
              $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`)
           }
           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              if ($(":checkbox[son]:checked").length > 0)
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe disabled  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)
            else
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)

           }

           var validator = $("#creation_eleve_form").validate({ ignore: "" });
            // alert($(":checkbox:checked").length+"_"+$(":radio").length+"_"+validator.form())
            if ($(":radio").length > 0 && validator.form() && $(":checkbox:checked").length > 0)
              $('.terminer').removeAttr("disabled");
            else 
              $('.terminer').prop("disabled", true);
        }

        if (choix == "specialite"){
            liste_classes = data.classes;
            nbre_classes = liste_classes.length;

            $('#liste_classes_niveaux').empty();
            $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe;                     
              id = liste_classes[i].id;
              option = nom_classe+"_"+id+"_*";
              // alert(option);
              if ($(":checkbox[son]:checked").length > 0)
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe disabled  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)
            else
              $('#liste_classes_niveaux').append(`<input type=radio name=classe_selected sa=1 class=radio_classe  value="${option}"> 
                                         ${nom_classe}&nbsp;&nbsp;&nbsp;`)

           }

           var validator = $("#creation_eleve_form").validate({ ignore: "" });
            // alert($(":checkbox:checked").length+"_"+$(":radio").length+"_"+validator.form())
            if ($(":radio").length > 0 && validator.form() && $(":checkbox:checked").length > 0)
              $('.terminer').removeAttr("disabled");
            else 
              $('.terminer').prop("disabled", true);
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

        var form = $(".recherche_eleve");
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

              liste_eleves = data.eleves;
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
                fin = data.eleves.length;
              }

              if (liste_eleves.length != 0){

                  for (var i = debut; i < fin; i++) {

                      id = liste_eleves[i].id;
                      matricule = liste_eleves[i].matricule;
                      nom = liste_eleves[i].nom;
                      prenom = liste_eleves[i].prenom                      
                      sexe = liste_eleves[i].sexe;
                      redouble = liste_eleves[i].redouble;
                      date_naissance = liste_eleves[i].date_naissance;
                      lieu_naissance = liste_eleves[i].lieu_naissance;
                      date_entree = liste_eleves[i].date_entree;
                      nom_pere = liste_eleves[i].nom_pere;
                      prenom_pere = liste_eleves[i].prenom_pere;
                      nom_mere = liste_eleves[i].nom_mere;
                      prenom_mere = liste_eleves[i].prenom_mere;
                      tel_pere = liste_eleves[i].tel_pere;
                      tel_mere = liste_eleves[i].tel_mere;
                      email_pere = liste_eleves[i].email_pere;
                      email_mere = liste_eleves[i].email_mere;
                      // alert(sexe, prenom, nom, id);
                        nouvelle_ligne = "<tr class='"+ id+'²²'+ matricule +'²²'+ nom+ '²²'+ prenom +'²²'+ sexe +'²²'+ redouble +'²²'+ date_naissance +'²²'+ lieu_naissance +'²²'+ date_entree +'²²'+ nom_pere +'²²'+ prenom_pere +'²²'+ nom_mere +'²²'+ prenom_mere +'²²'+ tel_pere +'²²'+ tel_mere +'²²'+ email_pere +'²²'+ email_mere +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-eleve-link-td fix-col1">'+ matricule + '</td><td style="text-transform: capitalize;" class="detail-eleve-link-td">' + nom + '</td><td class="detail-eleve-link-td">'+ prenom + '</td><td class="detail-eleve-link-td">'+ sexe + '</td><td class="detail-eleve-link-td">'+ redouble + '</td><td class="detail-eleve-link-td">'+ date_naissance + '</td><td class="detail-eleve-link-td">'+ lieu_naissance + '</td><td class="detail-eleve-link-td">'+ date_entree + '</td><td class="detail-eleve-link-td">'+ nom_pere + '</td><td class="detail-eleve-link-td">'+ prenom_pere + '</td><td class="detail-eleve-link-td">'+ nom_mere + '</td><td class="detail-eleve-link-td">'+ prenom_mere + '</td><td class="detail-eleve-link-td">'+ tel_pere + '</td><td class="detail-eleve-link-td">'+ tel_mere + '</td><td class="detail-eleve-link-td">'+ email_pere + '</td><td class="detail-eleve-link-td">'+ email_mere +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-eleve-link-td btn" data-toggle="modal" data-target="#modal_detail_eleve"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-eleve-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-eleve-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-eleve-link");
                    // alert(data.permissions.indexOf("eleves"));

                        index_model = data.permissions.indexOf("eleve")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
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


/*

    $(".ajouter-eleve-link").click(function() {

        $('#modal_ajouter_eleve').modal('show');

        $(".nom").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

        $(".nom").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".age").val("");

    });*/

    $("body").on("click", ".ajouter-eleve-link", function() {
        
        $('#modal_ajouter_eleve').modal('show');

        // $(".matricule").val(matricule);
        // $(".nom").val(nom);
        // $(".prenom").val(prenom);
        // $(".sexe").val(sexe);
        // $(".redouble").val(redouble);
        // $(".date_naissance").val(date_naissance);
        // $(".lieu_naissance").val(lieu_naissance);
        // $(".date_entree").val(date_entree);
        // $(".nom_pere").val(nom_pere);
        // $(".prenom_mere").val(prenom_mere);
        // $(".nom_mere").val(nom_mere);
        // $(".prenom_mere").val(prenom_mere);
        // $(".tel_pere").val(tel_pere);
        // $(".tel_mere").val(tel_mere);
        // $(".email_pere").val(email_pere);
        // $(".email_mere").val(email_mere);
        // $("#id_modif").val(id);

        // $(".matricule").val("");
        // $(".nom").val("");
        // $(".prenom").val("");
        // $(".sexe").val("");
        // $(".redouble").val();
        // $(".date_naissance").val();
        // $(".lieu_naissance").val();
        // $(".date_entree").val();
        // $(".nom_pere").val();
        // $(".prenom_mere").val();
        // $(".nom_mere").val();
        // $(".prenom_mere").val();
        // $(".tel_pere").val();
        // $(".tel_mere").val();
        // $(".email_pere").val();
        // $(".email_mere").val();

    });

    // $(".detail-eleve-link-td").click(function() {
     $("body").on("click", ".detail-eleve-link-td", function() {
//class="{{ cycl.id }}²²{{ cycl.nom }}²²{{ cycl.sous_eleve }}²²{{ cycl.eleve }}"
        $('#modal_detail_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        sexe = tab_element[4];
        redouble = tab_element[5];
        date_naissance = tab_element[6];
        lieu_naissance = tab_element[7];
        date_entree = tab_element[8];
        nom_pere = tab_element[9];
        prenom_pere = tab_element[10];
        nom_mere = tab_element[11];
        prenom_mere = tab_element[12];
        tel_pere = tab_element[13];
        tel_mere = tab_element[14];
        email_pere = tab_element[15];
        email_mere = tab_element[16];
      
        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".redouble").val(redouble);
        $(".date_naissance").val(date_naissance);
        $(".lieu_naissance").val(lieu_naissance);
        $(".date_entree").val(date_entree);
        $(".nom_pere").val(nom_pere);
        $(".prenom_mere").val(prenom_mere);
        $(".nom_mere").val(nom_mere);
        $(".prenom_mere").val(prenom_mere);
        $(".tel_pere").val(tel_pere);
        $(".tel_mere").val(tel_mere);
        $(".email_pere").val(email_pere);
        $(".email_mere").val(email_mere);
        $("#id_modif").val(id);

        $(".matricule").attr("disabled", "True");
        $(".nom").attr("disabled", "True");
        $(".prenom").attr("disabled", "True");
        $(".sexe").attr("disabled", "True");
        $(".redouble").attr("disabled", "True");
        $(".date_naissance").attr("disabled", "True");
        $(".lieu_naissance").attr("disabled", "True");
        $(".date_entree").attr("disabled", "True");
        $(".nom_pere").attr("disabled", "True");
        $(".prenom_mere").attr("disabled", "True");
        $(".nom_mere").attr("disabled", "True");
        $(".prenom_mere").attr("disabled", "True");
        $(".tel_pere").attr("disabled", "True");
        $(".tel_mere").attr("disabled", "True");
        $(".email_pere").attr("disabled", "True");
        $(".email_mere").attr("disabled", "True");

    });


    $(".modifier-eleve-link").click(function() {
        $('#modal_modifier_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        // sexe = tab_element[0];
        // prenom = tab_element[1];
        // nom = tab_element[2];
        // id = tab_element[3];
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        sexe = tab_element[4];
        redouble = tab_element[5];
        date_naissance = tab_element[6];
        lieu_naissance = tab_element[7];
        date_entree = tab_element[8];
        nom_pere = tab_element[9];
        prenom_pere = tab_element[10];
        nom_mere = tab_element[11];
        prenom_mere = tab_element[12];
        tel_pere = tab_element[13];
        tel_mere = tab_element[14];
        email_pere = tab_element[15];
        email_mere = tab_element[16];

        $(".nom").val(nom);
        $(".matricule").val(matricule);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".redouble").val(redouble);
        $(".date_naissance").val(date_naissance);
        $(".lieu_naissance").val(lieu_naissance);
        $(".date_entree").val(date_entree);
        $(".nom_pere").val(nom_pere);
        $(".prenom_mere").val(prenom_mere);
        $(".nom_mere").val(nom_mere);
        $(".prenom_mere").val(prenom_mere);
        $(".tel_pere").val(tel_pere);
        $(".tel_mere").val(tel_mere);
        $(".email_pere").val(email_pere);
        $(".email_mere").val(email_mere);
        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".sexe").removeAttr("disabled");
        $(".redouble").removeAttr("disabled");
        $(".date_naissance").removeAttr("disabled");
        $(".lieu_naissance").removeAttr("disabled");
        $(".date_entree").removeAttr("disabled");
        $(".nom_pere").removeAttr("disabled");
        $(".prenom_mere").removeAttr("disabled");
        $(".nom_mere").removeAttr("disabled");
        $(".prenom_mere").removeAttr("disabled");
        $(".tel_pere").removeAttr("disabled");
        $(".tel_mere").removeAttr("disabled");
        $(".email_pere").removeAttr("disabled");
        $(".email_mere").removeAttr("disabled");

    });



    $(".supprimer-eleve-link").click(function() {

      $('#modal_supprimer_eleve').modal('show');

      var classe = $(this).parents("tr").attr('class');
      tab_element = classe.split("²²");
      /*sexe = tab_element[0];
      prenom = tab_element[1];
      nom = tab_element[2];
      id = tab_element[3];*/
      id = tab_element[0];
      matricule = tab_element[1];
      nom = tab_element[2];
      prenom = tab_element[3];
      sexe = tab_element[4];
      redouble = tab_element[5];
      date_naissance = tab_element[6];
      lieu_naissance = tab_element[7];
      date_entree = tab_element[8];
      nom_pere = tab_element[9];
      prenom_pere = tab_element[10];
      nom_mere = tab_element[11];
      prenom_mere = tab_element[12];
      tel_pere = tab_element[13];
      tel_mere = tab_element[14];
      email_pere = tab_element[15];
      email_mere = tab_element[16];
      
      $("#id_supp").val(id);
      $("#modal_supprimer_eleve .matricule").text(matricule);
      $("#modal_supprimer_eleve .nom").text(nom);
      $("#modal_supprimer_eleve .prenom").text(prenom);
      $("#modal_supprimer_eleve .sexe").text(sexe);
      $("#modal_supprimer_eleve .redouble").text(redouble);
      $("#modal_supprimer_eleve .date_naissance").text(date_naissance);
      $("#modal_supprimer_eleve .lieu_naissance").text(lieu_naissance);
      $("#modal_supprimer_eleve .date_entree").text(date_entree);
      $("#modal_supprimer_eleve .nom_pere").text(nom_pere);
      $("#modal_supprimer_eleve .prenom_mere").text(prenom_mere);
      $("#modal_supprimer_eleve .nom_mere").text(nom_mere);
      $("#modal_supprimer_eleve .prenom_mere").text(prenom_mere);
      $("#modal_supprimer_eleve .tel_pere").text(tel_pere);
      $("#modal_supprimer_eleve .tel_mere").text(tel_mere);
      $("#modal_supprimer_eleve .email_pere").text(email_pere);
      $("#modal_supprimer_eleve .email_mere").text(email_mere);

    
    });

    $("#nbre_element_par_page").on("change", function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_eleve");
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
          sexe = tab_element[4];
          redouble = tab_element[5];
          date_naissance = tab_element[6];
          lieu_naissance = tab_element[7];
          date_entree = tab_element[8];
          nom_pere = tab_element[9];
          prenom_pere = tab_element[10];
          nom_mere = tab_element[11];
          prenom_mere = tab_element[12];
          tel_pere = tab_element[13];
          tel_mere = tab_element[14];
          email_pere = tab_element[15];
          email_mere = tab_element[16];
          
          $("#id_supp").val(id);
          $("#modal_supprimer_eleve .matricule").text(matricule);
          $("#modal_supprimer_eleve .nom").text(nom);
          $("#modal_supprimer_eleve .prenom").text(prenom);
          $("#modal_supprimer_eleve .sexe").text(sexe);
          $("#modal_supprimer_eleve .redouble").text(redouble);
          $("#modal_supprimer_eleve .date_naissance").text(date_naissance);
          $("#modal_supprimer_eleve .lieu_naissance").text(lieu_naissance);
          $("#modal_supprimer_eleve .date_entree").text(date_entree);
          $("#modal_supprimer_eleve .nom_pere").text(nom_pere);
          $("#modal_supprimer_eleve .prenom_mere").text(prenom_mere);
          $("#modal_supprimer_eleve .nom_mere").text(nom_mere);
          $("#modal_supprimer_eleve .prenom_mere").text(prenom_mere);
          $("#modal_supprimer_eleve .tel_pere").text(tel_pere);
          $("#modal_supprimer_eleve .tel_mere").text(tel_mere);
          $("#modal_supprimer_eleve .email_pere").text(email_pere);
          $("#modal_supprimer_eleve .email_mere").text(email_mere);

    });


    $("body").on("click", ".modifier-eleve-link-ajax", function() {
        
        $('#modal_modifier_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        matricule = tab_element[1];
        nom = tab_element[2];
        prenom = tab_element[3];
        sexe = tab_element[4];
        redouble = tab_element[5];
        date_naissance = tab_element[6];
        lieu_naissance = tab_element[7];
        date_entree = tab_element[8];
        nom_pere = tab_element[9];
        prenom_pere = tab_element[10];
        nom_mere = tab_element[11];
        prenom_mere = tab_element[12];
        tel_pere = tab_element[13];
        tel_mere = tab_element[14];
        email_pere = tab_element[15];
        email_mere = tab_element[16];

        $(".matricule").val(matricule);
        $(".nom").val(nom);
        $(".prenom").val(prenom);
        $(".sexe").val(sexe);
        $(".redouble").val(redouble);
        $(".date_naissance").val(date_naissance);
        $(".lieu_naissance").val(lieu_naissance);
        $(".date_entree").val(date_entree);
        $(".nom_pere").val(nom_pere);
        $(".prenom_mere").val(prenom_mere);
        $(".nom_mere").val(nom_mere);
        $(".prenom_mere").val(prenom_mere);
        $(".tel_pere").val(tel_pere);
        $(".tel_mere").val(tel_mere);
        $(".email_pere").val(email_pere);
        $(".email_mere").val(email_mere);
        $("#id_modif").val(id);

        $(".matricule").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".sexe").removeAttr("disabled");
        $(".redouble").removeAttr("disabled");
        $(".date_naissance").removeAttr("disabled");
        $(".lieu_naissance").removeAttr("disabled");
        $(".date_entree").removeAttr("disabled");
        $(".nom_pere").removeAttr("disabled");
        $(".prenom_mere").removeAttr("disabled");
        $(".nom_mere").removeAttr("disabled");
        $(".prenom_mere").removeAttr("disabled");
        $(".tel_pere").removeAttr("disabled");
        $(".tel_mere").removeAttr("disabled");
        $(".email_pere").removeAttr("disabled");
        $(".email_mere").removeAttr("disabled");

    });


      
  /*  $("body").on("click", ".detail-eleve-link-ajax", function() {
        $('#modal_detail_eleve').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom = tab_element[1];
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

        $(".sexe").val(nom);
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

        $(".sexe").attr("disabled", "True");
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

          var form = $(".recherche_eleve");
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

        var form = $(".recherche_eleve");
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

        var form = $(".recherche_eleve");
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
