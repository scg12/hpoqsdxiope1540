$(document).ready(function(){
$("#datetimepicker1").datetimepicker();
$("#datetimepicker2").datetimepicker();

$("body").on("change", ".entree_sortie_caisee2", function() {

  if ($(this).val() == "s"){
    $(".montant").removeAttr('required');
    $(".ordre_paiement").removeAttr('required');
    // $(".date_deb").removeAttr('required');
    // $(".date_fin").removeAttr('required');
    // $(".date_ordre_paiement").prop("hidden", true);
    $(".montant_label").text("Montant");
  }
  else{
    $(".montant").prop("required", true);
    // $(".date_ordre_paiement").removeAttr('hidden');
    // $(".date_deb").prop("required", true);
    // $(".date_fin").prop("required", true);
    $(".ordre_paiement").prop("required", true);
    $(".montant_label").text("Montant*");
  }
});

$(".choix_etab").on("change", function(){
  // On met la variable position à 1 pour indiquer que c'est etab qui a changé

    etab = $('.choix_etab').val()
    position = "1";
    id_etab = etab.split("_")[1];
    etab = etab.split("_")[0];

    var form = $(".load_type_payement_eleve_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_etab + "²²~~" + etab + "²²~~" + id_etab;

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

$(".choix_sousetab").on("change", function(){
  // On met la variable position à 2 pour indiquer que c'est sousetab qui a changé
    sousetab = $('.choix_sousetab').val();
    id_etab = $('.choix_etab').val().split("_")[1];
    position = "2";
    id_sousetab = sousetab.split("_")[1];
    sousetab = sousetab.split("_")[0];
    if (id_sousetab == "all"){
       $('.choix_cycle').empty();
          $('.choix_niveau').empty();
          $('.specialite').empty();
          $('.choix_classes').empty();
    }else{
          var form = $(".load_type_payement_eleve_ajax");
          var url_action = form.attr("action");
          var donnees = position + "²²~~" + id_sousetab + "²²~~" + sousetab + "²²~~" + id_etab;

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
     }
    
    });
  $(".choix_cycle").on("change", function(){
  // On met la variable position à 3 pour indiquer que c'est cycle qui a changé
    cycle = $('.choix_cycle').val();
    id_sousetab = $('.choix_cycle').val().split("_")[1];
    position = "3";
    id_cycle = cycle.split("_")[1];
    cycle = cycle.split("_")[0];

    if (id_cycle == "all"){
          $('.choix_niveau').empty();
          $('.specialite').empty();
          $('.choix_classes').empty();
    }else{

        var form = $(".load_type_payement_eleve_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_cycle + "²²~~" + cycle + "²²~~" + id_sousetab;

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
    }
    });
    $(".choix_niveau").on("change", function(){
  // On met la variable position à 3 pour indiquer que c'est niveau qui a changé
    niveau = $('.choix_niveau').val();
    id_cycle = $('.choix_niveau').val().split("_")[1];
    position = "4";
    id_niveau = niveau.split("_")[1];
    niveau = niveau.split("_")[0];

    if (id_niveau == "all"){
          $('.specialite').empty();
          $('#liste_classes_niveaux').empty();
          $('.choix_classes').empty();
    }else{
        var form = $(".load_type_payement_eleve_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_niveau + "²²~~" + niveau + "²²~~" + id_cycle;

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
    }
    });

  $(".specialite").on("change", function(){
  // On met la variable position à 3 pour indiquer que c'est niveau qui a changé
    specialite = $('.specialite').val();
    id_niveau = $('.choix_niveau').val().split("_")[1];
    position = "5";
    // id_specialite = specialite.split("_")[1];
    specialite = specialite.split("_")[0];

 /*if (specialite == "tous"){
          $('#liste_classes_niveaux').empty();
          $('#liste_classes_niveaux').append(`Classes:&nbsp;&nbsp;&nbsp;`);
          $('#liste_classes_niveaux').append(`<select name="choix_classes" style="width:200px;" class="choix_classes" size="4" multiple>
                                 </select>`);
    }else{*/
        var form = $(".load_type_payement_eleve_ajax");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_niveau + "²²~~" + specialite + "²²~~" + id_niveau;
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
    // }

    });

function gererSucces2(data) {
  console.log(data);
  choix = data.choix;

  if (choix == "etab") {
          liste_sousetabs = data.sousetabs;
          nbre_sousetabs = liste_sousetabs.length;
          

          $('.choix_sousetab').empty();
          $('.choix_cycle').empty();
          $('.choix_niveau').empty();
          $('.specialite').empty();
          $('.choix_classes').empty();
          
          $('.choix_sousetab').append(`<option value=tous_all>Tous`)
           for (var i = 0; i < nbre_sousetabs; i++) {
              nom_sousetab = liste_sousetabs[i].nom_sousetab                      
              id = liste_sousetabs[i].id;
              option = nom_sousetab+"_"+id;
              $('.choix_sousetab').append(`<option value="${option}"> 
                                         ${nom_sousetab} 
                                    </option>`);
           }
      }
  if (choix == "sousetab") {
          liste_cycles = data.cycles;
          nbre_cycles = liste_cycles.length;
          
          $('.choix_cycle').empty();
          $('.choix_niveau').empty();
          $('.specialite').empty();
          $('.choix_classes').empty();
          $('.choix_cycle').append(`<option value=tous_all>Tous`)
           for (var i = 0; i < nbre_cycles; i++) {
              nom_cycle = liste_cycles[i].nom_cycle                      
              id = liste_cycles[i].id;
              option = nom_cycle+"_"+id;
              $('.choix_cycle').append(`<option value="${option}"> 
                                         ${nom_cycle} 
                                    </option>`);
           }
     }
  if (choix == "cycle") {
          liste_niveaux = data.niveaux;
          nbre_niveaux = liste_niveaux.length;
          
          $('.choix_niveau').empty();
          $('.specialite').empty();
          $('.choix_classes').empty();
          $('.choix_niveau').append(`<option value=tous_all>Tous`)
           for (var i = 0; i < nbre_niveaux; i++) {
              nom_niveau = liste_niveaux[i].nom_niveau                      
              id = liste_niveaux[i].id;
              option = nom_niveau+"_"+id;
              $('.choix_niveau').append(`<option value="${option}"> 
                                         ${nom_niveau} 
                                    </option>`);
           }
     }
  if (choix == "niveau") {
          liste_specialites = data.specialites;
          nbre_specialites = liste_specialites.length;

          liste_classes = data.classes;
          nbre_classes = liste_classes.length;
          
          $('.specialite').empty();
          $('.choix_classes').empty();
          if (nbre_specialites != 0)
            $('.specialite').append(`<option value=tous_all>Toutes`);
          $('.specialite').append(`<option value=aucune_aucune>Sans spécialité`);
           for (var i = 0; i < nbre_specialites; i++) {
              specialite = liste_specialites[i].specialite                      
              id = liste_specialites[i].id;
              option = specialite+"_"+id;
              $('.specialite').append(`<option value="${option}"> 
                                         ${specialite} 
                                    </option>`);
           }

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe                      
              id = liste_classes[i].id;
              option = nom_classe+"_"+id;
              $('.choix_classes').append(`<option value="${option}"> 
                                         ${nom_classe} 
                                    </option>`);
           }
     }

    if (choix == "specialite") {
          liste_classes = data.classes;
          nbre_classes = liste_classes.length;
          
          $('.choix_classes').empty();

           for (var i = 0; i < nbre_classes; i++) {
              nom_classe = liste_classes[i].nom_classe                      
              id = liste_classes[i].id;
              option = nom_classe+"_"+id;
              $('.choix_classes').append(`<option value="${option}"> 
                                         ${nom_classe} 
                                    </option>`);
           }
     }

  } 

function gererErreur2(error) {
    $("#message").text(error);
        console.log(error);
}

// Lorsqu'on veut voir les paiements d'une autre classe
$("body").on("change", "#classe_recherchee", function() {

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_paiement");
        var url_action = form.attr("action");
        var classe_recherchee = $("#classe_recherchee").val();
        var trier_par = "non defini";

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + classe_recherchee ;

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

// Debut de la recherche
   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 
        $("#classe_recherchee").val("tous_all");
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

          if(data.permissions.indexOf("typepayementeleve") == -1){
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
                      montant = liste_paiements[i].montant                      
                      liste_classes_afficher = liste_paiements[i].liste_classes_afficher
                      ordre_paiement = liste_paiements[i].ordre_paiement                      

                      id = liste_paiements[i].id;
                      // alert(nom_etab, classe, libelle, id);
                        nouvelle_ligne = "<tr class='"+ id +'²²'+ libelle +'²²'+ date_deb +'²²'+ date_fin +'²²'+ entree_sortie_caisee +'²²'+ montant +'²²'+ liste_classes_afficher +'²²'+ ordre_paiement+"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-paiement-link-td fix-col1">'+ libelle + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ date_deb + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ date_fin + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ entree_sortie_caisee + '</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ montant +'</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ liste_classes_afficher +'</td><td style="text-transform: uppercase;" class="detail-paiement-link-td">'+ ordre_paiement +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-paiement-link-td btn" data-toggle="modal" data-target="#modal_detail_paiement"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-paiement-link-ajax btn"><i class="material-icons">edit</i></button>';
                    del = '&nbsp;<button rel="tooltip" class="supprimer-paiement-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-paiement-link");
                    // alert(data.permissions.indexOf("paiements"));

                        index_model = data.permissions.indexOf("typepayementeleve")
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

        /*$("#modal_ajouter_paiement .libelle").val(libelle);
        $("#modal_ajouter_paiement .date_deb").val(date_deb);
        $("#modal_ajouter_paiement .date_fin").val(date_fin);
        $("#modal_ajouter_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_ajouter_paiement .montant").val(montant);
        $("#modal_ajouter_paiement .classe").val(classe);*/
        // $("#id_modif").val(id);

        $("#modal_ajouter_paiement .libelle").val("");
        $("#modal_ajouter_paiement .date_deb").val("");
        $("#modal_ajouter_paiement .date_fin").val("");
        $("#modal_ajouter_paiement .entree_sortie_caisee").val("");
        $("#modal_ajouter_paiement .montant").val("");
        $("#modal_ajouter_paiement .liste_classes_afficher").val("");

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
        liste_classes_afficher = tab_element[6];
        ordre_paiement = tab_element[7];
      
        $("#modal_detail_paiement .libelle").val(libelle);
        $("#modal_detail_paiement .date_deb").val(date_deb);
        $("#modal_detail_paiement .date_fin").val(date_fin);
        $("#modal_detail_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_detail_paiement .montant").val(montant);
        $("#modal_detail_paiement .liste_classes_afficher").val(liste_classes_afficher);
        $("#modal_detail_paiement .ordre_paiement").val(ordre_paiement);
        $("#id_modif").val(id);

        $("#modal_detail_paiement .libelle").attr("disabled", "True");
        $("#modal_detail_paiement .date_deb").attr("disabled", "True");
        $("#modal_detail_paiement .date_fin").attr("disabled", "True");
        $("#modal_detail_paiement .entree_sortie_caisee").attr("disabled", "True");
        $("#modal_detail_paiement .montant").attr("disabled", "True");
        $("#modal_detail_paiement .liste_classes_afficher").attr("disabled", "True");
        $("#modal_detail_paiement .ordre_paiement").attr("disabled", "True");

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
        liste_classes_afficher = tab_element[6];
        ordre_paiement = tab_element[7];

        $("#modal_modifier_paiement .libelle").val(libelle);
        $("#modal_modifier_paiement .date_deb").val(date_deb);
        $("#modal_modifier_paiement .date_fin").val(date_fin);
        $("#modal_modifier_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_modifier_paiement .montant").val(montant);
        $("#modal_modifier_paiement .liste_classes_afficher").val(liste_classes_afficher);
        $("#modal_modifier_paiement .ordre_paiement").val(ordre_paiement);
        $("#id_modif").val(id);

        $("#modal_modifier_paiement .libelle").removeAttr("disabled");
        $("#modal_modifier_paiement .date_deb").removeAttr("disabled");
        $("#modal_modifier_paiement .date_fin").removeAttr("disabled");
        $("#modal_modifier_paiement .entree_sortie_caisee").removeAttr("disabled");
        $("#modal_modifier_paiement .montant").removeAttr("disabled");
        $("#modal_modifier_paiement .liste_classes_afficher").removeAttr("disabled");
        $("#modal_modifier_paiement .ordre_paiement").removeAttr("disabled");

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
      liste_classes_afficher = tab_element[6];
      ordre_paiement = tab_element[7];

      
      $("#id_supp").val(id);
      $("#modal_supprimer_paiement .libelle").text(libelle);
      $("#modal_supprimer_paiement .date_deb").text(date_deb);
      $("#modal_supprimer_paiement .date_fin").text(date_fin);
      $("#modal_supprimer_paiement .entree_sortie_caisee").text(entree_sortie_caisee);
      $("#modal_supprimer_paiement .montant").text(montant);
      $("#modal_supprimer_paiement .liste_classes_afficher").text(liste_classes_afficher);
      $("#modal_supprimer_paiement .ordre_paiement").text(ordre_paiement);
    
    });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        $("#classe_recherchee").val("tous_all");
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
          liste_classes_afficher = tab_element[6];
          ordre_paiement = tab_element[7];

          $("#id_supp").val(id);
          $("#modal_supprimer_paiement .libelle").text(libelle);
          $("#modal_supprimer_paiement .date_deb").text(date_deb);
          $("#modal_supprimer_paiement .date_fin").text(date_fin);
          $("#modal_supprimer_paiement .entree_sortie_caisee").text(entree_sortie_caisee);
          $("#modal_supprimer_paiement .montant").text(montant);
          $("#modal_supprimer_paiement .liste_classes_afficher").text(liste_classes_afficher);
          $("#modal_supprimer_paiement .ordre_paiement").text(ordre_paiement);

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
        liste_classes_afficher = tab_element[6];
        ordre_paiement = tab_element[7];


        $("#modal_modifier_paiement .montant").val(montant);
        $("#modal_modifier_paiement .liste_classes_afficher").val(liste_classes_afficher);
        $("#modal_modifier_paiement .date_deb").val(date_deb);
        $("#modal_modifier_paiement .libelle").val(libelle);
        $("#modal_modifier_paiement .date_fin").val(date_fin);
        $("#modal_modifier_paiement .entree_sortie_caisee").val(entree_sortie_caisee);
        $("#modal_modifier_paiement .ordre_paiement").val(ordre_paiement);
        $("#id_modif").val(id);

        $("#modal_modifier_paiement .montant").removeAttr("disabled");
        $("#modal_modifier_paiement .liste_classes_afficher").removeAttr("disabled");
        $("#modal_modifier_paiement .libelle").removeAttr("disabled");
        $("#modal_modifier_paiement .date_fin").removeAttr("disabled");
        $("#modal_modifier_paiement .entree_sortie_caisee").removeAttr("disabled");
        $("#modal_modifier_paiement .ordre_paiement").removeAttr("disabled");
        $("#modal_modifier_paiement .date_deb").removeAttr("disabled");

    });


    $("body").on("click", ".pagination-element", function(e) {

          e.stopImmediatePropagation();
          $("#classe_recherchee").val("tous_all");

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
        $("#classe_recherchee").val("tous_all");
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
        $("#classe_recherchee").val("tous_all");
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
