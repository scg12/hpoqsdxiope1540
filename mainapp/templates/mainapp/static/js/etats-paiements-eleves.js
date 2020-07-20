data_received = [];
donnes_imprimer = "";
$(document).ready(function(){

$(".div_etats").prop('hidden',true);
$(".order_by_div").prop('hidden',true);
$(".imprimer").prop('hidden',true);

$("body").on("click", "#voir_paiements_associes", function() {
  // alert("j'arrive");
  fini = false;

  genre = $(".genre").val();
  etats = $(".etats").val();
  date_deb = $(".date_deb").val().replace("/","-");
  date_fin = $(".date_fin").val().replace("/","-");
  order_by = $(".order_by").val();
  n1 = date_deb.split("-").length - 1
  n2 = date_fin.split("-").length - 1
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

  if (n1 == 2 && n2 == 2 && date_deb > date_fin){
    alert("Date Début doit être inférieur à Date Fin");
    fini = true;
  }
  position = "0";

    if (!fini)
    {
    passe = 0
    etab = $(".choix_etab").val().split("_")[0];
    id_etab = $(".choix_etab").val().split("_")[1];
    
    sousetab = $(".choix_sousetab").val().split("_")[0];
    id_sousetab = $(".choix_sousetab").val().split("_")[1];
    // alert(id_etab+" "+id_sousetab);
    if (id_sousetab == "all")
    {
      niveau_recherche = 1
      donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + etab + "²²~~" + id_etab;
      // 5 + 5 = 10 params
    }
    else {
      cycle = $(".choix_cycle").val().split("_")[0];
      id_cycle = $(".choix_cycle").val().split("_")[1];
      if (id_cycle == "all")
        {
          niveau_recherche = 2
          donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + sousetab  + "²²~~" + id_sousetab;
          // 5 + 5 = 10 params
        }
      else{
        niveau = $(".choix_niveau").val().split("_")[0];
        id_niveau = $(".choix_niveau").val().split("_")[1];
        if (id_niveau == "all")
          {
            niveau_recherche = 3
            // On a ajouté sousetab et id_sousetab
            donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + cycle  + "²²~~" + id_cycle + "²²~~" + sousetab  + "²²~~" + id_sousetab;
            // 5 + 5 = 10 params
            
          }
        else{
          passe = 1;
          specialite = $(".specialite").val().split("_")[0];
          id_specialite = $(".specialite").val().split("_")[1];
          classes = $(".choix_classes").val();
          // classes_selected = $(".choix_classes").children("option:selected").val();
          nbre_classes = $(".choix_classes").children("option").length;
          nbre_classes_selected = $(".choix_classes").children("option:selected").length;

          if (nbre_classes > 0 && nbre_classes_selected == nbre_classes)
            equal = "yes";
          else equal = "no"
          // alert(nbre_classes+" -- "+nbre_classes_selected);
          // if (id_specialite == "all")
            {
              niveau_recherche = 4
              donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + niveau  + "²²~~" + id_niveau + "²²~~" + specialite  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal+ "²²~~" +nbre_classes+ "²²~~" + nbre_classes_selected;
              // ligne ajoutée
              donnees += "²²~~" + sousetab + "²²~~" + id_sousetab + "²²~~" + cycle + "²²~~" + id_cycle
            // 11 + 5 = 16 params 
            }
        }
      }
    }
    sens_tri = $(".sens_tri").val();
    var form = $(".load_etats_paiements_eleves");
    var url_action = form.attr("action");
    // 5 params suppémentaires
    // if (passe == 0)
      donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + sens_tri;
    // else
    //   donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + sens_tri+ "²²~~" + id_sousetab;

    // alert(niveau_recherche+" -- "+donnees);
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
 }

});
$("body").on("change", ".etats", function() {
  if($(this).val() == "previsions")
    $(".order_by_div").prop('hidden',true);
  else{
    $(".order_by_div").removeAttr('hidden');
    position = "6"
    var donnees = position + "²²~~" + 1 + "²²~~" +  $(this).val() + "²²~~rien";
    var form = $(".load_etats_paiements_eleves");
    var url_action = form.attr("action");
    // alert("ici");
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
  }


});

$("body").on("click", ".imprimer", function() {
  // alert(donnees_imprimer);

  // var form = $(".load_etats_paiements_eleves");
  //         var url_action = form.attr("action");

  //          $.ajax({
  //              method: 'POST',
  //              url: url_action,
  //              data: {
  //                form_data : donnees_imprimer,
  //                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
  //              },
  //              success: gererSucces,
  //              error: gererErreur,
  //          });
});

$("body").on("click", ".afficher", function() {
  $(this).prop('disabled',true);
  $(".imprimer").prop('hidden',true);
  $("table thead tr").remove();
  $("table tbody tr").remove();
  $("table tfoot tr").remove();
  $("table").prop('hidden',true);
  etab = $(".choix_etab").val();
  sousetab = $(".choix_sousetab").val();
  cycle = $(".choix_cycle").val();
  niveau = $(".choix_niveau").val();
  specialite = $(".specialite").val();
  classes = $(".choix_classes").val();
  nbre_classes = $(".choix_classes").children("option").length;
  nbre_classes_selected = $(".choix_classes").children("option:selected").length;

  genre = $(".genre").val();
  etats = $(".etats").val();
  date_deb = $(".date_deb").val().replace("/","-");
  date_fin = $(".date_fin").val().replace("/","-");
  order_by = $(".order_by").val();
  sens_tri = $(".sens_tri").val();
  n1 = date_deb.split("-").length - 1
  n2 = date_fin.split("-").length - 1
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

  if (n1 == 2 && n2 == 2 && date_deb > date_fin){
    alert("Date Début doit être inférieur à Date Fin");
    fini = true;
  }
  else{
    donnees_imprimer = etab +"²²~~"+ sousetab +"²²~~"+cycle +"²²~~"+niveau +"²²~~"+specialite +"²²~~"+classes +"²²~~"+nbre_classes +"²²~~"+nbre_classes_selected +"²²~~"+genre +"²²~~"+etats +"²²~~"+date_deb +"²²~~"+date_fin +"²²~~"+order_by +"²²~~"+sens_tri;
  $(".donnees_imprimer").val(donnees_imprimer);
  }

  // genre = $(".genre").val();
  // etats = $(".etats").val();
  // date_deb = $(".date_deb").val();
  // date_fin = $(".date_fin").val();
  
  

    var form = $(".load_etats_paiements_eleves");
    var url_action = form.attr("action");
    position = "7"
    var donnees = "";
    fini = false;
    // niveau_recherche permet de savoir si la recherche est pr ts les sousetabs, cycle, niveau, spe, classes
    // niveau_recherche == 1 si id_sousetab == all
    // niveau_recherche == 2 si id_cycle == all
    // niveau_recherche == 3 si id_niveau == all
    // niveau_recherche == 4 sinon

    // alert(date_deb+" -- "+date_fin);
  if (!fini)
    {
    etab = $(".choix_etab").val().split("_")[0];
    id_etab = $(".choix_etab").val().split("_")[1];
    passe = 0
    sousetab = $(".choix_sousetab").val().split("_")[0];
    id_sousetab = $(".choix_sousetab").val().split("_")[1];
    // alert(id_etab+" "+id_sousetab);
    if (id_sousetab == "all")
    {
      niveau_recherche = 1
      donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + etab + "²²~~" + id_etab;
      // 5 + 5 = 10 params
    }
    else {
      cycle = $(".choix_cycle").val().split("_")[0];
      id_cycle = $(".choix_cycle").val().split("_")[1];
      if (id_cycle == "all")
        {
          niveau_recherche = 2
          donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + sousetab  + "²²~~" + id_sousetab;
          // 5 + 5 = 10 params
        }
      else{
        niveau = $(".choix_niveau").val().split("_")[0];
        id_niveau = $(".choix_niveau").val().split("_")[1];
        if (id_niveau == "all")
          {
            niveau_recherche = 3
            donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + cycle  + "²²~~" + id_cycle;
            // 5 + 5 = 10 params
            
          }
        else{
          passe = 1
          specialite = $(".specialite").val().split("_")[0];
          id_specialite = $(".specialite").val().split("_")[1];
          classes = $(".choix_classes").val();
          // classes_selected = $(".choix_classes").children("option:selected").val();
          nbre_classes = $(".choix_classes").children("option").length;
          nbre_classes_selected = $(".choix_classes").children("option:selected").length;

          if (nbre_classes > 0 && nbre_classes_selected == nbre_classes)
            equal = "yes";
          else equal = "no"
          // alert(nbre_classes+" -- "+nbre_classes_selected);
          // if (id_specialite == "all")
            {
              niveau_recherche = 4
              donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + niveau  + "²²~~" + id_niveau + "²²~~" + specialite  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal+ "²²~~" +nbre_classes+ "²²~~" + nbre_classes_selected;
            // 11 + 5 = 16 params 
            }
        }
      }
    }
    sens_tri = $(".sens_tri").val();
    // 5 params suppémentaires
    if (passe == 0)
      donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + sens_tri;
    else
      donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + sens_tri+ "²²~~" + id_sousetab;
    // alert(niveau_recherche+" -- "+donnees);
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
 }
});

$(".afficher_cacher_criteres_recherche").on("click", function(){
   if ($(".afficher_criteres").val() == "yes"){
      $(".div_etats").prop('hidden',true);
      $(".afficher_criteres").val("no");
      $(".afficher_cacher_criteres_recherche").text("Afficher Critères Recherche");
   }
   else{
      $(".div_etats").removeAttr('hidden');
      $(".afficher_criteres").val("yes");
      $(".afficher_cacher_criteres_recherche").text("Masquer Critères Recherche");

   }
});

$(".choix_etab").on("change", function(){
  // On met la variable position à 1 pour indiquer que c'est etab qui a changé

    etab = $('.choix_etab').val()
    position = "1";
    id_etab = etab.split("_")[1];
    etab = etab.split("_")[0];

    var form = $(".load_etats_paiements_eleves");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_etab + "²²~~" + etab + "²²~~" + id_etab;

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
          var form = $(".load_etats_paiements_eleves");
          var url_action = form.attr("action");
          var donnees = position + "²²~~" + id_sousetab + "²²~~" + sousetab + "²²~~" + id_etab;

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

        var form = $(".load_etats_paiements_eleves");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_cycle + "²²~~" + cycle + "²²~~" + id_sousetab;

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
          // $('#liste_classes_niveaux').empty();
          $('.choix_classes').empty();
    }else{
        var form = $(".load_etats_paiements_eleves");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_niveau + "²²~~" + niveau + "²²~~" + id_cycle;

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
    }
    });

  $(".specialite").on("change", function(){
  // On met la variable position à 3 pour indiquer que c'est niveau qui a changé
    specialite = $('.specialite').val();
    id_niveau = $('.choix_niveau').val().split("_")[1];
    position = "5";
    // id_specialite = specialite.split("_")[1];
    specialite = specialite.split("_")[0];

        var form = $(".load_etats_paiements_eleves");
        var url_action = form.attr("action");
        var donnees = position + "²²~~" + id_niveau + "²²~~" + specialite + "²²~~" + id_niveau;
        // var donnees = data_received;
         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             /*data:{my_data : data_received,
              csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),},*/
             success: gererSucces,
             error: gererErreur,
         });
    // }

    });


