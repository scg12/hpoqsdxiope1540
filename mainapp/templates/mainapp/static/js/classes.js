$(document).ready(function(){

     $(".recherche").keyup(function(e) {

          e.stopImmediatePropagation(); 

          $("#message").text("");
          var recherche = $("#recherche").val().trim();
          var nbre_element_par_page = $("#nbre_element_par_page").val();
          var numero_page = " "

          var form = $(".recherche_eleve");
          var url_action = form.attr("action");

          var trier_par = "non defini";
          
          var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

          var sousetab_id = $(".active-sousetab").attr("value");

          var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
          

          var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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

          if(data.permissions.indexOf("cours") == -1){
            $("table tbody tr").remove();

             nouvelle_ligne = '<tr><td colspan="11" class="text-center h4">Vous n\'avez plus droit d\'accès sur cette page</td></tr>';                
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
                      nom = liste_eleves[i].nom;                     
                      prenom = liste_eleves[i].prenom;
                      matricule = liste_eleves[i].matricule;
                      sexe = liste_eleves[i].sexe;
                      date_naissance = liste_eleves[i].date_naissance;
                      lieu_naissance = liste_eleves[i].lieu_naissance;
                      date_entree = liste_eleves[i].date_entree;
                      redouble = liste_eleves[i].redouble;
                      etat_sante = liste_eleves[i].etat_sante;
                      nom_pere = liste_eleves[i].nom_pere;
                      prenom_pere = liste_eleves[i].prenom_pere;
                      nom_mere = liste_eleves[i].nom_mere;
                      prenom_mere = liste_eleves[i].prenom_mere;
                      tel_pere = liste_eleves[i].tel_pere;
                      tel_mere = liste_eleves[i].tel_mere;
                      email_pere = liste_eleves[i].email_pere;
                      email_mere = liste_eleves[i].email_mere;
                      photo_url = liste_eleves[i].photo_url;

                      if (etat_sante == "0"){
                          img_etat_sante = '<div class="etat-sante-signe vert1" style=""></div>';
                      }else if(etat_sante == "1"){
                          img_etat_sante = '<div class="etat-sante-signe jaune" style=""></div>';
                      }else {
                          img_etat_sante = '<div class="etat-sante-signe rouge1" style=""></div>';
                      }
                      
                    nouvelle_ligne = "<tr class='"+ id +'²²'+ nom +'²²'+ prenom +'²²'+ matricule + '²²'+ sexe +'²²'+ date_naissance+'²²'+ lieu_naissance +'²²'+ date_entree +'²²'+ redouble +'²²'+ etat_sante +"'>" + '<th scope="row" class="fix-col0">'+ (i+1)
                    + '</th>'+ '<td class="detail-eleve-link-td fix-col1"><img class="photo" src="/../../media/photos/22_signe.jpeg" width="30px" height="30px"></td>' +'<td style="text-transform: uppercase;" class="detail-eleve-link-td fix-col2">'+ nom 
                    + '</td><td style="text-transform: uppercase;" class="detail-eleve-link-td">'+ prenom + '</td><td style="text-transform: uppercase;" class="detail-eleve-link-td">'+ matricule + '</td><td style="text-transform: uppercase;" class="detail-eleve-link-td">'
                    + sexe + '</td><td class="detail-eleve-link-td">'+ date_naissance+ '</td><td class="detail-eleve-link-td" style="text-transform: uppercase;">'+ lieu_naissance +'</td><td class="detail-eleve-link-td">' + date_entree + '</td><td class="detail-eleve-link-td" style="text-transform: uppercase;">'+ redouble
                    + '</td><td class="detail-eleve-link-td">'+ img_etat_sante + '</td>';

                    $("table tbody").append(nouvelle_ligne);
                      
                    
                  }

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

                /* mettre a jour le nouveau theme de l'utilisateur */
            $(".sidebar").attr("data-color", data_color);
            // $(".sidebar").addClass(sidebar_class);
            $(".btn").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
            $(".btn-rond").removeClass("orange vert violet turquoise bleu rose jaune").addClass(theme_class);
            $(".cursus-btn-pagination").removeClass("orange vert violet bleu rose jaune turquoise").addClass(theme_class);

          }
         
      }

      function gererErreur(error) {
        $("#message").text(error);
        console.log(error);
      
      }


     $("body").on("click", ".detail-eleve-link-td", function() {
        //class="{{ cycl.id }}²²{{ cycl.nom_eleve }}²²{{ cycl.sous_eleve }}²²{{ cycl.eleve }}"
        $('#modal_detail_eleve').modal('show');

        var eleve = $(this).parents("tr").attr('class');
        tab_element = eleve.split("²²");

         /*class="²²{{ eleve.sexe }}²²{{ eleve.date_naissance }}²²{{ lieu_naissance }}²²{{ date_entree }}²²{{ redouble }}
        eleve_id = tab_element[0];
        eleve_nom = tab_element[1];
        eleve_prenom = tab_element[2];
        eleve_sexe = tab_element[3];
        eleve_date_naissance = tab_element[4];
        eleve_lieu_naissance = tab_element[5];
        eleve_date_entree = tab_element[6];

      
        $(".eleve_id").val(nom_eleve);
        $(".eleve_nom").val(nom_niveau);
        $(".eleve_prenom").val(nom_cycle);
        $(".eleve_sexe").val(nom_sousetab);
        $(".eleve_date_naissance").val(nom_etab);
        $(".eleve_lieu_naissance").val(specialite);
        $(".eleve_date_entree").val(id);

        $(".nom_eleve").attr("disabled", "True");
        $(".nom_niveau").attr("disabled", "True");
        $(".nom_cycle").attr("disabled", "True");
        $(".nom_sousetab").attr("disabled", "True");
        $(".nom_etab").attr("disabled", "True");
        $(".specialite").attr("disabled", "True");*/

    });



        $("body").on("click", ".tri-asc", function(e) {

            e.stopImmediatePropagation();

            $(".tri").removeClass("tri-desc").addClass("tri-asc");
            $(this).removeClass("tri-asc").addClass("tri-desc");
            
            $(".tri").children("i").hide();
            $(this).children(".down").show();
            
            //$("#message").text("");
            var recherche = $("#recherche").val().trim();
            var nbre_element_par_page = $("#nbre_element_par_page").val();
            var numero_page = " ";

            var form = $(".recherche_eleve");
            var url_action = form.attr("action");
            var trier_par = $(this).parents("th").attr("class").split(" ")[0];
            

            $(this).attr("class", trier_par + " tri tri-desc");

          
            var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

            var sousetab_id = $(".active-sousetab").attr("value");

            var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
            
            var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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

            $(".tri").removeClass("tri-desc").addClass("tri-asc");
            $(this).removeClass("tri-desc").addClass("tri-asc");
            
            $(".tri").children("i").hide();
            $(this).children(".up").show(); 

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
          
            var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

            var sousetab_id = $(".active-sousetab").attr("value");

            var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
            
            var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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

        $("#nbre_element_par_page").change(function (e) {

            e.stopImmediatePropagation(); 
            $("#message").text("");
            var recherche = $("#recherche").val().trim();
            var nbre_element_par_page = $("#nbre_element_par_page").val();
            numero_page = " "

            var form = $(".recherche_eleve");
            var url_action = form.attr("action");
            
            var trier_par = "non defini";
            
            $("body table thead th span i").each(function(){
                  
                  if ($(this).css("display") !== 'none'){

                    if($(this).hasClass("up")){

                      trier_par = "-" + $(this).parents("th").attr("class").split(" ")[0];
                      
                    }else{
                      trier_par = $(this).parents("th").attr("class").split(" ")[0];
                    }
                  }
            });
            

            var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

            var sousetab_id = $(".active-sousetab").attr("value");

            var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
            
            var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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

        $("body").on("click", ".pagination-element", function(e) {

              e.stopImmediatePropagation();

              var numero_page = $(this).attr('id');
              
              var nbre_element_par_page = $("#nbre_element_par_page").val();

              var recherche = $("#recherche").val().trim();

              var form = $(".recherche_eleve");
              var url_action = form.attr("action");

              var trier_par = "non defini";

              $("body table thead th span i").each(function(){
                      
                      if ($(this).css("display") !== 'none'){

                        if($(this).hasClass("up")){

                          trier_par = "-" + $(this).parents("th").attr("class").split(" ")[0];
                          
                        }else{
                          trier_par = $(this).parents("th").attr("class").split(" ")[0];
                        }
                      }
              });
                

              var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

              var sousetab_id = $(".active-sousetab").attr("value");

              var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
              
              var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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

        $(".active-year").change(function (e) {

              alert("message?: DOMString");

              e.stopImmediatePropagation();

              var numero_page =" ";
              
              var nbre_element_par_page = $("#nbre_element_par_page").val();

              var recherche = $("#recherche").val().trim();

              var form = $(".recherche_eleve");
              var url_action = form.attr("action");

              var trier_par = "non defini";

              $("body table thead th span i").each(function(){
                      
                  if ($(this).css("display") !== 'none'){

                    if($(this).hasClass("up")){

                      trier_par = "-" + $(this).parents("th").attr("class").split(" ")[0];
                      
                    }else{
                      trier_par = $(this).parents("th").attr("class").split(" ")[0];
                    }

                  }

              });
                

              var salle_de_classe_id = $(".maSalleDeClasse").attr("value");

              var sousetab_id = $(".active-sousetab").attr("value");

              var annee_scolaire = $(".active-year").text().split("-")[0].trim()+"-" + $(".active-year").text().split("-")[1].trim();
              
              var donnees = recherche + "²²~~" + numero_page + "²²~~" + nbre_element_par_page + "²²~~" + trier_par + "²²~~" + salle_de_classe_id + "²²~~" + sousetab_id + "²²~~" + annee_scolaire ;

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
        
    $(function(){
    $('a[title]').tooltip();
    });

});
