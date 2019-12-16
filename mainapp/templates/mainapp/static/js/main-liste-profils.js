$(document).ready(function(){



   $(".recherche").keyup(function(event) {

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_profil");
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

            $("table tbody tr").remove();
            

              liste_profils = JSON.parse(data.profils);
           
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
              if (liste_profils.length < nbre_element_par_page){
                fin = parseInt(numero_page_active * liste_profils.length);
              }else{
                fin = parseInt(numero_page_active * nbre_element_par_page);
              }
              

      /* gere l'affichage des elements de la derniere page*/
              if (liste_page[liste_page.length-1] == numero_page_active){
                debut = (numero_page_active-1)*nbre_element_par_page; 
                fin = liste_profils.length;
              }
           
              if (liste_profils.length != 0){

                  for (var i = debut; i < fin; i++) {
                      //profil = JSON.parse(liste_profils[i]);alert("mon profil "+ liste_profils[i].photo_url);
                      id = liste_profils[i].id;
                      username = liste_profils[i].user.username;
                      last_name = liste_profils[i].user.last_name;
                      first_name = liste_profils[i].user.first_name;
                      groupe = liste_profils[i].user.groups;//alert(groupe+" ////");
                      
                      grp=""; 
                      grp_text=""; 

                      for (var j = 0; j < groupe.length; j++) {
                        
                        
                        if(j == groupe.length-1){
                          grp_text += groupe[j].name;
                          grp += '<span >'+groupe[j].name +'</span>';
                        }else{
                          grp_text += groupe[j].name +'$^^$';
                          grp += '<span >'+groupe[j].name +'</span>; ';
                        }
                        
                      }
                      
                      is_active = liste_profils[i].user.is_active;
                      telephone = liste_profils[i].telephone;
                      ville = liste_profils[i].ville;
                      quartier = liste_profils[i].quartier;
                      photo_url = liste_profils[i].photo_url;
                      

                    nouvelle_ligne = "<tr class='"+ id+'²²'+ username+ '²²'+ last_name +'²²'+ first_name +'²²' + grp_text+'²²'+ telephone + '²²'+ is_active+ '²²'+ ville + '²²'+ quartier+ '²²'+ photo_url  +"'>" + '<th scope="row" class="detail-profil-link-td">'+ (i+1) +
                    '</th><td class="detail-profil-link-td"><img class="photo img-raised" src="'+ photo_url +'" width="40px" height="40px"></td><td class="detail-profil-link-td">'+ username + '</td><td class="detail-profil-link-td">'+ last_name + '</td><td class="detail-profil-link-td">' + first_name + '</td><th class="detail-profil-link-td">'+ grp + '</th><td class="detail-profil-link-td">' + telephone + '</td><td class="detail-profil-link-td">' + is_active+ '</td>' + '<td class="td-actions text-right">'+
                    // '<button type="button" rel="tooltip" class="btn detail-profil-link" data-toggle="modal" data-target="#modal_detail_profil"><i class="material-icons">visibility</i></button>'+
                    '<button type="button" rel="tooltip" class="btn modifier-profil-link"><i class="material-icons">edit</i></button>'+
                    '&nbsp;<button rel="tooltip" class="btn btn-danger supprimer-profil-link"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
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
                  resultat_pagination += '<button class="btn btn-white btn-sm pagination-element" id="" disabled><i class="material-icons">arrow_back_ios</i></button>';
                }

                for (var num_page= 0; num_page < liste_page.length; num_page++) {

                    if (liste_page[num_page] == numero_page_active){
                     
                      resultat_pagination +='<button class="btn btn-sm pagination-element" id="'+liste_page[num_page]+'">'+ liste_page[num_page]+'</button>';
                    
                    }else{
                      
                      resultat_pagination +='<button class="btn btn-white btn-sm pagination-element" id="'+ liste_page[num_page] +'">'+ liste_page[num_page]+'</button>';
                      
                    }
                  
                }

                if(possede_page_suivante == true){
                  resultat_pagination += '<button class="btn btn-round btn-white btn-sm pagination-element" id="'+ suivant +'"><i class="material-icons">arrow_forward_ios</i></button>'
                }else{
                  resultat_pagination += '<button class="btn btn-round btn-white btn-sm pagination-element" id="" disabled><i class="material-icons">arrow_forward_ios</i></button>'
                }
            
                resultat_pagination += '</div>';

                $(".pagination").append(resultat_pagination);

              }
              else{
                /* aucun resultat de la recherche*/

                  nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Aucun utilisateur(s) ne correspond à votre recherche</td></tr>';                
                  
                  $("table tbody").append(nouvelle_ligne);

                  $(".pagination .contenu").remove();
              }

            //affiche le message en cas d'erreur
              if (data.message_resultat != ""){
                  $("#message").text(data.message_resultat).css('color',"red");
              }


          $(".sidebar").attr("data-color", data_color);
          $(".sidebar").addClass(sidebar_class);
          $(".btn").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
          $(".btn-rond").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);

      }

      function gererErreur(error) {
      $("#message").text(error);
      console.log(error);
      }

    $(".definir-groupe-link").click(function() {

        $('#modal_definir_groupe').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        username = tab_element[1];
        last_name = tab_element[2];
        first_name = tab_element[3];
        //email = tab_element[4];
        telephone = tab_element[5];
        is_active = tab_element[6];
        ville = tab_element[7];
        quartier = tab_element[8];
        photo_url = tab_element[9];


        $("#modal_detail_profil .username").text(username);
        $("#modal_detail_profil .last_name").text(last_name);
        $("#modal_detail_profil .first_name").text(first_name);
        $("#modal_detail_profil .telephone").text(telephone);
        $("#modal_detail_profil .is_active").text(is_active);
        $("#modal_detail_profil .ville").text(ville);
        $("#modal_detail_profil .quartier").text(quartier);
        $("#modal_detail_profil .photo").attr('src', photo_url);

        /*$("#modal_detail_profil .username").attr("disabled", "True");
        $("#modal_detail_profil .last_name").attr("disabled", "True");
        $("#modal_detail_profil .first_name").attr("disabled", "True");
        $("#modal_detail_profil .telephone").attr("disabled", "True");
        $("#modal_detail_profil .is_active").attr("disabled", "True");
        $("#modal_detail_profil .ville").attr("disabled", "True");
        $("#modal_detail_profil .quartier").attr("disabled", "True");*/

    });



    $("#nbre_element_par_page").change(function () {
        
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        numero_page = " "

        var form = $(".recherche_profil");
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


    $("body").on("click", ".ajouter-profil-link", function() {
        
        $('#modal_ajouter_profil').modal('show');

        $("#modal_ajouter_profil .user__username").removeAttr("disabled");
        $("#modal_ajouter_profil .user__last_name").removeAttr("disabled");
        $("#modal_ajouter_profil .user__first_name").removeAttr("disabled");
        $("#modal_ajouter_profil .telephone").removeAttr("disabled");
        $("#modal_ajouter_profil .user__is_active").removeAttr("disabled");
        $("#modal_ajouter_profil .ville").removeAttr("disabled");
        $("#modal_ajouter_profil .quartier").removeAttr("disabled");

        $("#modal_ajouter_profil .user__username").val("");
        $("#modal_ajouter_profil .user__last_name").val("");
        $("#modal_ajouter_profil .user__first_name").val("");
        $("#modal_ajouter_profil .telephone").val("");
        $("#modal_ajouter_profil .user__is_active").val("");
        $("#modal_ajouter_profil .ville").val("");
        $("#modal_ajouter_profil .quartier").val("");
        $(".label-group").addClass("is-focused");

    });


      
    $("body").on("click", ".supprimer-profil-link", function() {
        
        $('#modal_supprimer_profil').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        username = tab_element[1];
        last_name = tab_element[2];
        first_name = tab_element[3];
        groupe = tab_element[4];
        telephone = tab_element[5];
        is_active = tab_element[6];
        ville = tab_element[7];
        quartier = tab_element[8];
        photo_url = tab_element[9];

        groupes = groupe.split("$^^$");
        $("#modal_supprimer_profil #id_supp").val(id);
        $("#modal_supprimer_profil #tr_class").val(classe);
        $("#modal_supprimer_profil .user__username").val(username).trigger("change");
        $("#modal_supprimer_profil .user__last_name").val(last_name).trigger("change");
        $("#modal_supprimer_profil .user__first_name").val(first_name).trigger("change");
        $("#modal_supprimer_profil .telephone").val(telephone).trigger("change");
        $("#modal_supprimer_profil .user__is_active").val(is_active).trigger("change");
        $("#modal_supprimer_profil .ville").val(ville).trigger("change");

        $("#modal_supprimer_profil #suppression_groupe_liste_profil").children().remove();

        for (var i = 0; i < groupes.length; i++) {
          // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
          $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
        }

        $(".label-group").addClass("is-focused");

        $("#modal_supprimer_profil .quartier").val(quartier).trigger("change");
        $("#modal_supprimer_profil .photo").attr('src', photo_url);


          $("#modal_supprimer_profil .user__username").attr("disabled", "True");
          $("#modal_supprimer_profil .user__last_name").attr("disabled", "True");
          $("#modal_supprimer_profil .user__first_name").attr("disabled", "True");
          $("#modal_supprimer_profil .telephone").attr("disabled", "True");
          $("#modal_supprimer_profil .user__is_active").attr("disabled", "True");
          $("#modal_supprimer_profil .ville").attr("disabled", "True");
          // $("#modal_supprimer_profil .groupe").attr("disabled", "True");
          $("#modal_supprimer_profil .quartier").attr("disabled", "True");

    });



    $("body").on("click", ".modifier-profil-link", function() {
        
        $('#modal_modifier_profil').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        username = tab_element[1];
        last_name = tab_element[2];
        first_name = tab_element[3];
        groupe = tab_element[4];
        telephone = tab_element[5];
        is_active = tab_element[6];
        ville = tab_element[7];
        quartier = tab_element[8];
        photo_url = tab_element[9];

        groupes = groupe.split("$^^$");
        $("#modal_modifier_profil #id_modif").val(id);
        $("#modal_modifier_profil #tr_class").val(classe);
        $("#modal_modifier_profil .user__username").val(username).trigger("change");
        $("#modal_modifier_profil .user__last_name").val(last_name).trigger("change");
        $("#modal_modifier_profil .user__first_name").val(first_name).trigger("change");
        $("#modal_modifier_profil .telephone").val(telephone).trigger("change");
        $("#modal_modifier_profil .user__is_active").val(is_active).trigger("change");
        $("#modal_modifier_profil .ville").val(ville).trigger("change");

        $("#modal_modifier_profil #modification_groupe_liste_profil").children().remove();

        for (var i = 0; i < groupes.length; i++) {
          // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
          $("#modal_modifier_profil #modification_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
        }

        $(".label-group").addClass("is-focused");

        $("#modal_modifier_profil .quartier").val(quartier).trigger("change");
        $("#modal_modifier_profil .image-profil").attr('src', photo_url);

    });


      
    $("body").on("click", ".detail-profil-link", function() {
        
        $('#modal_detail_profil').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        username = tab_element[1];
        last_name = tab_element[2];
        first_name = tab_element[3];
        //email = tab_element[4];
        telephone = tab_element[5];
        is_active = tab_element[6];
        ville = tab_element[7];
        quartier = tab_element[8];
        photo_url = tab_element[9];

        $("#modal_detail_profil .user__username").val(username).trigger("change");
        $("#modal_detail_profil .user__last_name").val(last_name).trigger("change");
        $("#modal_detail_profil .user__first_name").val(first_name).trigger("change");
        $("#modal_detail_profil .telephone").val(telephone).trigger("change");
        $("#modal_detail_profil .user__is_active").val(is_active).trigger("change");
        $("#modal_detail_profil .ville").val(ville).trigger("change");
        $("#modal_detail_profil .quartier").val(quartier).trigger("change");
        $("#modal_detail_profil .photo").attr('src', photo_url);

        // $("#modal_detail_profil .user__username").attr("disabled", "True");
        // $("#modal_detail_profil .user__last_name").attr("disabled", "True");
        // $("#modal_detail_profil .user__first_name").attr("disabled", "True");
        // $("#modal_detail_profil .telephone").attr("disabled", "True");
        // $("#modal_detail_profil .user__is_active").attr("disabled", "True");
        // $("#modal_detail_profil .ville").attr("disabled", "True");
        // $("#modal_detail_profil .quartier").attr("disabled", "True");


    });


      
    $("body").on("click", ".detail-profil-link-td", function() {
        
        $('#modal_detail_profil').modal('show');

        var classe = $(this).parents("tr").attr('class');
        tab_element = classe.split("²²");
        id = tab_element[0];
        username = tab_element[1];
        last_name = tab_element[2];
        first_name = tab_element[3];
        groupe = tab_element[4];
        telephone = tab_element[5];
        is_active = tab_element[6];
        ville = tab_element[7];
        quartier = tab_element[8];
        photo_url = tab_element[9];

        groupes = groupe.split("$^^$");
        
        $(".label-group").addClass("is-focused");

        $("#modal_detail_profil #tr_class").val(classe);
        $("#modal_detail_profil .user__username").val(username).trigger("change");
        $("#modal_detail_profil .user__last_name").val(last_name).trigger("change");
        $("#modal_detail_profil .user__first_name").val(first_name).trigger("change");
        $("#modal_detail_profil .telephone").val(telephone).trigger("change");
        $("#modal_detail_profil .user__is_active").val(is_active).trigger("change");
        $("#modal_detail_profil .ville").val(ville).trigger("change");
        $("#modal_detail_profil .quartier").val(quartier).trigger("change");
        $("#modal_detail_profil .photo").attr('src', photo_url);

        $("#modal_detail_profil #detail_groupe_liste_profil").children().remove();
        for (var i = 0; i < groupes.length; i++) {
          // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
          $("#modal_detail_profil #detail_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
        }

        $("#modal_detail_profil .user__username").attr("disabled", "True");
        $("#modal_detail_profil .user__last_name").attr("disabled", "True");
        $("#modal_detail_profil .user__first_name").attr("disabled", "True");
        $("#modal_detail_profil .telephone").attr("disabled", "True");
        $("#modal_detail_profil .user__is_active").attr("disabled", "True");
        $("#modal_detail_profil .ville").attr("disabled", "True");
        $("#modal_detail_profil .quartier").attr("disabled", "True");


    });




    $("body").on("click", ".pagination-element", function() {

          var numero_page = $(this).attr('id');
          
          var nbre_element_par_page = $("#nbre_element_par_page").val();

          var recherche = $("#recherche").val().trim();

          var form = $(".recherche_profil");
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

    $("body").on("click", ".tri-asc", function(){
  
        $(".tri").find("img").attr("src", "/static/images/arrow.png");
        $(this).find("img").attr("src", "/static/images/up.png");
        
        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_profil");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class");
      

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

        $(this).attr("class","tri tri-desc");


    });


   $("body").on("click", ".tri-desc", function(){

        $(".tri").find("img").attr("src", "/static/images/arrow.png");
        $(this).find("img").attr("src", "/static/images/down.png");       

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_profil");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class");

        /* tri decroissant */
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

        $(this).attr("class","tri tri-asc");


    });



//previsualiser image profil

   function readURL(input) {

      if (input.files && input.files[0]) {
          var reader = new FileReader();

          reader.onload = function(e) {
            $('.image-profil').attr('src', e.target.result);
          }

          reader.readAsDataURL(input.files[0]);
      }
  }

  $(".file-image").change(function() {
      
      readURL(this);

      $(".modifier-image, .supprimer-image").show();
      $(".show-camera").hide();

   });

  // $('.image-profil').on("click", function(){
  //   $('.file-image').trigger('click');
  // });
  
var compteur = 0
  $(".select-image").click(function(e){
    //e.preventDefault();
    //$(".file-image").click();
    //$(".file-image").trigger("click");
    //e.stopImmediatePropagation();//use to stop click twice or more

          // if (compteur==0){
          //   alert(compteur);
          //   compteur++;
          // $(".file-image").unbind("click");
          //   $(".file-image").trigger('click');
          //   $(".file-image").unbind("click");
          //   $(".file-image").mouseup();
           
            

          // }else{
          //   alert(compteur);
          // }
  });


  
  // $(".file-image").on("click", function(e) {
    
  //         //e.preventDefault();
  //         alert("e = " + e);
          
  //        // e.stopPropagation();
         
          
  // });
//   $(".file-image").mouseup(function(e) {
//         e.preventDefault();
//          // alert("e = " + e);
//           alert("mouseup = ");
//          e.stopImmediatePropagation();
         
// });
// $("input").click(function(event){
//     alert("input clicked");
//     event.stopPropagation();
// });

  $(".modifier-image").on("click", function(e) {
    
          
          $(".show-camera").hide();
          $(".modifier-image, .supprimer-image").show();
         
          
  });


  $('.image-profil').on('load', function () {

       if($(".image-profil").attr('src') == "/static/assets/img/faces/profil.jpg"){

            $(".select-image").show();
            $(".modifier-image, .supprimer-image").hide();

        }else{
              $(".select-image").find("label").children("i").remove();
              $(".select-image").find("label").append('<i class="material-icons">edit</i>');
              $(".select-image, .supprimer-image").show();
              $(".show-camera").hide();
              
        }
        
  });


  $(".supprimer-image").on("click", function() {
          
          $('.image-profil').attr('src', "/static/assets/img/faces/profil.jpg");
          $(".select-image").find("label").children("i").remove();
          $(".select-image").find("label").append('<i class="material-icons">photo</i>');
          $(".select-image").show();
          $(".show-camera").show();
          $(this).hide();
          
  });


  $(".modifier-image, .supprimer-image, .take-snapshot, .retour-camera, .modifier-image-camera, .supprimer-image-camera").hide();


  //changer le curseur de la souris
  $('.detail-profil-link-td').css('cursor', 'pointer');

  $("body").on("hover", ".detail-profil-link-td", function(){

    $('.detail-profil-link-td').css('cursor', 'pointer');

  });


  $("body").on("click", ".show-camera", function() {
      
        // Configure a few settings and attach camera
        Webcam.set({
          width: 175,
          height: 175,
          image_format: 'jpeg',
          jpeg_quality: 100
         });
        Webcam.attach('#image_and_webcam');

      $(".take-snapshot, .retour-camera").show();
      // $('#modal_ajouter_profil .select-modif').hide();
      $(this).hide();
      $(".modifier-image, .supprimer-image, .select-image").hide();


  });

  $("body").on("click", ".supprimer-image-camera", function() {
      
        // Configure a few settings and attach camera
        Webcam.set({
          width: 200,
          height: 200,
          image_format: 'jpeg',
          jpeg_quality: 100
         });
        Webcam.attach('#image_and_webcam');

      $(".take-snapshot, .retour-camera").show();
      // $('#modal_ajouter_profil .select-modif').hide();
      $(this).hide();
      $(".modifier-image-camera").hide();
      $('#modal_ajouter_profil .webcam_photo').val("");

  });

  $("body").on("click", ".modifier-image-camera", function() {
      
        // Configure a few settings and attach camera
        Webcam.set({
          width: 200,
          height: 200,
          image_format: 'jpeg',
          jpeg_quality: 100
         });
        Webcam.attach('#image_and_webcam');

      $(".take-snapshot, .retour-camera").show();
      // $('#modal_ajouter_profil .select-modif').hide();
      $(this).hide();
      $(".supprimer-image-camera").hide();


  });

  $("body").on("click", ".retour-camera", function() {
      
      $(".take-snapshot, .retour-camera").hide();
      Webcam.reset();
      //Webcam.off();

      $(".select-image, .show-camera").show();
      $('#modal_ajouter_profil .webcam_photo').val("");
      $(this).hide();
      $("#image_and_webcam").children().remove();
      $("#image_and_webcam").append('<img class="image-profil img-raised" src="/static/assets/img/faces/profil.jpg"  width="175px" height="175px">');


  });


    $("body").on("click", ".take-snapshot", function() {
        
         // play camera sound effect
         jouerSonCamera();
        

         // take snapshot and get image data
         Webcam.snap( function(data_uri) {
         // display results in page
           $("#image_and_webcam").children().remove();
           $("#image_and_webcam").append('<img src="'+data_uri+'"'+ 'class="image-profil img-raised"' +'width= "175px" height="175px" />');

           $(".webcam_photo").val(data_uri);

         });

         $(".modifier-image-camera, .supprimer-image-camera").show();
         $(".take-snapshot, .retour-camera").hide();
         $(this).hide();
         


    });


    $("body").on("click", ".precedent-modal-modifier", function() {
            


      tr_class = $("#modal_modifier_profil #tr_class").val();

      $("table tbody tr").each(function(){
        
          if ($(this).attr('class')==tr_class){

              if($(this).prev().text()!= ""){

                classe = $(this).prev().attr('class');
              }else{
                classe = $("table tbody tr:last").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");
                $("#modal_modifier_profil #id_modif").val(id);
                $("#modal_modifier_profil #tr_class").val(classe);
                $("#modal_modifier_profil .user__username").val(username).trigger("change");
                $("#modal_modifier_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_modifier_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_modifier_profil .telephone").val(telephone).trigger("change");
                $("#modal_modifier_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_modifier_profil .ville").val(ville).trigger("change");

                $("#modal_modifier_profil #modification_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_modifier_profil #modification_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_modifier_profil .quartier").val(quartier).trigger("change");
                $("#modal_modifier_profil .image-profil").attr('src', photo_url);
              

          }
      });

      
    });


    $("body").on("click", ".suivant-modal-modifier", function() {


      tr_class = $("#modal_modifier_profil #tr_class").val();

      $("table tbody tr").each(function(){

          if ($(this).attr('class')==tr_class){

              if($(this).next().text()!= ""){

                classe = $(this).next().attr('class');
              }else{
                classe = $("table tbody tr:first").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");
                $("#modal_modifier_profil #id_modif").val(id);
                $("#modal_modifier_profil #tr_class").val(classe);
                $("#modal_modifier_profil .user__username").val(username).trigger("change");
                $("#modal_modifier_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_modifier_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_modifier_profil .telephone").val(telephone).trigger("change");
                $("#modal_modifier_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_modifier_profil .ville").val(ville).trigger("change");

                $("#modal_modifier_profil #modification_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_modifier_profil #modification_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_modifier_profil .quartier").val(quartier).trigger("change");
                $("#modal_modifier_profil .image-profil").attr('src', photo_url);

              
          }
      });


    });


    $("body").on("click", ".precedent-modal-detail", function() {
            


      tr_class = $("#modal_detail_profil #tr_class").val();

      $("table tbody tr").each(function(){
        
          if ($(this).attr('class')==tr_class){

              if($(this).prev().text()!= ""){

                classe = $(this).prev().attr('class');
              }else{
                classe = $("table tbody tr:last").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");

                $("#modal_detail_profil #tr_class").val(classe);
                $("#modal_detail_profil .user__username").val(username).trigger("change");
                $("#modal_detail_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_detail_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_detail_profil .telephone").val(telephone).trigger("change");
                $("#modal_detail_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_detail_profil .ville").val(ville).trigger("change");
                $("#modal_detail_profil .photo").attr('src', photo_url);

                $("#modal_detail_profil #detail_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_detail_profil #detail_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_detail_profil .quartier").val(quartier).trigger("change");
                $("#modal_detail_profil .image-profil").attr('src', photo_url);

              

          }
      });

      
    });


    $("body").on("click", ".suivant-modal-detail", function() {


      tr_class = $("#modal_detail_profil #tr_class").val();

      $("table tbody tr").each(function(){

          if ($(this).attr('class')==tr_class){

              if($(this).next().text()!= ""){

                classe = $(this).next().attr('class');
              }else{
                classe = $("table tbody tr:first").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");

                $("#modal_detail_profil #tr_class").val(classe);
                $("#modal_detail_profil .user__username").val(username).trigger("change");
                $("#modal_detail_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_detail_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_detail_profil .telephone").val(telephone).trigger("change");
                $("#modal_detail_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_detail_profil .ville").val(ville).trigger("change");
                $("#modal_detail_profil .photo").attr('src', photo_url);

                $("#modal_detail_profil #detail_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_detail_profil #detail_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_detail_profil .quartier").val(quartier).trigger("change");
                $("#modal_detail_profil .image-profil").attr('src', photo_url);

              
          }
      });


    });


    $("body").on("click", ".precedent-modal-supprimer", function() {
            


      tr_class = $("#modal_supprimer_profil #tr_class").val();

      $("table tbody tr").each(function(){
        
          if ($(this).attr('class')==tr_class){

              if($(this).prev().text()!= ""){

                classe = $(this).prev().attr('class');
              }else{
                classe = $("table tbody tr:last").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");

                $("#modal_supprimer_profil #tr_class").val(classe);
                $("#modal_supprimer_profil .user__username").val(username).trigger("change");
                $("#modal_supprimer_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_supprimer_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_supprimer_profil .telephone").val(telephone).trigger("change");
                $("#modal_supprimer_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_supprimer_profil .ville").val(ville).trigger("change");
                $("#modal_supprimer_profil .photo").attr('src', photo_url);

                $("#modal_supprimer_profil #suppression_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_supprimer_profil .quartier").val(quartier).trigger("change");
                $("#modal_supprimer_profil .image-profil").attr('src', photo_url);

              

          }
      });

      
    });


    $("body").on("click", ".suivant-modal-supprimer", function() {


      tr_class = $("#modal_supprimer_profil #tr_class").val();

      $("table tbody tr").each(function(){

          if ($(this).attr('class')==tr_class){

              if($(this).next().text()!= ""){

                classe = $(this).next().attr('class');
              }else{
                classe = $("table tbody tr:first").attr('class');
              }

                tab_element = classe.split("²²");
                id = tab_element[0];
                username = tab_element[1];
                last_name = tab_element[2];
                first_name = tab_element[3];
                groupe = tab_element[4];
                telephone = tab_element[5];
                is_active = tab_element[6];
                ville = tab_element[7];
                quartier = tab_element[8];
                photo_url = tab_element[9];

                groupes = groupe.split("$^^$");

                $("#modal_supprimer_profil #tr_class").val(classe);
                $("#modal_supprimer_profil .user__username").val(username).trigger("change");
                $("#modal_supprimer_profil .user__last_name").val(last_name).trigger("change");
                $("#modal_supprimer_profil .user__first_name").val(first_name).trigger("change");
                $("#modal_supprimer_profil .telephone").val(telephone).trigger("change");
                $("#modal_supprimer_profil .user__is_active").val(is_active).trigger("change");
                $("#modal_supprimer_profil .ville").val(ville).trigger("change");
                $("#modal_supprimer_profil .photo").attr('src', photo_url);

                $("#modal_supprimer_profil #suppression_groupe_liste_profil").children().remove();

                for (var i = 0; i < groupes.length; i++) {
                  // $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span style="background-color:blue;color:white">'+groupes[i]+"</span> ").trigger("change");       
                  $("#modal_supprimer_profil #suppression_groupe_liste_profil").append('<span class="concept">'+groupes[i]+"</span> ").trigger("change");
                }

                $(".label-group").addClass("is-focused");

                $("#modal_supprimer_profil .quartier").val(quartier).trigger("change");
                $("#modal_supprimer_profil .image-profil").attr('src', photo_url);

              
          }
      });


    });





});
