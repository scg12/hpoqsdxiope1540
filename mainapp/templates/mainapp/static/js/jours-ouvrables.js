$(document).ready(function(){

$(".pause_rmv").click(function() {
  ind = $("input[sa]").length;
  div = "div"+""+ind;
  $("."+div).remove();
  $("#nb_pauses").val(ind-1);
});
$(".pause_add").click(function() {
ind = $("input[sa]").length + 1;
$("#nb_pauses").val(ind);
pause_var = "pause"+""+ind;
nom_pause = "libelle_pause"+""+ind;
div = "div"+""+ind;
ligne = `<div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Libellé</label>
                           <input type="text" name="${nom_pause}" class="form-group form-control ">
                              </div>
                           </div>
                       </div>
                       <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-1 ${div}">
                          <div class="input-group form-control-md ">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Durée</label>
                           <input type="number" sa pause style="width:70px;" min="1" name="${pause_var}" class="form-group form-control">
                              </div>
                           </div>
                       </div>
                        <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Minutes</label>
                              </div>
                           </div>
                       </div>`;
$(".les_pauses").append(ligne);
});
   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_eleve33");
        var url_action = form.attr("action");
        // var url_action = '/mainapp/recherche-eleve3/';
        
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

              liste_sous_etablissements = data.jours_ouvrables;
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
                fin = data.jours_ouvrables.length;
              }

              if (liste_sous_etablissements.length != 0){

                  for (var i = debut; i < fin; i++) {

                      id = liste_sous_etablissements[i].id;
                      nom_sousetab = liste_sous_etablissements[i].nom_sousetab;
                      liste_jours_ouvrables = liste_sous_etablissements[i].liste_jours_ouvrables;
                      duree_tranche_horaire = liste_sous_etablissements[i].duree_tranche_horaire;
                      heure_deb_cours = liste_sous_etablissements[i].heure_deb_cours;
                      liste_pauses = liste_sous_etablissements[i].liste_pauses;
                      liste_pauses_afficher = liste_sous_etablissements[i].liste_pauses_afficher;
                      

                    nouvelle_ligne = "<tr class='"+ id+'²²'+ nom_sousetab+ '²²'+ liste_jours_ouvrables +'²²'+ duree_tranche_horaire +'²²'+ heure_deb_cours +'²²'+ liste_pauses +'²²' + liste_pauses_afficher +"'>" + '<th class="fix-col" scope="row">'+ (i+1) +
                    '</th><td class="nom_sousetab fix-col1" style="text-transform: capitalize;">'+ nom_sousetab + '</td><td style="text-transform: capitalize;">' + liste_jours_ouvrables + '</td><td style="text-transform: capitalize;">' + duree_tranche_horaire + '</td><td>'+'</td><td style="text-transform: capitalize;">' + heure_deb_cours+ '</td><td>'+ liste_pauses_afficher +'</td>' + '<td class="td-actions text-right">';
                    // view = '<button type="button" rel="tooltip" class="btn detail-sousetab-link-ajax" data-toggle="modal" data-target="#modal_detail_sousetab"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="btn modifier-sousetab-link-ajax"><i class="material-icons">edit</i></button>';
                    // del = '&nbsp;<button rel="tooltip" class="btn btn-danger supprimer-sousetab-link-ajax"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-sousetab-link");
                    // alert(data.permissions.indexOf("etablissements"));

                        index_model = data.permissions.indexOf("sousetab")
                        // if(data.permissions[index_model + 1] ==1 ){
                        //   nouvelle_ligne += view;
                        // }                      
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                       /* if(data.permissions[index_model + 3] ==0 ){
                          $("button .ajouter-sousetab-link").remove();
                        }                      
                        if(data.permissions[index_model + 4] ==1 ){
                          nouvelle_ligne += del;
                        }*/

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



/*    $("body").on("click", ".ajouter-sousetab-link", function() {
        
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

    });*/


    $(".modifier-sousetab-link").click(function() {

        $('#modal_modifier_sousetab').modal('show');
        $(".les_pauses").empty();

        $(".lundi").prop("checked", false);
         $(".mardi").prop("checked", false);
         $(".mercredi").prop("checked", false);
         $(".jeudi").prop("checked", false);
         $(".vendredi").prop("checked", false);
         $(".samedi").prop("checked", false);
         $(".dimanche").prop("checked", false);

        $("#current_lang").val($("#language").val());
        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        liste_jours_ouvrables = tab_element[2];
        duree_tranche_horaire = tab_element[3];
        heure_deb_cours = tab_element[4];
        liste_pauses = tab_element[5];
        liste_pauses_afficher = tab_element[6];
        h = heure_deb_cours.split("h");
        $(".heure_deb_cours_h").val(h[0]);
        $(".heure_deb_cours_m").val(h[1]);
        $(".sousetab").removeAttr("disabled");
        $(".sousetab").val(id);
        $("#id_sousetab").val(id);
        $(".sousetab").prop("disabled", true);





        // alert(liste_pauses_afficher);

        $(".nom_sousetab").val(nom_sousetab);
        $(".liste_jours_ouvrables").val(liste_jours_ouvrables);
        $(".duree_tranche_horaire").val(duree_tranche_horaire);
        $(".heure_deb_cours").val(heure_deb_cours);
        $(".liste_pauses_afficher").val(liste_pauses_afficher);

        liste_jours_ouvrables = liste_jours_ouvrables.split(", ");
        nb_jours_ouvrables = liste_jours_ouvrables.length - 1;
        liste_jours_ouvrables.forEach( function(item, index) {
            if (index < nb_jours_ouvrables){
              switch(item) {
                case "lundi":
                  $(".lundi").prop("checked", true);
                  break;
                case "mardi":
                  $(".mardi").prop("checked", true);
                  break;
                case "mercredi":
                  $(".mercredi").prop("checked", true);
                  break;
                case "jeudi":
                  $(".jeudi").prop("checked", true);
                  break;
                case "vendredi":
                  $(".vendredi").prop("checked", true);
                  break;
                case "samedi":
                  $(".samedi").prop("checked", true);
                  break;
                case "dimanche":
                  $(".dimanche").prop("checked", true);
                  break;
                default:
                  break;
              }
            }
        });
      /*  alert(ind);
        ind = liste_pauses.split(']');
        nb_item = ind.length - 1;
        var ids = [];
        ind.forEach( function(item, index) {
            if (index < nb_item){
              ids.push(item.split("~")[0]);
            }
        });
        alert(ids);*/
        i = 1;
        liste_pauses_afficher = liste_pauses_afficher.split(", ")
        nb_liste_pauses_afficher = liste_pauses_afficher.length - 1;
        liste_pauses_afficher.forEach( function(item, index) {
          if (index < nb_liste_pauses_afficher){

            elem = item.split(": ")
            nom_pause_val = elem[0]
            pause_val = elem[1]
            id_ = "libelle_pause"+i
            pause_id_ = "pause"+i;
            div = "div"+""+i;
            i++;

            ligne = `<div class="col-sm-0 col-md-1 ${div}"></div><div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Libellé</label>
                           <input type="text" name="${id_}" value="${nom_pause_val}" class="form-group form-control paused">
                              </div>
                           </div>
                       </div>
                       <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-1 ${div}">
                          <div class="input-group form-control-md ">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Durée</label>
                           <input type="number" sa pause style="width:70px;" min="1" value="${pause_val}" name="${pause_id_}" class="form-group form-control paused">
                              </div>
                           </div>
                       </div>
                        <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Minutes</label>
                              </div>
                           </div>
                       </div>`;
          $(".les_pauses").append(ligne);
          }
          $("#nb_pauses").val($("input[sa]").length);

      });
    $("#id_modif").val(id);
});



    /*$(".supprimer-sousetab-link").click(function() {

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
    
    });*/

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_eleve33");
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
      
    // $("body").on("click", ".supprimer-sousetab-link-ajax", function() {
        
    //     $('#modal_supprimer_sousetab').modal('show');

    //     var classe = $(this).parents("tr").attr('class');
    //     tab_element = classe.split("²²");
    //     id = tab_element[0];
    //     matricule = tab_element[1];
    //     nom = tab_element[2];
    //     prenom = tab_element[3];
    //     age = tab_element[4];
        
    //     $("#id_supp").val(id);
    //     $("#modal_supprimer_sousetab .matricule").text(matricule);
    //     $("#modal_supprimer_sousetab .nom").text(nom);
    //     $("#modal_supprimer_sousetab .prenom").text(prenom);
    //     $("#modal_supprimer_sousetab .age").text(age);

    // });


    $("body").on("click", ".modifier-sousetab-link-ajax", function() {
        
        $('#modal_modifier_sousetab').modal('show');
        $("#current_lang").val($("#language").val());

         $(".lundi").prop("checked", false);
         $(".mardi").prop("checked", false);
         $(".mercredi").prop("checked", false);
         $(".jeudi").prop("checked", false);
         $(".vendredi").prop("checked", false);
         $(".samedi").prop("checked", false);
         $(".dimanche").prop("checked", false);

        $(".les_pauses").empty();
        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        liste_jours_ouvrables = tab_element[2];
        duree_tranche_horaire = tab_element[3];
        heure_deb_cours = tab_element[4];
        liste_pauses = tab_element[5];
        liste_pauses_afficher = tab_element[6];
        h = heure_deb_cours.split("h");
        $(".heure_deb_cours_h").val(h[0]);
        $(".heure_deb_cours_m").val(h[1]);
        $(".sousetab").removeAttr("disabled");
        $(".sousetab").val(id);
        $("#id_sousetab").val(id);
        $(".sousetab").prop("disabled", true);

        $(".nom_sousetab").val(nom_sousetab);
        $(".liste_jours_ouvrables").val(liste_jours_ouvrables);
        $(".duree_tranche_horaire").val(duree_tranche_horaire);
        $(".heure_deb_cours").val(heure_deb_cours);
        $(".liste_pauses_afficher").val(liste_pauses_afficher);


        liste_jours_ouvrables = liste_jours_ouvrables.split(", ");
        nb_jours_ouvrables = liste_jours_ouvrables.length - 1;
        liste_jours_ouvrables.forEach( function(item, index) {
            if (index < nb_jours_ouvrables){
              switch(item) {
                case "lundi":
                  $(".lundi").prop("checked", true);
                  break;
                case "mardi":
                  $(".mardi").prop("checked", true);
                  break;
                case "mercredi":
                  $(".mercredi").prop("checked", true);
                  break;
                case "jeudi":
                  $(".jeudi").prop("checked", true);
                  break;
                case "vendredi":
                  $(".vendredi").prop("checked", true);
                  break;
                case "samedi":
                  $(".samedi").prop("checked", true);
                  break;
                case "dimanche":
                  $(".dimanche").prop("checked", true);
                  break;
                default:
                  break;
              }
            }
        });
        
        i = 1;
        liste_pauses_afficher = liste_pauses_afficher.split(", ")
        nb_liste_pauses_afficher = liste_pauses_afficher.length - 1;
        liste_pauses_afficher.forEach( function(item, index) {
          if (index < nb_liste_pauses_afficher){

            elem = item.split(": ")
            nom_pause_val = elem[0]
            pause_val = elem[1]
            id_ = "libelle_pause"+i
            pause_id_ = "pause"+i;
            div = "div"+""+i;
            i++;

            ligne = `<div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Libellé</label>
                           <input type="text" name="${id_}" value="${nom_pause_val}" class="form-group form-control paused">
                              </div>
                           </div>
                       </div>
                       <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-1 ${div}">
                          <div class="input-group form-control-md ">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Durée</label>
                           <input type="number" sa pause style="width:70px;" min="1" value="${pause_val}" name="${pause_id_}" class="form-group form-control paused">
                              </div>
                           </div>
                       </div>
                        <div class="col-sm-0 col-md-1 ${div}"></div>
                       <div class="col-sm-12 col-md-4 ${div}">
                          <div class="input-group form-control-md">
                              <div class="form-group bmd-form-group ">
                           <label for="pause1" class="bmd-label-floating ">Minutes</label>
                              </div>
                           </div>
                       </div>`;
          $(".les_pauses").append(ligne);
          }
          $("#nb_pauses").val($("input[sa]").length);

      });

    });


      
    /*$("body").on("click", ".detail-sousetab-link-ajax", function() {
        
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

    });*/




    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_eleve33");
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

        var form = $(".recherche_eleve33");
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

        var form = $(".recherche_eleve33");
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
