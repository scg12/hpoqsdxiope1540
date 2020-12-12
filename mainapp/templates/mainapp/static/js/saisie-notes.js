    var myVar;    
    function save_notes(){
        // alert("Bonjour");
        console.log("bonjour");
    myVar = setInterval(save_notes, 5000);

    }
    function stopFunction(){
        clearInterval(myVar); // stop the timer
    }

    old_note = ""
    choice_quota = ""
    nb_vide = 0;
    val = 0;
$(document).ready(function(){
    $(".quota").prop("hidden",true);
    $("body").on("mouseup", "input[sa]", function() {
      // $(this).trigger("keyup");
      nb_vide = 0;
      var quota = $(".quota").val();
      if(quota == "ponderation"){
            total_first = 0;
            console.log("FIRST: ",$(".first").val());
            $('.first').each(function() { 
                if($(this).val()!="")
                    {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;} 
                else nb_vide++; });
            console.log("FIRST apres: ",total_first);
            if(total_first == notation_sur && nb_vide == 0)
                $(".ajouter_btn").removeAttr("disabled");
            else
                $(".ajouter_btn").prop("disabled",true);

        }
        if(quota == "pourcentage"){
            total_first = 0;
            $('.first').each(function() { 
                if($(this).val()!="")
                    {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;}                 
                else nb_vide++; });

            if(total_first == 100 && nb_vide == 0)
                $(".ajouter_btn").removeAttr("disabled");
            else
                $(".ajouter_btn").prop("disabled",true);
        }
    });
    /*$("body").on("keyup", "input[sa]", function() {
        // alert("SALUT");
        
    });*/
   

    $("body").on("click", ".excel_note", function() {
        $('#form').attr('action', '/mainapp/telecharger-fichier-notes-excel/');
        $("#form").submit();
        // $("#telecharger_fichier_notes_excel").submit();
    });
    // note_to_save sera sur la forme: 
    // id_eleve²²id_div_temps²²id_sousetab²²note0²²15.5
    note_to_save = ""
    // save_notes(); 

    $(".ajouter_btn").prop("disabled",true);
    quota_notes = $("#quota_notes").val();
    notation_sur = parseFloat($("#notation_sur").val());
    console.log("quota_notes: "+quota_notes);
    console.log("notation_sur: "+notation_sur);



    $("body").on("keyup", ".first", function() {
        var quota = $(".quota").val();
        console.log(choice_quota);
        nb_vide = 0;
        if ( choice_quota =="opt1"){
            if(quota == "ponderation"){
                total_first = 0;
                console.log("FIRST-: ",$(".first").val());
                $('.first').each(function() { 
                    if($(this).val()!="")
                        {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;} 
                    else nb_vide++;});
                    
                console.log("FIRST apres-: ",total_first);
                if(total_first == notation_sur && nb_vide == 0)
                    $(".ajouter_btn").removeAttr("disabled");
                else
                    $(".ajouter_btn").prop("disabled",true);

            }
            if(quota == "pourcentage"){
                total_first = 0;
                $('.first').each(function() { 
                    if($(this).val()!="")
                        {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;} 
                    else nb_vide++;});
                    
                if(total_first == 100 && nb_vide == 0)
                    $(".ajouter_btn").removeAttr("disabled");
                else
                    $(".ajouter_btn").prop("disabled",true);
            }
            if(quota == "decimal"){
                total_first = 0;
                $('.first').each(function() { 
                    if($(this).val()!="")
                        {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;} 
                    else nb_vide++;});

                if(total_first == 1 && nb_vide == 0)
                    $(".ajouter_btn").removeAttr("disabled");
                else
                    $(".ajouter_btn").prop("disabled",true);
            }
            if(quota == "fraction"){
                total_first = 0;
                var first=[];
                var second=[];
                $('.first').each(function() {
                        // console.log("first: ",$(this).val());
                        if($(this).val()!="")
                            first.push(parseFloat($(this).val()));
                        else nb_vide++;
                });
                $('.second').each(function() {
                        // console.log("second: ",$(this).val());
                        if($(this).val()!="")
                            second.push(parseFloat($(this).val()));
                        else nb_vide++;
                });
                nb_first = first.length;
                nb_second = second.length;
                if(nb_first == nb_second){
                    total = 0;
                    for(i=0; i<nb_first; i++){
                        total += first[i]/second[i]
                    }
                    if (total == 1 && nb_vide == 0)
                        $(".ajouter_btn").removeAttr("disabled");
                    else 
                        $(".ajouter_btn").prop("disabled",true);
                    console.log("total: ",total);
                }else
                    $(".ajouter_btn").prop("disabled",true);
            }
        }
        // quota = ponderation normale
        else {
                total_first = 0;
                $('.first').each(function() { 
                    if($(this).val()!="")
                        {val = parseFloat($(this).val()); total_first += val; if (val == 0) nb_vide++;} 
                    else nb_vide++; });

                console.log("FIRST apres:* ",total_first);
                if(total_first == notation_sur && nb_vide == 0)
                    $(".ajouter_btn").removeAttr("disabled");
                else
                    $(".ajouter_btn").prop("disabled",true);

            }

    });


    if ($(".quota").val() != "fraction"){
            $(".second").val("");
            $(".second").prop("hidden",true);
            $(".first").val("");
            if ($(".quota").val() == "pourcentage"){
                    $(".separateur_unite").html("%");
                }
            else {$(".separateur_unite").html("");
           }
        }
        else{
            $(".second").val("");
            $(".second").removeAttr("hidden");
            // $(".separateur_unite").html("/");


        }

    $('.quota').change(function(){
        $(".ajouter_btn").prop("disabled",true);
        if ($(".quota").val() != "fraction"){
                $(".second").val("");
                $(".second").prop("hidden",true);
                $(".first").val("");
                if ($(".quota").val() == "pourcentage"){
                    $(".separateur_unite").html("%");
                }
                else {$(".separateur_unite").html("");

            }
                
            }
            else{
                $(".second").val("");
                $(".second").removeAttr("hidden");
                $(".first").val("");
                // $(".separateur_unite").html("/");

            }
    });

    $('.choix_quota').change(function(){
        choice_quota = $(this).val();
        $(".ajouter_btn").prop("disabled",true);
        if ($(this).val()=="opt2"){
            $(".quota").prop("hidden",true);
            $(".second").val("");
            $(".separateur_unite").html("");
            $(".second").prop("hidden",true);
            $(".first").val("");
        }
        else 
            {$(".quota").removeAttr("hidden");
            if ($(".quota").val() != "fraction"){
                $(".second").val("");
                $(".second").prop("hidden",true);
                $(".first").val("");
                if ($(".quota").val() == "pourcentage"){
                    $(".separateur_unite").html("%");
                }
                else $(".separateur_unite").html("");
            }
            else{
                $(".second").val("");
                $(".first").val("");
                // $(".separateur_unite").html("/");
                $(".second").removeAttr("hidden");
            }
        }
    });

    var currCell = $('td').first();

     $('.classes').change(function(){
        $('#form').attr('action', '/mainapp/saisie-notes/');

        var id_user = $("#user").val();
        var classe = $(this).val();
        var cours = $(".cours").val();
       /*   
        if (cours.includes("²²"+classe+"²²")){
            alert("Ok: "+classe +" in "+ cours)
        }
        else{
            $(".cours > option").each(function() {
                // if (cours.includes("²²"+classe+"²²"))
                alert(this.text + ' ' + this.value);
            });

        }

        alert(id_user+" - "+classe+" - "+cours)*/

        id_sousetab = 1;
        // id_sousetab = $(".sousetab").val();
        id_dt_niv_dt = $(".divisions_temps").val();
        id_classe_id_cours_id_matiere = $(".classes").val();
        // id_elev_num_note = $(this).attr("info");


        var form = $(".saisie_notes");
        var url_action = form.attr("action");

        var trier_par = "non defini";

        var donnees = "cours²²"+id_sousetab + "²²" + id_dt_niv_dt + "²²" + id_classe_id_cours_id_matiere;
        

         $.ajax({
             method: 'POST',
             url: url_action,
             data: {
               form_data : donnees,
               csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
             },
             success: gererSucces2,
             error: gererErreur,
         });

     });

     $('.cours').change(function(){
        var id_user = $("#user").val();
        var cours = $(this).val();
        var classe = $(".classes").val();
        // alert("* "+id_user+" - "+classe+" - "+cours)
     });

     $("body").on("keyup", ".input", function() {
    // $('.input').keyup(function(){
    var val = $(this).val();
    if(isNaN(val)){
         val = val.replace(/[^0-9\.\,]/g,'');
        if(val.split('.').length>2 || val.split(',').length>1) 
             val =val.replace(/\.+$/,"");
        if(val.split(',').length>2 || val.split('.').length>1) 
            val =val.replace(/\,+$/,"");
    }
    $(this).val(val); 
});

    // User clicks on a cell
    $("body").on("click", "td", function() {
    // $('td').click(function() {
        currCell = $(this);
    });

    // User navigates table using keyboard
    $("body").on("keydown", "#table_notes", function(e) {
    // $('table').keydown(function (e) {
        var c = "";
        if (e.which == 39) {
            // Right Arrow
            // e.preventDefault() permet d'eviter le comportement par défaut qui empêchait que select()
            // fonctionne. ds l'evt focus de l'input plus bas on active le select
            e.preventDefault();
            c = currCell.next();
            er = c.find('input');
            er.focus();


        } else if (e.which == 37) { 
            // Left Arrow
            e.preventDefault();
            c = currCell.prev();
            c.find('input').focus();
        } else if (e.which == 38) { 
            // Up Arrow
            e.preventDefault();
            c = currCell.closest('tr').prev().find('td:eq(' + 
              currCell.index() + ')');
            c.find('input').focus();
        } else if (e.which == 40) { 
            // Down Arrow
            e.preventDefault();
            c = currCell.closest('tr').next().find('td:eq(' + 
              currCell.index() + ')');
            c.find('input').focus();
        } 
        else if (e.which == 9 && !e.shiftKey) { 
            // Tab
            e.preventDefault();
            c = currCell.next();
            c.find('input').focus();
        } else if (e.which == 9 && e.shiftKey) { 
            // Shift + Tab
            e.preventDefault();
            c = currCell.prev();
            c.find('input').focus();
        } 

        // If we didn't hit a boundary, update the current cell
        if (c.length > 0) {
            currCell = c;
            // currCell.focus();
        }
    });

     $("body").on("focus", ".input", function() {
     // $(".input").focus(function() {
         old_note =  $(this).val();
            $(this).select(); 
        }); 
          $("body").on("change", ".divisions_temps", function() {
            $('#form').attr('action', '/mainapp/saisie-notes/');
            id_sousetab = 2
            // id_sousetab = $(".sousetab").val();
            id_dt_niv_dt = $(".divisions_temps").val();
            id_classe_id_cours_id_matiere = $(".classes").val();
            id_elev_num_note = $(this).attr("info");

            var form = $(".saisie_notes");
            var url_action = form.attr("action");

            var trier_par = "non defini";

            var donnees = "division_temps²²"+id_sousetab + "²²" + id_dt_niv_dt + "²²" + id_classe_id_cours_id_matiere;

             $.ajax({
                 method: 'POST',
                 url: url_action,
                 data: {
                   form_data : donnees,
                   csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                 },
                 success: gererSucces2,
                 error: gererErreur,
             });
        });

     $("body").on("focusout", ".input", function() {
     // $(".input").focusout(function() { 
            $('#form').attr('action', '/mainapp/saisie-notes/');

            call_ajax = 1;
            current_note =  $(this).val();
            console.log(old_note+" "+current_note);
            if (current_note == "" && old_note == "")
             call_ajax = 0;
            if (current_note != "" && old_note != "" && parseFloat(current_note) == parseFloat(old_note))
             call_ajax = 0;

                
            id_sousetab = 1;
            // id_sousetab = $(".sousetab").val();
            id_dt_niv_dt = $(".divisions_temps").val();
            id_classe_id_cours_id_matiere = $(".classes").val();
            id_elev_num_note = $(this).attr("info");
            note = $(this).val();
            // console.log("id_classe_id_cours_id_matiere: ",id_classe_id_cours_id_matiere);
            if (call_ajax == 1)
            {
                console.log($(this).val());
                console.log($(this).attr("info"));

                // idclasse²²idcours²²idmatiere
                console.log("idclasse²²idcours²²idmatiere:",$(".classes").val());

                var form = $(".saisie_notes");
                var url_action = form.attr("action");

                var trier_par = "non defini";

                var donnees = "note²²"+id_sousetab + "²²" + id_dt_niv_dt + "²²" + id_classe_id_cours_id_matiere + "²²" + id_elev_num_note+ "²²" + note;

                 $.ajax({
                     method: 'POST',
                     url: url_action,
                     data: {
                       form_data : donnees,
                       csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                     },
                     success: gererSucces2,
                     error: gererErreur,
                 });
            }
            

        }); 

         function gererErreur(data){
            console.log(data);
         }
        function gererSucces2(data){
            console.log(data);
            choix = data.choix;
            console.log(choix);
            if (choix == "cours" || choix == "division_temps"){
                $("#table_notes tbody tr").remove();
                $("#table_notes thead tr").remove();

                eleves_id = data.eleves_id
                eleves_mat = data.eleves_mat
                eleves_nom = data.eleves_nom
                eleves_prenom = data.eleves_prenom
                notes_eleves = data.notes_eleves
                nb_sous_notes = data.nb_sous_notes

                nb_items = eleves_id.length;
                console.log(nb_sous_notes, eleves_id.length);
                nouvelle_ligne = "";

                nouvelle_ligne = `<tr><th class="copy-btn th1">#</th><th class="copy-btn th1">Matricule</th>`;
                nouvelle_ligne += `<th class="copy-btn th1">Nom</th><th class="copy-btn th1">Prénom</th>`;
                
                if (nb_sous_notes <= 1)
                    nouvelle_ligne += `<th class="copy-btn th">Note</th>`;
                else{
                    for(var i=0; i < nb_sous_notes; i++){

                        nouvelle_ligne += `<th class="copy-btn th">Note ${i+1}</th>`; 
                    }
                     nouvelle_ligne += `<th class="copy-btn th1">Note Finale</th></tr>`;
                }
                $("#table_notes thead").append(nouvelle_ligne);

                j = 0;
                nouvelle_ligne = "";
                 for(var i=0; i < nb_items; i++){
                    j++;
                // console.log(i);
                nouvelle_ligne += `<tr><td class="td readonly"><input type="text" class="input1 readonly" value="${j}" readonly></td>`;
                nouvelle_ligne += `<td class="td readonly"><input type="text" class="input1 readonly" value="${eleves_mat[i]}" readonly></td>`;
                nouvelle_ligne += `<td class="td readonly"><input type="text" class="input1 readonly" value="${eleves_nom[i]}" readonly></td>`;
                nouvelle_ligne += `<td class="td readonly"><input type="text" class="input1 readonly" value="${eleves_prenom[i]}" readonly></td>`;
                el_id = eleves_id[i];
                
                if (nb_sous_notes <= 1){
                    console.log(notes_eleves[i][0]);
                    if (notes_eleves[i][0] == -111 || typeof notes_eleves[i][0] === 'undefined'){
                        nouvelle_ligne += `<td tabindex="0" class="td"><input type="text" class="input note0" value="" info="${el_id}²²0"></td>`;
                    }
                    else{
                        nouvelle_ligne += `<td tabindex="0" class="td"><input type="text" class="input note0" value="${notes_eleves[i][0]}" info="${el_id}²²0"></td>`;
                    }
                }
                else{
                    nb_sn = 0;
                    for(var k=0; k < nb_sous_notes; k++){
                        if(notes_eleves[i][k] == -111 || typeof notes_eleves[i][k] === 'undefined'){
                            nouvelle_ligne += `<td tabindex="0" class="td"><input type="text" class="input note${k}" value="" info="${el_id}²²${k}"></td>`;
                        }
                        else{
                            nouvelle_ligne += `<td tabindex="0" class="td"><input type="text" class="input note${k}" value="${notes_eleves[i][k]}" info="${el_id}²²${k}"></td>`;
                        }
                    }
                    nouvelle_ligne += `<td class="td readonly"><input type="text" class="input1 readonly note_finale" value="17" style="font-weight: 500;" readonly></td>`;
                  }
                     
            }

                $("#table_notes tbody").append(nouvelle_ligne);
        }

    }

    $("body").on("click", ".copy-btn", function() {
    // $(".copy-btn").click(function() {
        let tmpElement = $('<textarea style="opacity:0;"></textarea>');

        tds = $(this)
                  .filter('th, td')
                  .filter(':not([colspan])')
                  .closest('table')
                  .find('tr')
                  .filter(':not(:has([colspan]))')
                  .children(':nth-child(' + ($(this).index()+1) + ')');
                i = 0;
        tds.each(function(){ 
            if (i > 0){
                tmpElement.text(tmpElement.text() + $(this).find('input').val() + '\n');
            }
            i++;
        });
        tmpElement.appendTo($('body')).focus().select();
        document.execCommand("copy");
        tmpElement.remove();

});
    $('td input').bind('paste', null, function(e) {
    // $("body").bind("paste", "td input", function(e) {

      $txt = $(this);
      setTimeout(function() {
        var values = $txt.val().split(/\s+/);
        var values2 = $txt.val().split(/\n+/);
        // var values = $txt.val().split('\n');
        // alert(values+" - "+values2);
        values2 = values2.toString()
        n = values2.length;
        // alert(values2+" - "+n);
        i = 0;
        j = 0;
        /*while (i<n) {
            console.log(values2[i].charCodeAt(0));
            i++;
        }*/
        console.log(" ______ ");
        c1 = '';
        c2 = '';
        k = 0;
        ch = "";
        passe = false;
        console.log("values: "+values);
        values.forEach( function(item, index) {
            c1 = item;
            c2 = values2[i];
            k = 0;
            j = 0;
            console.log(c1);
            console.log(c2);
            passe = false;

            console.log(values2[i].charAt(0) == ""+" - "+String.fromCharCode(values2[i]));
            // while(item != c2){
            //     if(String.fromCharCode(values2[i]) !== 'undefined'){
            //         c2 += values2[i];
            //         console.log("icic");
            //     }
            //     else k++;
            //     i++;
            //     passe = true;
               
            //    console.log(item+" -- "+c2+" - "+item==c2);
            // }
            // if(passe == false) i++;

            // if( k>0 ) k -=2;
            // while (j < k) {
            //     ch +="²²-";
            //     j++;
            // }
            // ch += "²²"+c1;
            // console.log("* "+k);
            // console.log(c1 == c2);
        });
        // console.log(ch);
        // ch2 = ch.split("²²");
        // ch2.forEach( function(item, index) {
        //     console.log(String.fromCharCode(item));
        // });
        // alert($txt);
        var currentRowIndex = $txt.parent().parent().index();
        var currentColIndex = $txt.parent().index();
        // alert(currentRowIndex+" -"+currentColIndex);
        var totalRows = $('#table_notes tbody tr').length;
        var totalCols = $('#table_notes thead th').length;
        var count = 0;
        // alert(currentRowIndex);
        // alert($('#table_notes tbody tr').eq(currentRowIndex).find('td').find('input'));
          for (var j = currentRowIndex; j < totalRows; j++) {
            if (count > (totalRows - currentRowIndex)) break;
            
            // alert($('#table_notes tbody tr').eq(j).find('td').eq(currentColIndex).find('input'));
            // alert($('#table_notes tbody tr').eq(j).find('td').find('input').hasClass("readonly"));
            if($('#table_notes tbody tr').eq(j).find('td').eq(currentColIndex).find('input').hasClass("readonly")) break;
            var value = values[count];
            var inp = $('#table_notes tbody tr').eq(j).find('td').eq(currentColIndex).find('input');
            // alert(value == null);
            // alert(value);
            if (value != null)
            {
                inp.empty();
                inp.val(value);  
            count++;
            }
            // inp.trigger("focusout");


          }

      }, 0);
    });
$("body").on("dblclick", ".th", function() {
// $(".th").dblclick(function() {
        var col_index = $(this).index();
        var $col = $(this);
        $(this).addClass('col_color_click');

        var currentRowIndex = $col.parent().parent().index();
        var currentColIndex = $col.parent().index();

        var totalRows = $('#table_notes tbody tr').length;
        var totalCols = $('#table_notes thead th').length;

          for (var j = currentRowIndex; j < totalRows; j++) {
            var inp = $('#table_notes tbody tr').eq(j).find('td').eq(col_index).find('input');
            inp.addClass('input_color_click');
          }
        var left = $(this).offset().left;
        var top = $(this).offset().top;
        top += 6;

        var position = $(this).offset();
        // $("#id_tooltip1").css(position)
        // $("#id_tooltip1").css("top", top);
        $("#id_tooltip1").css({top: top, left: left, position:'absolute'});
        $('#id_tooltip1').show();

        setTimeout(function () {

            $col.removeClass('col_color_click');
            for (var j = currentRowIndex; j < totalRows; j++) {
                var inp = $('#table_notes tbody tr').eq(j).find('td').eq(col_index).find('input');
                inp.removeClass('input_color_click');
             }
            $('#id_tooltip1').hide();

        }, 400);
});

$("body").on("click", ".ajouter-sous-note-link", function() {
        
        $('#modal_ajouter_sous_note').modal('show');

        // id_sousetab = $(".sousetab").val();
        id_sousetab = 1;
        id_dt_niv_dt = $(".divisions_temps").val();
        id_classe_id_cours_id_matiere = $(".classes").val();
        id_elev_num_note = $(this).attr("info");
        nb_sous_notes = $("#nb_sous_notes").val();
        var info = id_sousetab + "²²" + id_dt_niv_dt + "²²" + id_classe_id_cours_id_matiere+ "²²" + nb_sous_notes;
        console.log(info);

        $("#id_info").val(info);

    });


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

});