$(document).ready(function(){
$('.valider').prop("disabled", true);
$(".terminer").prop("disabled", true);
$(".boutons_terminer").prop("hidden", true);

$("body").on("click", ".terminer", function() {
  $("input[son]").removeAttr("disabled");
  // $(".mode_saisie").removeAttr("disabled");
  $(".definition_division_temps").submit();
  $(".terminer").prop("disabled", true);
  $(".annuler").prop("disabled", true);

 });

 $("body").on("click", ".ajouter-divisiontemps-link", function() {
      
      $('#modal_detail_lesdivisiontemps').modal('show');
      $(".hierarchie_liste div:gt(3)").remove();
      $(".boutons_valider").removeAttr("hidden");
      $('.valider').prop("disabled", true);
      $(".boutons_terminer").prop("hidden", true);
      $(".terminer").prop("disabled", true);

      ligne = `<div class="col-sm-12 col-md-4">
                 <label for="2" class="bmd-label-floating hierarchie_suivante "><b><a href="#" style="color :#506ce9;">Hiérarchie2--></a></b></label>
               </div>`;
      $(".hierarchie_liste").append(ligne);
      // $(".appellation_bull").val("");
      // $(".hierarchie1").val("");   
      $(".info_divisionstemps").empty();
      // $('#modal_detail_lesdivisiontemps').modal({backdrop: 'static', keyboard: false});

  });

$("body").on("click", ".valider", function() {
  $(".hierarchie_suivante").prop("hidden", true);
  // alert($("input[son]").val());
  $("input[son]").prop("disabled", true);
  // $(".mode_saisie").prop("disabled", true);
  $(".boutons_valider").prop("hidden", true);
  $(".boutons_terminer").removeAttr("hidden");
  nbre_hierarchie = parseInt($("#nb_hierarchies").val());
  // alert(nbre_hierarchie);
  if (nbre_hierarchie == 2)
      $(".terminer").removeAttr("disabled");
  else 
      $(".terminer").prop("disabled",true);



  // nbre_mode commence à 1 et nbre_hierarchie à 2
  indice = 2;
  nbre_hierarchie = parseInt($("#nb_hierarchies").val());
  nbre_mode = nbre_hierarchie - 1;
  // $("#nb_hierarchies").val(nbre_hierarchie);
  ligne = "";
  prec = 2;
  suiv = 3;
  k = 0;
  p=0;
  fin = 0;

for (var i = 2; i <= nbre_hierarchie; i++) {
    nom_hierarchie_division_temps_suiv ="";
    nom_hierarchie_division_temps = $(".hierarchie"+i).val();
    nbre_hierarchie_division_temps = $(".nombre_hierarchie"+i).val();
    // mode_hierarchie_division_temps = $(".mode"+i).val();

  // alert(nom_hierarchie_division_temps+" _ "+nbre_hierarchie_division_temps+" _ "+mode_hierarchie_division_temps);
  if (nbre_mode == 1){
    for (var j = 1; j <= nbre_hierarchie_division_temps ; j++) {
      ligne += ` <div class="col-sm-12 col-md-4">
                  <label for="2" class="bmd-label-floating "><b style="color :#506ce9;">${nom_hierarchie_division_temps}${j}</b></label>
               </div>
               
               <div class="col-md-1">
               </div>
               <div class="col-sm-12 col-md-2">
                   <div class="input-group form-control-md">
                      <div class="form-group bmd-form-group ">
                      <label for="appellation_b" class="bmd-label-floating">date deb</label>
                      <input type="text" name="date_deb_${j}" class="form-control form-group">
                    </div>
                   </div>
               </div>
               <div class="col-sm-12 col-md-2">
                   <div class="input-group form-control-md">
                      <div class="form-group bmd-form-group ">
                      <label for="appellation_b" class="bmd-label-floating">date fin</label>
                      <input type="text" name="date_fin_${j}" class="form-control form-group">
                    </div>
                   </div>
               </div>`;
    }
   }
  else if (nbre_mode > 1) {
    if (i <= nbre_hierarchie - 1 ){
      nom_hierarchie_division_temps_suiv = $(".hierarchie"+(i+1)).val();
     if (i>=4) {
        p++;
        k+=p+1
     }
      
    
    for (var j = 1; j <= nbre_hierarchie_division_temps ; j++) {
        ligne += `<div class="col-sm-12 col-md-4">
                      <label for="2" class="bmd-label-floating "><b style="color :#506ce9;">${nom_hierarchie_division_temps}${j}</b></label>
                      <label for="2" class="bmd-label-floating "><b>&nbsp;&nbsp;# ${nom_hierarchie_division_temps_suiv}(s)</b></label>
                   </div>
                   
                   <div class="col-sm-12 col-md-1">
                      <div class="input-group form-control-md">
                          <div class="form-group bmd-form-group ">
                       <input sa type="number" min="1" name="nbrehierarchie_${j+k}" nbre="${i}" class="form-group form-control">
                          </div>
                       </div>
                   </div>
                   <div class="col-sm-12 col-md-2">
                       <div class="input-group form-control-md">
                          <div class="form-group bmd-form-group ">
                          <label for="appellation_b" class="bmd-label-floating">date deb</label>
                          <input type="text" name="date_deb_${j+k}" class="form-control form-group">
                        </div>
                       </div>
                   </div>
                   <div class="col-sm-12 col-md-2">
                       <div class="input-group form-control-md">
                          <div class="form-group bmd-form-group ">
                          <label for="appellation_b" class="bmd-label-floating">date fin</label>
                          <input type="text" name="date_fin_${j+k}" class="form-control form-group">
                        </div>
                       </div>
                   </div>`;
                   fin = j + k;
    }
    k++;
  } else if (i == nbre_hierarchie ) {
    // k += 2+p;
    fin++;
    var t = 1;
    var limit = parseInt(fin) + parseInt(nbre_hierarchie_division_temps);
    // var limit = fin+nbre_hierarchie_division_temps;
    // alert(fin+"  "+ limit);
    for (var j = fin; j < limit  ; j++) {
        ligne += ` <div class="col-sm-12 col-md-4">
                  <label for="2" class="bmd-label-floating "><b style="color :#506ce9;">${nom_hierarchie_division_temps}${t}</b></label>
               </div>
               
               <div class="col-md-1">
               </div>
               <div class="col-sm-12 col-md-2">
                   <div class="input-group form-control-md">
                      <div class="form-group bmd-form-group ">
                      <label for="appellation_b" class="bmd-label-floating">date deb</label>
                      <input type="text" name="date_deb_${j}" class="form-control form-group">
                    </div>
                   </div>
               </div>
               <div class="col-sm-12 col-md-2">
                   <div class="input-group form-control-md">
                      <div class="form-group bmd-form-group ">
                      <label for="appellation_b" class="bmd-label-floating">date fin</label>
                      <input type="text" name="date_fin_${j}" class="form-control form-group">
                    </div>
                   </div>
               </div>`;
      t++;
    }
   }
    k++;

  }
}
  $(".info_divisionstemps").append(ligne);
});

$("body").on("click", "input[sa]", function() {
  $("input[sa]").trigger("keyup");
});

$("body").on("keyup", "input[sa]", function() {
  nbre_input_text_vide = 0;
  nbre_input_text = $("input[sa]").length;
  $("input[sa]").each(function(){
      nbre_input_text_vide = nbre_input_text_vide+($.trim($(this).val())=="" ? 1 : 0);
  });

  // nbre_hierarchie = $('.mode_saisie').length + 1;
  nbre_hierarchie = $("#nb_hierarchies").val();
  fini = false;
  i = 2;
  while (i < nbre_hierarchie && fini == false) {
  
    nbre_hierarchie_division_temps = $(".nombre_hierarchie"+(i+1)).val();
    total = 0;
    $("input[nbre="+i+"]").each(function(){
      if ($(this).val() != "")
        total = total + parseInt($(this).val());
    });
    if (total != parseInt(nbre_hierarchie_division_temps))
      fini = true;
    // console.log(total, parseInt(nbre_hierarchie_division_temps), fini);
    i++;
  }


   if (nbre_input_text_vide == 0 && fini == false)
     $('.terminer').removeAttr("disabled");
   else $('.terminer').prop("disabled", true);
});

$("body").on("click", "input[son]", function() {
  $("input[son]").trigger("keyup");
});

 $("body").on("keyup", "input[son]", function() {
  // nbre_mode = $("#nb_hierarchies").val() -1;
  nbre_input_text_vide = 0;
  nbre_input_text = $("input[son]").length;
  $("input[son]").each(function(){
      nbre_input_text_vide = nbre_input_text_vide+($.trim($(this).val())=="" ? 1 : 0);
  });

  if (nbre_input_text_vide == 0)
     $('.valider').removeAttr("disabled");
  else $('.valider').prop("disabled", true);
  
  /*if (nbre_mode == 1){
    current_mode = $(".mode2").val();

      if (current_mode == "saisi")
        if (nbre_input_text_vide == 0)
          $('.valider').removeAttr("disabled");
        else $('.valider').prop("disabled", true);
      else $('.valider').prop("disabled", true);
    }
  else if (nbre_mode > 1) {
   mode_saisie = $('.mode_saisie:last').val();
   nbre_mode_en_saisie = 0;
    $(".mode_saisie").each(function(){
        nbre_mode_en_saisie = nbre_mode_en_saisie+($.trim($(this).val())=="saisi" ? 1 : 0);
    });
   // console.log(mode_saisie, nbre_mode_en_saisie);
    if (nbre_mode_en_saisie == 1 && mode_saisie == "saisi" && nbre_input_text_vide == 0)
       $('.valider').removeAttr("disabled");
    else $('.valider').prop("disabled", true);
    // console.log(mode_saisie);
  }*/
 });

 $("body").on("change", ".mode_saisie", function() {
    nbre_mode = $('.mode_saisie').length;
    current_mode = $(this).val()
    nbre_input_text_vide = 0;
    $("input[son]").each(function(){
        nbre_input_text_vide = nbre_input_text_vide+($.trim($(this).val())=="" ? 1 : 0);
    });
    nbre_input_text = $("input[son]").length;

    if (nbre_mode == 1){
      if (current_mode == "saisi")
        if (nbre_input_text_vide == 0)
          $('.valider').removeAttr("disabled");
        else $('.valider').prop("disabled", true);
      else $('.valider').prop("disabled", true);
    }
    else if (nbre_mode > 1) {
    nbre_mode_en_saisie = 0;
    $(".mode_saisie").each(function(){
        nbre_mode_en_saisie = nbre_mode_en_saisie+($.trim($(this).val())=="saisi" ? 1 : 0);
    });
    mode_saisie = $('.mode_saisie:last').val();
    if (nbre_mode_en_saisie == 1 && mode_saisie == "saisi" && nbre_input_text_vide == 0)
       $('.valider').removeAttr("disabled");
    else $('.valider').prop("disabled", true);
    // console.log(nbre_mode_en_saisie);
  }
    // nbre_input_text_vide = $("input[son]").filter('[value=""]').length;
    // alert(nbre_input_text+" _ "+nbre_input_text_vide);

 });

  $("body").on("click", ".hierarchie_suivante", function() {
    $(this).prop("hidden", true);
    $('.valider').prop("disabled", true);
    // alert($(this).attr("for"));
    $("#nb_hierarchies").val($(this).attr("for"));
    prec_hierarchie = parseInt($(this).attr("for")) - 1;
    indice_hierarchie = prec_hierarchie + 1;
    suiv_hierarchie = indice_hierarchie + 1;
    
    ligne = `<div class="col-sm-12 col-md-4">
                <label for="hierarchie${indice_hierarchie}" class="bmd-label-floating"><b>Hiérarchie${indice_hierarchie}:</b></label>
                
               </div>
               <div class="col-sm-12 col-md-3">
                 <div class="input-group form-control-md">
                  <div class="form-group bmd-form-group ">
                  <label for="appellation_b_f" class="bmd-label-floating">Nom Bulletin hierarchie${indice_hierarchie}</label>
                  <input type="text" son name="hierarchie${indice_hierarchie}" class="form-control form-group hierarchie${indice_hierarchie}">
                </div>
                </div>
               </div>

              <div class="col-sm-12 col-md-1">
                 <div class="input-group form-control-md">
                  <div class="form-group bmd-form-group ">
                  <label for="appellation_b_f" class="bmd-label-floating">#</label>
                  <input type="number" son min="1" name="nombre_hierarchie${indice_hierarchie}" class="form-control form-group nombre_hierarchie${indice_hierarchie}">
                </div>
                </div>
              </div>

               <div class="col-sm-12 col-md-4">
               <!--  <button type="button" class="btn">hiérarchie2</button> -->
                 <label for="${suiv_hierarchie}" class="bmd-label-floating hierarchie_suivante "><b><a href="#" style="color :#506ce9;">Hiérarchie${suiv_hierarchie}--></a></b></label>
               </div>
             </div>`;
  $(".hierarchie_liste").append(ligne);
      
  });



});


  