function gererSucces(data){
  data_received = data;
  console.log(data_received);
  choix = data.choix;
  if (choix == "voir_paiements_associes"){
    $(".thead_type_paiement").empty();
    $(".tbody_type_paiement").empty();
    $(".tfoot_type_paiement").empty();

    nb_paiements = data.type_paiements_associes.length;
    liste_type_paiements_associes = data.type_paiements_associes;
    nouvelle_ligne = "<tr><th>Libellé</th><th>Montant</th><th>Date début</th><th>Date fin</th><th>Ordre paiement</th><th>S'applique a</th></tr>";
    $(".thead_type_paiement").append(nouvelle_ligne);
    nouvelle_ligne = "";
     for (var i = 0; i < nb_paiements; i++) {
      libelle = liste_type_paiements_associes[i].libelle;
      montant = liste_type_paiements_associes[i].montant;
      date_deb = liste_type_paiements_associes[i].date_deb;
      date_fin = liste_type_paiements_associes[i].date_fin;
      ordre_paiement = liste_type_paiements_associes[i].ordre_paiement;
      classe_display = liste_type_paiements_associes[i].classe_display;
      nouvelle_ligne += `<tr><td>${libelle}</td><td>${montant}</td><td>${date_deb}</td><td>${date_fin}</td><td>${ordre_paiement}</td><td>${classe_display}</td></tr>`;
     }
    $(".tbody_type_paiement").append(nouvelle_ligne);
    nouvelle_ligne = "<tr><th>Libellé</th><th>Montant</th><th>Date début</th><th>Date fin</th><th>Ordre paiement</th><th>S'applique a</th></tr>";
    $(".tfoot_type_paiement").append(nouvelle_ligne);
    $('#modal_type_paiement').modal('show');
             


  }
  if (choix == "eleves_tous"){
    $("#titre_etat").text("Apprenants en règle | pas en règle");
    $(".div_etats").prop('hidden',true);
    $(".afficher_cacher_criteres_recherche").text("Afficher Critères Recherche");
    $(".afficher_criteres").val("no");
    $("table").removeAttr('hidden');

    if(data.permissions.indexOf("typepayementeleve") == -1){
            $("table thead tr").remove();
            $("table tbody tr").remove();
            $("table tfoot tr").remove();


             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
      }
      else{
        nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Versé</b></th><th><b>Total</b></th><th><b>Reste</b></th><th><b>Excédent</b></th></tr>`;
      $("table thead").append(nouvelle_ligne);
      nouvelle_ligne = "";
      nb_eleves = data.info_eleves.length;
      liste_info_eleves = data.info_eleves;
      verses = 0;
      totaux = 0;
      restes = 0;
      excedents = 0;
      for (var i = 0; i < nb_eleves; i++) {
        matricule = liste_info_eleves[i].matricule;
        nom = liste_info_eleves[i].nom;
        prenom = liste_info_eleves[i].prenom;
        classe = liste_info_eleves[i].classe;
        paye = liste_info_eleves[i].verse;
        total = liste_info_eleves[i].total;
        reste = liste_info_eleves[i].reste;
        excedent = liste_info_eleves[i].excedent;
        verses += paye;
        totaux += total;
        restes += reste;
        excedents += excedent;
        if (reste == 0 && excedent > 0)
          nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${matricule}</b></td><td><b>${nom}</b></td><td><b>${prenom}</b></td><td><b>${classe}</b></td><td><b style=color:green;>${paye}</b></td><td><b>${total}</b></td><td><b>${reste}</b></td><td><b style=color:green;>${excedent}</b></td></tr>`;
        else if (reste == 0 && excedent == 0) {
          nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${matricule}</b></td><td><b>${nom}</b></td><td><b>${prenom}</b></td><td><b>${classe}</b></td><td><b style=color:green;>${paye}</b></td><td><b>${total}</b></td><td><b>${reste}</b></td><td><b>${excedent}</b></td></tr>`; 
        }
        else
          nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${matricule}</b></td><td><b>${nom}</b></td><td><b>${prenom}</b></td><td><b>${classe}</b></td><td><b>${paye}</b></td><td><b>${total}</b></td><td><b>${reste}</b></td><td><b>${excedent}</b></td></tr>`;


      }
      if (restes == 0)
        nouvelle_ligne += `<tr><th><b>#</b></th><th><b>TOTAL</b></th><th></th><th></th><th></th><th><b style=color:green;>${verses}</b></th><th><b>${totaux}</b></th><th><b style=color:green;>${restes}</b></th><th><b>${excedents}</b></th></tr>`;
      else
        nouvelle_ligne += `<tr><th></th><th><b>TOTAL</b></th><th></th><th></th><th></th><th><b style=color:green;>${verses}</b></th><th><b>${totaux}</b></th><th><b style=color:red;>${restes}</b></th><th><b>${excedents}</b></th></tr>`;

      $("table tbody").append(nouvelle_ligne);
        nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Versé</b></th><th><b>Total</b></th><th><b>Reste</b></th><th><b>Excédent</b></th></tr>`;
    $("table tfoot").append(nouvelle_ligne);
    }
  $(".afficher").removeAttr('disabled');
  $(".imprimer").removeAttr('hidden');
  }


  if (choix == "eleves_inscrits"){
    $("#titre_etat").text("Apprenants en règle");
    $(".div_etats").prop('hidden',true);
    $(".afficher_cacher_criteres_recherche").text("Afficher Critères Recherche");
    $(".afficher_criteres").val("no");
    $("table").removeAttr('hidden');

    if(data.permissions.indexOf("typepayementeleve") == -1){
            $("table thead tr").remove();
            $("table tbody tr").remove();
            $("table tfoot tr").remove();


             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
      }
      else{
        nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Total</b></th><th><b>Versé</b></th><th><b>Excédent</b></th></tr>`;

      $("table thead").append(nouvelle_ligne);
      nouvelle_ligne = "";
      nb_eleves = data.info_eleves.length;
      liste_info_eleves = data.info_eleves;
      totaux = 0;
      excedents = 0;
      verses = 0;
      for (var i = 0; i < nb_eleves; i++) {
        matricule = liste_info_eleves[i].matricule;
        nom = liste_info_eleves[i].nom;
        prenom = liste_info_eleves[i].prenom;
        classe = liste_info_eleves[i].classe;
        total = liste_info_eleves[i].total;
        verse = liste_info_eleves[i].verse;
        excedent = liste_info_eleves[i].excedent;
        totaux += total;
        excedents += excedent;
        verses += verse;
      nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${matricule}</b></td><td><b>${nom}</b></td><td><b>${prenom}</b></td><td><b>${classe}</b></td><td><b>${total}</b></td><td><b>${verse}</b></td><td><b>${excedent}</b></td></tr>`;
      }
      nouvelle_ligne += `<tr><th></th><th><b>TOTAL</b></th><th></th><th></th><th></th><th><b style=color:green;>${totaux}</b></th><th><b style=color:green;>${verses}</b></th><th><b style=color:green;>${excedents}</b></th></tr>`;

      $("table tbody").append(nouvelle_ligne);
        nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Total</b></th><th><b>Versé</b></th><th><b>Excédent</b></th></tr>`;
    $("table tfoot").append(nouvelle_ligne);
    }
  $(".afficher").removeAttr('disabled');
  $(".imprimer").removeAttr('hidden');
  }


   if (choix == "eleves_non_inscrits"){
    $("#titre_etat").text("Apprenants pas en règles");
    $(".div_etats").prop('hidden',true);
    $(".afficher_cacher_criteres_recherche").text("Afficher Critères Recherche");
    $(".afficher_criteres").val("no");
    $("table").removeAttr('hidden');

    if(data.permissions.indexOf("typepayementeleve") == -1){
            $("table thead tr").remove();
            $("table tbody tr").remove();
            $("table tfoot tr").remove();


             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
      }
      else{
        nouvelle_ligne = `<tr><th><b>#</b><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Versé</b></th><th><b>Reste</b></th><th><b>Total</b></th></tr>`;
      $("table thead").append(nouvelle_ligne);
      nouvelle_ligne = "";
      nb_eleves = data.info_eleves.length;
      liste_info_eleves = data.info_eleves;
      verses = 0;
      totaux = 0;
      restes = 0;
      for (var i = 0; i < nb_eleves; i++) {
        matricule = liste_info_eleves[i].matricule;
        nom = liste_info_eleves[i].nom;
        prenom = liste_info_eleves[i].prenom;
        classe = liste_info_eleves[i].classe;
        paye = liste_info_eleves[i].verse;
        total = liste_info_eleves[i].total;
        reste = total - paye
        verses += paye;
        totaux += total;
        restes += reste;

      nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${matricule}</b></td><td><b>${nom}</b></td><td><b>${prenom}</b></td><td><b>${classe}</b></td><td><b>${paye}</b></td><td><b>${reste}</b></td><td><b>${total}</b></td></tr>`;
      }
      nouvelle_ligne += `<tr><th></th><th><b>TOTAL</b></th><th></th><th></th><th></th><th><b style=color:green;>${verses}</b></th><th><b style=color:red;>${restes}</b></th><th><b>${totaux}</b></th></tr>`;

      $("table tbody").append(nouvelle_ligne);
        nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Matricule</b></th><th><b>Nom</b></th><th><b>Prénom</b></th><th><b>Classe</b></th><th><b>Versé</b></th><th><b>Reste</b></th><th><b>Total</b></th></tr>`;
    $("table tfoot").append(nouvelle_ligne);
    }
  $(".afficher").removeAttr('disabled');
  $(".imprimer").removeAttr('hidden');
  }


  if (choix == "previsions") {
    $("#titre_etat").text("Prévision et Existant");
    $(".div_etats").prop('hidden',true);
    $(".afficher_cacher_criteres_recherche").text("Afficher Critères Recherche");
    $(".afficher_criteres").val("no");

    montant_previsionnel = data.montant_previsionnel;
    montant_total_eleves = data.montant_total_eleves;
    taux_recouvrement = data.taux_recouvrement;
    excedent_total_eleves = data.excedent_total_eleves;
    nb_classes = data.info_classes.length;
    liste_info_classes = data.info_classes
    $("table").removeAttr('hidden');
    
    if(data.permissions.indexOf("typepayementeleve") == -1){
            $("table thead tr").remove();
            $("table tbody tr").remove();
            $("table tfoot tr").remove();


             nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
             $("table tbody").append(nouvelle_ligne);
      }
      else{
      
    nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Classe</b></th><th><b>Montant Prévisionnel</b></th><th><b>Montant Existant</b></th><th><b>Déficit</b></th><th><b>Taux de Recouvrement</b></th></tr>`;
    $("table thead").append(nouvelle_ligne);
    nouvelle_ligne = "";
    deficit = 0
    deficit_classe = 0
    for (var i = 0; i < nb_classes; i++) {
      classe = liste_info_classes[i].classe;
      montant_previsionnel_classe = liste_info_classes[i].montant_previsionnel_classe;
      montant_total_eleves_classe = liste_info_classes[i].montant_total_eleves_classe;
      taux_recouvrement_classe = liste_info_classes[i].taux_recouvrement_classe;
      deficit_classe = montant_previsionnel_classe - montant_total_eleves_classe
      deficit += deficit_classe
      nouvelle_ligne += `<tr><td><b>${i + 1}</b></td><td><b>${classe}</b></td><td><b>${montant_previsionnel_classe}</b></td><td><b>${montant_total_eleves_classe}</b></td><td><b>${deficit_classe}</b></td><td><b>${taux_recouvrement_classe}</b></td></tr>`;

    }
    if (montant_previsionnel > montant_total_eleves)
      nouvelle_ligne += `<tr><th><b></b></th><th><b>TOTAL</b></th><th><b style=color:green;>${montant_previsionnel}</b></th><th><b style=color:red;>${montant_total_eleves}</b></th><th><b style=color:red;>${deficit}</b></th><th><b style=color:red;>${taux_recouvrement}%</b></th></tr>`;
    else
      nouvelle_ligne += `<tr><th></th><th><b>TOTAL</b></th><th><b style=color:green;>${montant_previsionnel}</b></th><th><b style=color:green;>${montant_total_eleves}</b></th><th><b style=color:red;>${deficit}</b></th><th><b style=color:green;>${taux_recouvrement}%</b></th></tr>`;

    $("table tbody").append(nouvelle_ligne);
    nouvelle_ligne = `<tr><th><b>#</b></th><th><b>Classe</b></th><th><b>Montant Prévisionnel</b></th><th><b>Montant Existant</b></th><th><b>Déficit</b></th><th><b>Taux de Recouvrement</b></th></tr>`;
    $("table tfoot").append(nouvelle_ligne);

      }
  $(".afficher").removeAttr('disabled');
  $(".imprimer").removeAttr('hidden');

  }


  if (choix == "etab") { $(".afficher").removeAttr('disabled');
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
  if (choix == "sousetab") { $(".afficher").removeAttr('disabled');
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
  if (choix == "cycle") { $(".afficher").removeAttr('disabled');
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
  if (choix == "niveau") { $(".afficher").removeAttr('disabled');
          liste_specialites = data.specialites;
          nbre_specialites = liste_specialites.length;

          liste_classes = data.classes;
          nbre_classes = liste_classes.length;
          // alert($(".choix_niveau").val())
          id_niveau = $(".choix_niveau").val().split('_')[1]
          $('.specialite').empty();
          $('.choix_classes').empty();
          if (nbre_specialites != 0)
            $('.specialite').append(`<option value=tous_${id_niveau}>Toutes`);
          $('.specialite').append(`<option value=aucune_${id_niveau}>Sans spécialité`);
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

          if (nbre_classes == 0)
            $(".afficher").prop('disabled', true);
          else
            $(".afficher").removeAttr('disabled');
          
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

     if (choix == "order_by") {
        $(".order_by").empty();
        // alert("order_by");
        liste_order_by = data.order_by;
        nbre_order_by = liste_order_by.length;
        
         for (var i = 0; i < nbre_order_by; i++) {
            order_by = liste_order_by[i]                     
            // id = liste_sousetabs[i].id;
            // option = nom_sousetab+"_"+id;
            $('.order_by').append(`<option value="${order_by}"> 
                                       ${order_by} 
                                  </option>`);
          }
     }


}

function gererErreur(error) {
$("#message").text(error);
console.log(error);
}

});