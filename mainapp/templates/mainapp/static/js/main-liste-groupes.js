$(document).ready(function(){


/*   $(".recherche").keyup(function(event) {

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

      // initialise debut et la fin des elements du tableau(resultat de la recherche) pour une meilleure pagination
              debut = parseInt((numero_page_active-1) * nbre_element_par_page);
              if (liste_profils.length < nbre_element_par_page){
                fin = parseInt(numero_page_active * liste_profils.length);
              }else{
                fin = parseInt(numero_page_active * nbre_element_par_page);
              }
              

      // gere l'affichage des elements de la derniere page
              if (liste_page[liste_page.length-1] == numero_page_active){
                debut = (numero_page_active-1)*nbre_element_par_page; 
                fin = liste_profils.length;
              }
           
              if (liste_profils.length != 0){

                  for (var i = debut; i < fin; i++) {
                      //profil = JSON.parse(liste_profils[i]);alert("mon profil "+ profil);
                      id = liste_profils[i].id;
                      username = liste_profils[i].user.username;
                      last_name = liste_profils[i].user.last_name;
                      first_name = liste_profils[i].user.first_name;
                      groupe = liste_profils[i].user.email;
                      is_active = liste_profils[i].user.is_active;
                      telephone = liste_profils[i].telephone;
                      ville = liste_profils[i].ville;
                      quartier = liste_profils[i].quartier;
                      

                    nouvelle_ligne = "<tr class='"+ id+'²²'+ username+ '²²'+ last_name +'²²'+ first_name +'²²' + groupe+'²²'+ telephone + '²²'+ is_active+ '²²'+ ville + '²²'+ quartier  +"'>" + '<th scope="row">'+ id +
                    '</th><td><img src="/static/assets/img/faces/avatar.jpg" width="25px" height="25px"></td><td>'+ username + '</td><td style="text-transform: uppercase;">' + last_name + '</td><td style="text-transform: capitalize;">' + first_name + '</td><td>'+ groupe + '</td><td>' + telephone + '</td><td>' + is_active+ '</td>' + '<td class="td-actions text-right">'+
                    '<button type="button" rel="tooltip" class="btn btn-primary detail-profil-link-ajax" data-toggle="modal" data-target="#modal_detail_profil"><i class="material-icons">visibility</i></button>'+
                    '&nbsp;<button type="button" rel="tooltip" class="btn btn-primary modifier-profil-link-ajax"><i class="material-icons">edit</i></button>'+
                    '&nbsp;<button rel="tooltip" class="btn btn-danger supprimer-profil-link-ajax"><i class="material-icons">close</i></button>' + "</td></tr>";                
                    
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
                     
                      resultat_pagination +='<button class="btn btn-primary btn-sm pagination-element" id="'+liste_page[num_page]+'">'+ liste_page[num_page]+'</button>';
                    
                    }else{
                      
                      resultat_pagination +='<button class="btn btn-white btn-sm pagination-element" id="'+ liste_page[num_page] +'">'+ liste_page[num_page]+'</button>';
                      
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
                // aucun resultat de la recherche

                  nouvelle_ligne = '<tr><td colspan="7" class="text-center h4">Aucun utilisateur(s) ne correspond à votre recherche</td></tr>';                
                  
                  $("table tbody").append(nouvelle_ligne);

                  $(".pagination .contenu").remove();
              }



            //affiche le message en cas d'erreur
              if (data.message_resultat != ""){
                  $("#message").text(data.message_resultat).css('color',"red");
              }

      }

      function gererErreur(error) {
      $("#message").text(error);
      console.log(error);
      }




    $(".ajouter-profil-link").click(function() {

        $('#modal_ajouter_profil').modal('show');

        $("#modal_ajouter_profil .username").removeAttr("disabled");
        $("#modal_ajouter_profil .last_name").removeAttr("disabled");
        $("#modal_ajouter_profil .first_name").removeAttr("disabled");
        $("#modal_ajouter_profil .telephone").removeAttr("disabled");
        $("#modal_ajouter_profil .is_active").removeAttr("disabled");
        $("#modal_ajouter_profil .ville").removeAttr("disabled");
        $("#modal_ajouter_profil .quartier").removeAttr("disabled");

        $("#modal_ajouter_profil .username").val("");
        $("#modal_ajouter_profil .last_name").val("");
        $("#modal_ajouter_profil .first_name").val("");
        $("#modal_ajouter_profil .telephone").val("");
        $("#modal_ajouter_profil .is_active").val("");
        $("#modal_ajouter_profil .ville").val("");
        $("#modal_ajouter_profil .quartier").val("");

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

    });

    $(".detail-profil-link").click(function() {

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


        $("#modal_detail_profil .username").text(username);
        $("#modal_detail_profil .last_name").text(last_name);
        $("#modal_detail_profil .first_name").text(first_name);
        $("#modal_detail_profil .telephone").text(telephone);
        $("#modal_detail_profil .is_active").text(is_active);
        $("#modal_detail_profil .ville").text(ville);
        $("#modal_detail_profil .quartier").text(quartier);


    });





    $(".supprimer-profil-link").click(function() {

      $('#modal_supprimer_profil').modal('show');

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
      
      $("#id_supp").val(id);
      $("#modal_supprimer_profil .user__username").text(username);
      $("#modal_supprimer_profil .user__last_name").text(last_name);
      $("#modal_supprimer_profil .user__first_name").text(first_name);
      $("#modal_supprimer_profil .telephone").text(telephone);
      $("#modal_supprimer_profil .user__is_active").text(is_active);
      $("#modal_supprimer_profil .ville").text(ville);
      $("#modal_supprimer_profil .quartier").text(quartier);
    
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
      
    $("body").on("click", ".supprimer-profil-link-ajax", function() {
        
        $('#modal_supprimer_profil').modal('show');

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
        
        $("#id_supp").val(id);
        $("#modal_supprimer_profil .user__username").text(username);
        $("#modal_supprimer_profil .user__last_name").text(last_name);
        $("#modal_supprimer_profil .user__first_name").text(first_name);
        $("#modal_supprimer_profil .telephone").text(telephone);
        $("#modal_supprimer_profil .user__is_active").text(is_active);
        $("#modal_supprimer_profil .ville").text(ville);
        $("#modal_supprimer_profil .quartier").text(quartier);

    });


    $("body").on("click", ".modifier-profil-link-ajax", function() {
        
        $('#modal_modifier_profil').modal('show');

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

        $("#modal_modifier_profil .user__username").val(username);
        $("#modal_modifier_profil .user__last_name").val(last_name);
        $("#modal_modifier_profil .user__first_name").val(first_name);
        $("#modal_modifier_profil .telephone").val(telephone);
        $("#modal_modifier_profil .user__is_active").val(is_active);
        $("#modal_modifier_profil .ville").val(ville);
        $("#modal_modifier_profil .quartier").val(quartier);
        $("#id_modif").val(id);

        $("#modal_modifier_profil .user__username").removeAttr("disabled");
        $("#modal_modifier_profil .user__last_name").removeAttr("disabled");
        $("#modal_modifier_profil .user__first_name").removeAttr("disabled");
        $("#modal_modifier_profil .telephone").removeAttr("disabled");
        $("#modal_modifier_profil .user__is_active").removeAttr("disabled");
        $("#modal_modifier_profil .ville").removeAttr("disabled");
        $("#modal_modifier_profil .quartier").removeAttr("disabled");

    });


      
    $("body").on("click", ".detail-profil-link-ajax", function() {
        
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

        $("#modal_detail_profil .user__username").val(username);
        $("#modal_detail_profil .user__last_name").val(last_name);
        $("#modal_detail_profil .user__first_name").val(first_name);
        $("#modal_detail_profil .telephone").val(telephone);
        $("#modal_detail_profil .user__is_active").val(is_active);
        $("#modal_detail_profil .ville").val(ville);
        $("#modal_detail_profil .quartier").val(quartier);

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


   $(".tri-asc").click(function() {

        $(".tri-asc").find("img").attr("src", "/static/images/up2.png");
        $(".tri-desc").find("img").attr("src", "/static/images/down2.png");
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

    });


   $(".tri-desc").click(function() {

      $(".tri-asc").find("img").attr("src", "/static/images/up2.png");
      $(".tri-desc").find("img").attr("src", "/static/images/down2.png");
      $(this).find("img").attr("src", "/static/images/down.png");

        $("#message").text("");
        var recherche = $("#recherche").val().trim();
        var nbre_element_par_page = $("#nbre_element_par_page").val();
        var numero_page = " "

        var form = $(".recherche_profil");
        var url_action = form.attr("action");
        var trier_par = $(this).parents("th").attr("class");

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

*/

    $(".definir-permission-link").click(function() {

        $('#modal_definir_permission').modal('show');
        $('#modal_definir_permission form .corps').children().remove();
        var classe = $(this).parents("tr").attr('class');

        var tab_info_group = classe.split("~~²²");
        elt = tab_info_group[0];
        elt = elt.split("@~");
        groupe_id = elt[0]
        groupe_nom = elt[1];

        $("#id").val(groupe_id);

        classe = tab_info_group[1]
        tab_permissions = classe.split("~~");

        //alert(tab_permissions.length+' taille')
        if(classe.search("0") >= 0){
          ligne = '<h1 style="text-align: center; font-size: 1.8em;" title={% trans "Liste_des_groupes" %}>Groupe: <input type="text" value="'+groupe_nom+'" name="{{ group.name }}" style="text-align: center;"> </h1><h3><a href="#" value="main" ><b value="main">-</b></a> <input type="checkbox" name="main" value="main" id="main" onclick="togglecheck(this.value)"> All</h3>';

        }else{
          ligne = '<h1 style="text-align: center; font-size: 1.8em;" title={% trans "Liste_des_groupes" %}>Groupe: <input type="text" value="'+groupe_nom+'" name="{{ group.name }}" style="text-align: center;"> </h1><h3><a href="#" value="main" ><b value="main">-</b></a> <input type="checkbox" name="main" value="main" id="main" onclick="togglecheck(this.value)" checked> All</h3>';
        }
        
        $('#modal_definir_permission form .corps').append(ligne);


        for (var i = 0; i < tab_permissions.length; i++) {
          tab_element = tab_permissions[i].split("²²");

          permission_code = parseInt(tab_element[0]);
          permission_nom = tab_element[1];
          model = tab_element[2];

          if (i % 4 == 0){
            if(tab_permissions[i].split("²²")[0]==1 && tab_permissions[i+1].split("²²")[0]==1 && tab_permissions[i+2].split("²²")[0]==1 && tab_permissions[i+3].split("²²")[0]==1){
              ligne = '<div style="margin-left: 2rem; ">'+
                        '<h3>'+
                        '<a href="#" value="'+model+'" ><b value="'+model+'">-</b></a> <input type="checkbox" name="'+model+'" value="'+model+'" boss="boss" tocheck="'+ Math.floor(i/4) +'" onclick="togglecheck(this.value)" checked> '+ model+
                      '</h3></div>';
                    }else{
                      ligne = '<div style="margin-left: 2rem; ">'+
                        '<h3>'+
                        '<a href="#" value="'+model+'" ><b value="'+model+'">-</b></a> <input type="checkbox" name="'+model+'" value="'+model+'" boss="boss" tocheck="'+ Math.floor(i/4) +'" onclick="togglecheck(this.value)"> '+ model+
                      '</h3></div>';
                }
            

            $('#modal_definir_permission form .corps').append(ligne);

            if (permission_code == 1){
              ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+'" id="'+model+'" value="'+Math.floor(i/4)+'" checked > View</h4>';
            }else{
              ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+"1"+'" id="'+model+'" value="'+Math.floor(i/4)+'" > View</h4>';

            }
            $('#modal_definir_permission form .corps').append(ligne);
    
          }

          if (i % 4 == 1 ){

              if (permission_code == 1){
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+'" id="'+model+'" value="'+Math.floor(i/4)+'" checked > Change</h4>';
              }else{
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+"1"+'" id="'+model+'" value="'+Math.floor(i/4)+'" > Change</h4>';

              }
              $('#modal_definir_permission form .corps').append(ligne);

          }
          
          if (i % 4 == 2 ){

              if (permission_code == 1){
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+'" id="'+model+'" value="'+Math.floor(i/4)+'" checked > Add</h4>';
              }else{
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+"1"+'" id="'+model+'" value="'+Math.floor(i/4)+'" > Add</h4>';

              }
              $('#modal_definir_permission form .corps').append(ligne);

          }
          
          if (i % 4 == 3 ){

              if (permission_code == 1){
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+'" id="'+model+'" value="'+Math.floor(i/4)+'" checked > Delete</h4>';
              }else{
                ligne = '<h4 style="margin-left: 4rem; " id="'+model+'"><input type="checkbox" son="'+model +'" name="'+permission_nom+model+"1"+'" id="'+model+'" value="'+Math.floor(i/4)+'" > Delete</h4>';

              }
              $('#modal_definir_permission form .corps').append(ligne);

          }
          

          //alert(groupe_id + "** "+groupe_nom + "** "+ permission_code +"** "+ permission_nom + "*** "+model);
        }

        // id = tab_element[0];
        // username = tab_element[1];
        // last_name = tab_element[2];
        // first_name = tab_element[3];
        // //email = tab_element[4];
        // telephone = tab_element[5];
        // is_active = tab_element[6];
        // ville = tab_element[7];
        // quartier = tab_element[8];

        // $("#modal_modifier_profil .user__username").val(username);
        // $("#modal_modifier_profil .user__last_name").val(last_name);
        // $("#modal_modifier_profil .user__first_name").val(first_name);
        // $("#modal_modifier_profil .telephone").val(telephone);
        // $("#modal_modifier_profil .user__is_active").val(is_active);
        // $("#modal_modifier_profil .ville").val(ville);
        // $("#modal_modifier_profil .quartier").val(quartier);
        // $("#id_modif").val(id);

        
 

    });

});
