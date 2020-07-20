$(document).ready(function(){

$("body").on("click", ".valider", function() {  
swal({ title:"Good job!", text: "You clicked the button!", type: "success", buttonsStyling: false, confirmButtonClass: "btn btn-success"});
});

$("body").on("click", ".activer", function() {
  date_deb = $(".date_deb_saisie1").val().replace("/","-");
  date_fin = $(".date_fin_saisie1").val().replace("/","-");
  // alert($(".date_deb_saisie").val());
  n1 = date_deb.split("-").length - 1;
  n2 = date_fin.split("-").length - 1;
  nb_select = $(":checkbox:checked").length;

  // n1 == 2 date bien formé sinon mal formé. De m pr n2
  if (n1 == 2){
    // Ici on met la date au format anglais pr la recherche
    date = date_deb.split("-");
    un = date[0];
    deux = date[1];
    trois = date[2];
    if (trois.length == 4)
      date_deb = trois+"-"+deux+"-"+un;
    }
    else
      date_deb = "";

   if (n2 == 2){
    // Ici on met la date au format anglais pr la recherche
    date = date_fin.split("-");
    un = date[0];
    deux = date[1];
    trois = date[2];
    if (trois.length == 4)
      date_fin = trois+"-"+deux+"-"+un
    }
    else
      date_fin = "";

  // if (n1 == 2 && n2 == 2 && date_deb > date_fin){
  //   alert("Date Début doit être inférieur à Date Fin");
  // }
   

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;
// alert(date_deb+"  "+date_fin);
// alert( date_deb <= date_fin);
// if (date_deb <= today && date_fin >= today)
//   alert("On reste active");

test = false;
if (nb_select == 1){
    if (n1 == 2 && n2 == 2 && date_deb <= date_fin && date_deb <= today && date_fin >= today){
     // alert("On reste active");
     test = true;
     // Pr ne plus vérifier côté django
     $("#dates_ok").val("all_ok");
    }
    else if (n1 == 2 && n2 != 2 && date_deb <= today) {
      // alert("On reste active deb");
     test = true;
     $("#dates_ok").val("deb_ok");

    }
    else if (n2 == 2 && n1 != 2 && date_fin >= today) {
      // alert("On reste active fin");
     test = true;
     $("#dates_ok").val("fin_ok");

    }
    // else alert("on desactive");
  if (test == false){
      $(".date_deb_saisie1").prop("disabled",true).css("background-color","#ffc6c3");
      $(".date_fin_saisie1").prop("disabled",true).css("background-color","#ffc6c3");
     $("#dates_ok").val("bad_bad");

  }
  else {
      $(".date_deb_saisie1").removeAttr("disabled").css("background-color","inherit");
      $(".date_fin_saisie1").removeAttr("disabled").css("background-color","inherit");
  }
}
else{
  $(".date_deb_saisie1").removeAttr("disabled").css("background-color","inherit");
  $(".date_fin_saisie1").removeAttr("disabled").css("background-color","inherit");
}



});

   $(".recherche").keyup(function(e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "
        // alert("yes...");
        var form = $(".recherche_periodes");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~1";

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


   $("body").on("change", "#sousetab_recherche", function() {
        $("#id_sousetab_selected").val($(this).val());
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".periodes_saisie_actives1");
        var url_action = form.attr("action");
        var trier_par = "non defini";
        var sousetab_recherche = $("#sousetab_recherche").val();

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + sousetab_recherche ;
        // var donnees = classe_recherchee ;

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

/*    function gererSucces2(data) {
    // alert("retour de python");
    console.log(data);
    choix = data.choix;
    if (choix == "sousetab_recherche"){
      sousetabs = data.sousetabs
      id_sousetabs = data.id_sousetabs
      periode_saisies = data.periode_saisies
      nom_evaluation = data.nom_evaluation
      nbre_sousetabs = sousetabs.length;

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
    }
  }
}*/

      function gererSucces(data){
        console.log(data);

          if(data.permissions.indexOf("note") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
          }
     else{


            $("table tbody tr").remove();
            //$("table thead").remove();
              //alert("1");

              liste_periode_saisies = data.periode_saisies;
              nbre_element_par_page = data.nbre_element_par_page;
              numero_page_active = data.numero_page_active;
              liste_page = data.liste_page;
              nom_evaluation = data.nom_evaluation
              id_sousetab_selected = data.id_sousetab_selected
              $("#id_sousetab_selected").val(id_sousetab_selected);

              $(".nom_evaluation").text(nom_evaluation);
              $(".evaluation").empty();

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
                fin = data.periode_saisies.length;
              }

              if (liste_periode_saisies.length != 0){

                  for (var i = debut; i < fin; i++) {
                      libelle = liste_periode_saisies[i].libelle;
                      id = liste_periode_saisies[i].id;
                      $(".evaluation").append(`<option value=${id}>${libelle}`);
                      nom_sousetab = liste_periode_saisies[i].nom_sousetab                      
                      is_active = liste_periode_saisies[i].is_active;
                      is_active_afficher = "<b style=color:green;>Active</b>"
                      date_deb_saisie = liste_periode_saisies[i].date_deb_saisie;
                      date_fin_saisie = liste_periode_saisies[i].date_fin_saisie;
                      if (is_active == false)
                        is_active_afficher = ""
                        nouvelle_ligne = "<tr class='"+ id+'²²'+ nom_sousetab+ '²²'+ libelle+ '²²'+ is_active+ '²²'+ date_deb_saisie +'²²'+ date_fin_saisie +"'>" + '<th scope="row" class="fix-col">'+ (i+1) +
                    '</th><td style="text-transform: uppercase;" class="detail-cycle-link-td fix-col1">'+ nom_sousetab + '</td><td style="text-transform: capitalize;" class="detail-cycle-link-td">' + libelle + '</td><td class="detail-cycle-link-td">'+ is_active_afficher + '</td><td class="detail-cycle-link-td">'+ date_deb_saisie + '</td><td class="detail-cycle-link-td">'+ date_fin_saisie +'</td><td class="td-actions text-right">';
                    view = '<button type="button" rel="tooltip" class="detail-cycle-link-td btn" data-toggle="modal" data-target="#modal_detail_cycle"><i class="material-icons">visibility</i></button>';
                    change ='&nbsp;<button type="button" rel="tooltip" class="modifier-saisie-note-link-ajax btn"><i class="material-icons">edit</i></button>';
                    // del = '&nbsp;<button rel="tooltip" class="supprimer-cycle-link-ajax btn btn-danger"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
                   
                    //$("table tbody button:last").addClass("supprimer-cycle-link");
                    // alert(data.permissions.indexOf("cycles"));

                        index_model = data.permissions.indexOf("note")
                        /*if(data.permissions[index_model + 1] ==1 ){
                          nouvelle_ligne += view;
                        } */                     
                        if(data.permissions[index_model + 2] ==1 ){
                          nouvelle_ligne += change;
                        }  
                        //retirer le bouton add si pas de permission pour ajouter
                        // if(data.permissions[index_model + 3] ==0 ){
                        //   $("button .ajouter-cycle-link").remove();
                        // }                      
                        // if(data.permissions[index_model + 4] ==1 ){
                        //   nouvelle_ligne += del;
                        // }

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

    $(".ajouter-cycle-link").click(function() {

        $('#modal_ajouter_cycle').modal('show');

        $(".nom_cycle").removeAttr("disabled");
        $(".nom").removeAttr("disabled");
        $(".prenom").removeAttr("disabled");
        $(".age").removeAttr("disabled");

        $(".nom_cycle").val("");
        $(".nom").val("");
        $(".prenom").val("");
        $(".age").val("");

    });*/

    // $("body").on("click", ".ajouter-cycle-link", function() {
        
    //     $('#modal_ajouter_cycle').modal('show');

    //     $(".nom_cycle").val(nom_cycle);
    //     $(".nom_sousetab").val(nom_sousetab);
    //     $(".nom_etab").val(nom_etab);
    //     $("#id_modif").val(id);

    //     $(".nom_cycle").val("");
    //     $(".nom_sousetab").val("");
    //     $(".nom_etab").val("");

    // });

    // $(".detail-cycle-link-td").click(function() {
//      $("body").on("click", ".detail-cycle-link-td", function() {
// //class="{{ cycl.id }}²²{{ cycl.nom_cycle }}²²{{ cycl.sous_cycle }}²²{{ cycl.cycle }}"
//         $('#modal_detail_cycle').modal('show');

//         var classe = $(this).parents("tr").attr('class');
//         tab_element = classe.split("²²");
//         id = tab_element[0];
//         nom_cycle = tab_element[1];
//         nom_sousetab = tab_element[2];
//         nom_etab = tab_element[3];
      
//         $(".nom_cycle").val(nom_cycle);
//         $(".nom_sousetab").val(nom_sousetab);
//         $(".nom_etab").val(nom_etab);
//         $("#id_modif").val(id);

//         $(".nom_cycle").attr("disabled", "True");
//         $(".nom_sousetab").attr("disabled", "True");
//         $(".nom_etab").attr("disabled", "True");

//     });

    $(".modifier-saisie-note-link").click(function() {
        $('#modal_modifier_saisie_notes').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        // id+'²²'+ nom_sousetab+ '²²'+ libelle+ '²²'+ is_active+ '²²'+ date_deb_saisie +'²²'+ date_deb_saisie
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        libelle = tab_element[2];
        is_active = tab_element[3];
        date_deb_saisie = tab_element[4];
        date_fin_saisie = tab_element[5];

        if (is_active.toString() == "True")
          $(".activer").prop("checked", true);
        else 
          $(".activer").prop("checked", false);
        $(".evaluation").val(id);
        $(".libelle").val(libelle);
        $(".date_deb_saisie1").val(date_deb_saisie);
        $(".date_fin_saisie1").val(date_fin_saisie);
        $(".nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);
        
        $(".date_deb_saisie_label").addClass("is-focused");
        $(".date_fin_saisie_label").addClass("is-focused");

        // $(".nom_cycle").removeAttr("disabled");
        // $(".nom_sousetab").removeAttr("disabled");
        // $(".nom_etab").removeAttr("disabled");

    });



    // $(".supprimer-cycle-link").click(function() {

    //   $('#modal_supprimer_cycle').modal('show');

    //   var classe = $(this).parents("tr").attr('class');
    //   tab_element = classe.split("²²");
    //   /*nom_etab = tab_element[0];
    //   nom_sousetab = tab_element[1];
    //   nom_cycle = tab_element[2];
    //   id = tab_element[3];*/
    //   id = tab_element[0];
    //   nom_cycle = tab_element[1];
    //   nom_sousetab = tab_element[2];
    //   nom_etab = tab_element[3];
      
    //   $("#id_supp").val(id);
    //   $("#modal_supprimer_cycle .nom_cycle").text(nom_cycle);
    //   $("#modal_supprimer_cycle .nom_sousetab").text(nom_sousetab);
    //   $("#modal_supprimer_cycle .nom_etab").text(nom_etab);
    
    // });

    $("#nbre_element_par_page").change(function (e) {

        e.stopImmediatePropagation(); 
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_periodes");
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

       var sousetab_recherche = $("#sousetab_recherche").val();

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + sousetab_recherche ;

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
      
/*    $("body").on("click", ".supprimer-cycle-link-ajax", function() {
        
        $('#modal_supprimer_cycle').modal('show');

         var classe = $(this).parents("tr").attr('class');
          tab_element = classe.split("²²");
          id = tab_element[0];
          nom_cycle = tab_element[1];
          nom_sousetab = tab_element[2];
          nom_etab = tab_element[3];
          age = tab_element[4];
          bp = tab_element[5];
          email = tab_element[6];
          tel = tab_element[7];
          devise = tab_element[8];
          langue = tab_element[9];
          annee_scolaire = tab_element[10];
          site_web = tab_element[11];
          
          $("#id_supp").val(id);
          $("#modal_supprimer_cycle .nom_cycle").text(nom_cycle);
          $("#modal_supprimer_cycle .nom_sousetab").text(nom_sousetab);
          $("#modal_supprimer_cycle .nom_etab").text(nom_etab);
          // $("#modal_supprimer_cycle .id").text(id);
          $("#modal_supprimer_cycle .bp").text(bp);
          $("#modal_supprimer_cycle .email").text(email);
          $("#modal_supprimer_cycle .tel").text(tel);
          $("#modal_supprimer_cycle .devise").text(devise);
          $("#modal_supprimer_cycle .langue").text(langue);
          $("#modal_supprimer_cycle .annee_scolaire").text(annee_scolaire);
          $("#modal_supprimer_cycle .site_web").text(site_web);

    });*/


    $("body").on("click", ".modifier-saisie-note-link-ajax", function() {
        
        $('#modal_modifier_saisie_notes').modal('show');
        var classe = $(this).parents("tr").attr('class');
        // alert(classe);
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_sousetab = tab_element[1];
        libelle = tab_element[2];
        is_active = tab_element[3];
        date_deb_saisie = tab_element[4];
        date_fin_saisie = tab_element[5];

        if (is_active.toString() == "true")
          $(".activer").prop("checked", true);
        else 
          $(".activer").prop("checked", false);
        $(".evaluation").val(id);
        $(".libelle").val(libelle);
        $(".date_deb_saisie1").val(date_deb_saisie);
        $(".date_fin_saisie1").val(date_fin_saisie);
        $(".nom_sousetab").val(nom_sousetab);
        $("#id_modif").val(id);

        $(".date_deb_saisie_label").addClass("is-focused");
        $(".date_fin_saisie_label").addClass("is-focused");


    });


      
  /*  $("body").on("click", ".detail-cycle-link-ajax", function() {
        $('#modal_detail_cycle').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        nom_cycle = tab_element[1];
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

        $(".nom_etab").val(nom_cycle);
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

          var form = $(".recherche_periodes");
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
 

          var sousetab_recherche = $("#sousetab_recherche").val();

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + sousetab_recherche ;

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
        // alert("enfin...")
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " ";

        var form = $(".recherche_periodes");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class").split(" ")[0];
        
        // alert(url_action);
        $(this).attr("class", trier_par + " tri tri-desc");
        url_action = '/mainapp/recherche-eleve3/';
      
        var sousetab_recherche = $("#sousetab_recherche").val();

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + sousetab_recherche ;

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

        var form = $(".recherche_periodes");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class").split(" ")[0];
        

        $(this).attr("class", trier_par + " tri tri-asc");


        // tri decroissant 
        trier_par = "-" + trier_par;
      
        var sousetab_recherche = $("#sousetab_recherche").val();

        var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + sousetab_recherche ;

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
