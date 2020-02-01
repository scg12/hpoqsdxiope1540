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

        var jj = 1;

        //index de l'onglet actif
        var my_index = 0;

        /* gestion du boutton suivant*/
        $("#next-navigation").on("click",function () {
          
            width =  $(".wizard-navigation ul li:first").width()*jj;
            taille = $(".wizard-navigation ul li").length;

            if(jj <= taille-1){

                if (jj == taille-1){
                    $(".moving-tab").css({"transform": "translate3d("+ (width+Xcoordinate_translation) +"px, 0px, 0px)",
                    "position":"absolute", "top": "-5px",
                    "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                  
                }else{
                    $(".moving-tab").css({"transform": "translate3d("+ width+"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px",
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

            if(jj >= 2){

                if (jj == 2){
                    $(".moving-tab").css({"transform": "translate3d("+ (width-Xcoordinate_translation) +"px, 0px, 0px)",
                    "position":"absolute", "top": "-5px",
                    "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
                }else{
                    $(".moving-tab").css({"transform": "translate3d("+ width+"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px",
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

            $("#position").val(jj);alert(jj);

            width =  $(".wizard-navigation ul li:first").width()*(jj-1);

            /* chargement du contenu de l'onglet actif*/
            my_index = $(this).index();
            $(".tab-pane").removeClass("active");
            $(".tab-content").children(".tab-pane").eq(my_index).addClass("active")
            

            if (jj ==1){
            //alert("debut");

              $(".moving-tab").css({"transform": "translate3d("+ (width-Xcoordinate_translation) +"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }else if(jj == taille){
            //alert("fin");

                $(".moving-tab").css({"transform": "translate3d("+ (width+Xcoordinate_translation) +"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }else{
            //alert("milieu");

              $(".moving-tab").css({"transform": "translate3d("+ (width) +"px, 0px, 0px)",
                      "position":"absolute", "top": "-5px",
                      "transition": "all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1) 0s"});
            }       
          
        });

    });
          