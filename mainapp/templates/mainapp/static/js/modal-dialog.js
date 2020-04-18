    $(document).ready(function() {

        /*  
        var width = "";

        $(".new-modal").click(function(){

            $("#test_new_model").modal("show");
            // width = $(".card-body").width();
            width = $(window).width();

            var nbreLevel = $(".wizard-navigation ul li").length; 

            if(width > 700){

              $(".moving-tab").css("width", (width/(nbreLevel+1)-100) );
            }else{
              $(".moving-tab").css("width", (width/(nbreLevel+1)) );

            }
                
        });*/
        
        
        //taille du debordement a l'extreme gauche et a l'extreme droite
        Xcoordinate_translation = 12;
        var debut = 0;
        var taille_justify_content_center = 0;
        
        $("#modal_ajouter_eleve").on("focus",function () {
           if(debut == 0)
                {width =  $(".wizard-navigation ul li:first").width()*jj;
                taille = $(".wizard-navigation ul li").length;
                hh =  $(".wizard-navigation").height();
                if (taille_justify_content_center == 0) {
                    taille_justify_content_center = $("#justify-content-center1").height();
                    $("#justify-content-center2").css({"height" : taille_justify_content_center +"px"});
                    $("#justify-content-center3").css({"height" : taille_justify_content_center +"px"});
                }
                // alert("justify-content-center height: "+ taille_justify_content_center);
                debut++;
                $(".moving-tab").css({"height" : hh +"px",});
            }
          
        });
        hh =  $(".wizard-navigation").height();
        $(".moving-tab").css({ "height" : hh +"px"});
        
        var jj = 1;

        //index de l'onglet actif
        var my_index = 0;

        /* gestion du boutton suivant*/
        $("#next-navigation").on("click",function () {
          
            width =  $(".wizard-navigation ul li:first").width()*jj;
            taille = $(".wizard-navigation ul li").length;
            hh =  $(".wizard-navigation").height();
            // Ajouté arbitrairement
            if (jj + 1 != taille)
                width += 10;
            
            if(jj <= taille-1){

                if (jj == taille-1){
                    $(".moving-tab").css({"transform": "translate3d("+ (width+Xcoordinate_translation) +"px, 0px, 0px)",
                    "position":"absolute", "top": "0px", "height" : hh +"px",
                    "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                  
                }else{
                    $(".moving-tab").css({"transform": "translate3d("+ width+"px, 0px, 0px)",
                      "position":"absolute", "top": "0px", "height" : hh +"px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                }

                $(".moving-tab").text($(".wizard-navigation ul li a")[jj].text);

                jj++;

                /* chargement du contenu de l'onglet actif*/
                my_index = my_index+1;
                $(".tab-pane").removeClass("active");
                $(".tab-content").children(".tab-pane").eq(my_index).addClass("active");
            }           
          
        });

        /* gestin du boutton precedent*/
        $("#previous-navigation").on("click",function () {

            width =  $(".wizard-navigation ul li:first").width()*(jj-2);
            taille = $(".wizard-navigation ul li").length;
            hh =  $(".wizard-navigation").height();
            // Ajouté arbitrairement, on veut repartir au premier onglet
            if (jj == 2)
                width += 10;
            // alert("Back "+ jj)

            if(jj >= 2){

                if (jj == 2){
                    $(".moving-tab").css({"transform": "translate3d("+ (width-Xcoordinate_translation) +"px, 0px, 0px)",
                    "position":"absolute", "top": "0px", "height" : hh +"px",
                    "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                }else{
                    $(".moving-tab").css({"transform": "translate3d("+ width+"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px", "height" : hh +"px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                }

                $(".moving-tab").text($(".wizard-navigation ul li a")[jj-2].text);

                jj--;

                /* chargement du contenu de l'onglet actif*/
                my_index = my_index-1;
                $(".tab-pane").removeClass("active");
                $(".tab-content").children(".tab-pane").eq(my_index).addClass("active");

            }
           
        });
       
       /* gestion de l'onglet actif(ajout de la classe "active") */
        $(".wizard-navigation ul li a").on("click",function () {
          
            $(".wizard-navigation ul li a").removeClass("active");
            $(this).addClass("active");
              
            $(".moving-tab").text(this.textContent);
           
        });


        /* gestion du click sur un onglet donné */
        $(".wizard-navigation ul li").click(function(){
          
            taille = $(".wizard-navigation ul li").length;
            jj = $(this).index()+1;
            hh =  $(".wizard-navigation").height();
            $("#position").val(jj);
            

            width =  $(".wizard-navigation ul li:first").width()*(jj-1);
            // Ajouté arbitrairement
            if (jj != taille)
                width += 10;
            // alert("jj "+jj);

            /* chargement du contenu de l'onglet actif*/
            my_index = $(this).index();
            $(".tab-pane").removeClass("active");
            $(".tab-content").children(".tab-pane").eq(my_index).addClass("active")
            

            if (jj ==1){
            //alert("debut");

              $(".moving-tab").css({"transform": "translate3d("+ (width-Xcoordinate_translation) +"px, 0px, 0px)",
                      "position":"absolute", "top": "0px", "left": "0px", "height" : hh +"px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }else if(jj == taille){
            //alert("fin");

                $(".moving-tab").css({"transform": "translate3d("+ (width+Xcoordinate_translation) +"px, 0px, 0px)",
                      "position":"absolute", "top": "0px", "height" : hh +"px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }else{
            //alert("milieu");

              $(".moving-tab").css({"transform": "translate3d("+ (width) +"px, 0px, 0px)",
                      "position":"absolute", "top": "0px", "height" : hh +"px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }       
          
        });

    });
          