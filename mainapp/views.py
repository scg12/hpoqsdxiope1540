#from django.shortcuts import render
from django.shortcuts import render,redirect
from mainapp.forms import *
from mainapp import services
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

import requests
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from requests.exceptions import ConnectionError

from django.http import JsonResponse, HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import *

from mainapp.serializers import *

from pymongo import MongoClient

from django.db.models import Q, F
from django.apps import apps
from django.db import transaction, connection

from .forms import InitialisationForm 
from django.contrib.staticfiles.storage import staticfiles_storage

import pandas as pd
from pandas import Timestamp
#pour la webcam
from base64 import b64decode
from django.core.files.base import ContentFile
#from django.core.files.images.ImageFile 

from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

import numbers
import cv2
import numpy as np
import time
from datetime import date
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from playsound import playsound

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import get_template
from django.db.models import Avg, Count, Min, Sum
from functools import reduce
import operator


# definition des constantes
pagination_nbre_element_par_page = 50
photo_repertoire = "/photos/"
photo_eleves_repertoire = "mainapp/media/photos/"

# definition des preferences utilisateurs par defaut (couleur, theme, ...) pour ceux qui ne sont pas connectés
data_color_default = "bleu"
sidebar_class_default = "bleu"
theme_class_default = "bleu"

#chemin vers le fichier excel
chemin_fichier_excel = "mainapp/templates/mainapp/static/upload/"
ANNEE_SCOLAIRE = "2019-2020"



class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# Retourne la date ok et la date aun format anglophone
def date_correct(date):
    # date_ok = "11/06/2020"
    date_ok = date.replace("/","-")
    date_ok_en = ""
    n1 = len(date_ok.split("-")) - 1
    # n1 == 2 date bien formé sinon mal formé. De m pr n2
    if n1 == 2:
    # Ici on met la date au format anglais pr la recherche
        date_ = date_ok.split("-")
        un = date_[0]
        deux = date_[1]
        trois = date_[2]
        # print("Deux: ",deux, deux.isdigit())
        if len(trois) == 4 and len(deux) == 2 and len(un) == 2 and trois.isdigit() and deux.isdigit() and un.isdigit():
          date_ok_en = trois+"-"+deux+"-"+un
          date_ok = un+"-"+deux+"-"+trois
        else:
            date_ok = ""
    else:
        date_ok, date_ok_en = "", ""
    return date_ok, date_ok_en

def set_divisiontemps_status(date_deb_en, date_fin_en,today):
    # On cherche à fixer la le status de la division du temps
    is_active = False
    if date_deb_en != "" and date_fin_en != "":
        is_active = True if today <= date_fin_en and today >= date_deb_en else False

    elif date_deb_en != "" and date_fin_en == "":
            is_active = True if today >= date_deb_en else False

    elif date_deb_en == "" and date_fin_en != "":
        is_active = True if today <= date_fin_en else False
    else:
        is_active = False
    # print(date_deb_en, today, date_fin_en,is_active)

    return is_active

def definition_divisionstemps(request):
    
    start = time.time()  
    id_sousetab = request.POST["sousetab"] if request.POST["sousetab"] == "all" else int(request.POST["sousetab"])
    print("id_sousetab", id_sousetab)   
    sousetab_id, nom_sousetab = "", ""
    setab = []
    evolution, cpte_evolution, nb_sousetab = 1, 0, 0

    appellation_bull = request.POST['appellation_bull']
    nb_hierarchies = int(request.POST['nb_hierarchies'])
    print("nb_hierarchies ", nb_hierarchies)
    # evolution = nb_hierarchies * nb_sousetab
    # evolution = nb_hierarchies * nb_sousetab + 2 if id_sousetab == "all" else nb_hierarchies * nb_sousetab + 1
    cpte_evolution = 1
    indice = 2
    while indice <= nb_hierarchies:
        # if indice < nb_hierarchies:
        nombre_hierarchie = int(request.POST['nombre_hierarchie'+str(indice)])
        # print("nombre_hierarchie",indice, nombre_hierarchie)
        evolution += nombre_hierarchie
        indice += 1
    # print("evolution: ", evolution)

    if id_sousetab != "all":
        setab = SousEtab.objects.values('id','nom_sousetab').filter(pk = id_sousetab)[0]
        sousetab_id, nom_sousetab = setab['id'], setab['nom_sousetab']
        nb_sousetab = 1
    else:
        nb_sousetab =  SousEtab.objects.all().count()

    evolution = evolution * nb_sousetab

    if LesDivisionTemps.objects.all().count() > 0 or DivisionTemps.objects.all().count() > 0:
        cursor = connection.cursor()
        liste_classes_id = []
        niveaux = []

        # cursor.execute(“DELETE FROM mainapp_lesdivisiontempssousetab WHERE store_id = %s”, [store.id])
        if id_sousetab != "all":
            cursor.execute("DELETE FROM mainapp_lesdivisiontemps WHERE id_sousetab = %s", [id_sousetab])
            cursor.execute("DELETE FROM mainapp_divisiontemps WHERE id_sousetab = %s", [id_sousetab])
            cursor.execute("DELETE FROM mainapp_lesdivisiontempssousetab WHERE id_sousetab = %s", [id_sousetab])
            
            Groupe.objects.filter(id_sousetab = id_sousetab).update(divisions_temps = [])
            Cours.objects.filter(id_sousetab = id_sousetab).update(divisions_temps = [])

            niveaux = Niveau.objects.filter(id_sousetab = id_sousetab)

        else:
            cursor.execute("DELETE FROM mainapp_lesdivisiontemps")
            cursor.execute("DELETE FROM mainapp_divisiontemps")
            cursor.execute("DELETE FROM mainapp_lesdivisiontempssousetab")

            # le ~Q(id_sousetab = 0) est juste un muchibichi pr dire tous car le update semble vouloir un param au niveau du filter
            Groupe.objects.filter(~Q(id_sousetab = 0)).update(divisions_temps = [])
            Cours.objects.filter(~Q(id_sousetab = 0)).update(divisions_temps = [])

            niveaux = Niveau.objects.filter()
        for n in niveaux:
            # niv = niveaux.classes.all()
            classes = n.classes.values('id').all()
            [liste_classes_id.append(c['id']) for c in classes]
        # print(liste_classes_id)
        Eleve.objects.filter(id_classe_actuelle__in = liste_classes_id).update(divisions_temps = [])
        deletion_time = time.time() 
        print("TIME OF DELETION OF OLD DATA IS: ", deletion_time-start)


    indice = 1

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    p, today = date_correct(today)
    libelle = ""


    # On save d'abord les infos annuelles
    niveau_division_temps = 1
    libelle = request.POST['hierarchie1']
    nom_hierarchie_suiv = request.POST['hierarchie2']

    # Ici on save d'abord la division de temps annuelle, qui est calculée.
    if id_sousetab == "all":
        # sousetab_id = SousEtab.objects.values('id','nom_sousetab')
        sousetab_id = SousEtab.objects.all()
        for s in sousetab_id:
            print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
            cpte_evolution += 1
            print(s.nom_sousetab)
            dt  = LesDivisionTempsSousEtab()
            dt.libelle = libelle
            dt.date_deb, dt.date_deb_en =  "", ""
            dt.date_fin, dt.date_fin_en =  "", ""
            dt.is_active = False
            dt.niveau_division_temps = niveau_division_temps
            dt.mode = "calculé"
            dt.nom_sous_hierarchie = nom_hierarchie_suiv
            dt.archived = "0"
            dt.id_sousetab = s.id
            dt.nom_sousetab = s.nom_sousetab
            dt.save()
            s.divisions_temps.add(dt)
            s.appellation_bulletin = appellation_bull
            s.save()
            groupes = Groupe.objects.filter(id_sousetab = s.id)
            for g in groupes:
                #print(g)
                dt  = LesDivisionTemps()
                dt.niveau_division_temps = niveau_division_temps
                dt.archived = "0"
                dt.id_sousetab = s.id
                dt.nom_sousetab = s.nom_sousetab
                dt.save()
                g.divisions_temps.add(dt)

            cours = Cours.objects.filter(id_sousetab = s.id)
            for c in cours:
                #print(c)
                dt  = LesDivisionTemps()
                dt.niveau_division_temps = niveau_division_temps
                dt.archived = "0"
                dt.id_sousetab = s.id
                dt.nom_sousetab = s.nom_sousetab
                dt.save()
                c.divisions_temps.add(dt)
                elvs = c.eleves.all()
                for e in elvs:
                    # dt  = LesDivisionTemps()
                    # dt.niveau_division_temps = niveau_division_temps
                    # dt.archived = "0"
                    # dt.id_sousetab = s.id
                    # dt.nom_sousetab = s.nom_sousetab
                    # dt.save()
                    divt = DivisionTemps()
                    divt.id_sousetab = s.id
                    divt.nom_sousetab = s.nom_sousetab
                    divt.niveau_division_temps = niveau_division_temps
                    divt.save()
                    # divt.type_divisions_temps.add(dt)
                    e.divisions_temps.add(divt)

    else:
        sousetab = SousEtab.objects.filter(pk = id_sousetab)[0]
        print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
        cpte_evolution += 1
        dt  = LesDivisionTempsSousEtab()
        dt.libelle = libelle
        dt.date_deb, dt.date_deb_en =  "", ""
        dt.date_fin, dt.date_fin_en =  "", ""
        dt.is_active = False
        dt.niveau_division_temps = niveau_division_temps
        dt.mode = "calculé"
        dt.nom_sous_hierarchie = nom_hierarchie_suiv
        dt.archived = "0"
        dt.id_sousetab = id_sousetab
        dt.nom_sousetab = nom_sousetab
        dt.save()
        sousetab.divisions_temps.add(dt)
        # sousetab.update(appellation_bulletin = appellation_bull)
        sousetab.appellation_bulletin = appellation_bull
        sousetab.save()
        groupes = Groupe.objects.filter(id_sousetab = id_sousetab)
        for g in groupes:
            #print(g)
            dt  = LesDivisionTemps()
            dt.archived = "0"
            dt.niveau_division_temps = niveau_division_temps
            dt.id_sousetab = id_sousetab
            dt.nom_sousetab = nom_sousetab
            dt.save()
            g.divisions_temps.add(dt)

        cours = Cours.objects.filter(id_sousetab = id_sousetab)
        for c in cours:
            #print(c)
            dt  = LesDivisionTemps()
            dt.archived = "0"
            dt.niveau_division_temps = niveau_division_temps
            dt.id_sousetab = id_sousetab
            dt.nom_sousetab = nom_sousetab
            dt.save()
            c.divisions_temps.add(dt)
            elvs = c.eleves.all()
            for e in elvs:
                # dt  = LesDivisionTemps()
                # dt.archived = "0"
                # dt.niveau_division_temps = niveau_division_temps
                # dt.nom_sousetab = nom_sousetab
                # dt.id_sousetab = id_sousetab
                # dt.save()
                divt = DivisionTemps()
                divt.nom_sousetab = nom_sousetab
                divt.id_sousetab = id_sousetab
                divt.niveau_division_temps = niveau_division_temps
                divt.save()
                # divt.type_divisions_temps.add(dt)
                e.divisions_temps.add(divt)

    niveau_division_temps = 2

    # Dans ce cas il y a une seule division du temps
    if nb_hierarchies == 2:
        nombre_hierarchie = int(request.POST['nombre_hierarchie'+str(indice+1)])
        print("nombre_hierarchie",indice+1, nombre_hierarchie)
        hierarchie = request.POST['hierarchie'+str(indice+1)]
        print("hierarchie", indice+1, hierarchie)

        
        while indice <= nombre_hierarchie:
            
            date_deb = request.POST['date_deb_'+str(indice)]
            date_fin = request.POST['date_fin_'+str(indice)]
            d_deb, d_deb_en = date_correct(date_deb)
            d_fin, d_fin_en = date_correct(date_fin)
            is_active = set_divisiontemps_status(d_deb_en, d_fin_en,today)
            libelle =  hierarchie+str(indice)

            if id_sousetab == "all":
                sousetab = SousEtab.objects.filter()
                for s in sousetab:
                    print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                    cpte_evolution += 1
                    print(s.nom_sousetab)
                    dt  = LesDivisionTempsSousEtab()
                    dt.libelle = libelle
                    dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                    dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                    dt.is_active = is_active
                    dt.mode = "saisi"
                    dt.niveau_division_temps = niveau_division_temps
                    dt.archived = "0"
                    dt.id_sousetab = s.id
                    dt.nom_sousetab = s.nom_sousetab
                    dt.save()
                    s.nom_division_temps_saisisable = libelle
                    s.save()
                    s.divisions_temps.add(dt)
                    groupes = Groupe.objects.filter(id_sousetab = s.id)
                    #print("***Config Groupes")
                    for g in groupes:
                        dt  = LesDivisionTemps()
                        # dt.libelle = hierarchie+str(indice)
                        # dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                        # dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                        # dt.is_active = is_active
                        # dt.mode = "saisi"
                        dt.niveau_division_temps = niveau_division_temps
                        dt.archived = "0"
                        dt.id_sousetab = s.id
                        dt.nom_sousetab = s.nom_sousetab
                        dt.save()
                        g.divisions_temps.add(dt)

                    cours = Cours.objects.filter(id_sousetab =  s.id)
                    #print("***Config Cours")

                    for c in cours:
                        dt  = LesDivisionTemps()
                        dt.niveau_division_temps = niveau_division_temps
                        dt.archived = "0"
                        dt.id_sousetab = s.id
                        dt.nom_sousetab = s.nom_sousetab
                        dt.save()
                        c.divisions_temps.add(dt)
                        elvs = c.eleves.all()
                        for e in elvs:
                            # print(e.divisions_temps.all())
                            # dt  = LesDivisionTemps()
                            # dt.niveau_division_temps = niveau_division_temps
                            # dt.archived = "0"
                            # dt.id_sousetab = s.id
                            # dt.nom_sousetab = s.nom_sousetab
                            # dt.save()
                            divt = DivisionTemps()
                            divt.id_sousetab = s.id
                            divt.nom_sousetab = s.nom_sousetab
                            divt.niveau_division_temps = niveau_division_temps
                            divt.save()
                            # divt.type_divisions_temps.add(dt)
                            e.divisions_temps.add(divt)
                            # divt.type_divisions_temps.add(dt)

            else:
                print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                cpte_evolution += 1
                sousetab = SousEtab.objects.filter(pk = id_sousetab)[0]
                dt  = LesDivisionTempsSousEtab()
                dt.libelle = libelle
                dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                dt.is_active = is_active
                dt.mode = "saisi"
                dt.niveau_division_temps = niveau_division_temps
                dt.archived = "0"
                dt.id_sousetab = sousetab_id
                dt.nom_sousetab = nom_sousetab
                dt.save()
                sousetab.nom_division_temps_saisisable = libelle
                sousetab.save()
                sousetab.divisions_temps.add(dt)
                groupes = Groupe.objects.filter(id_sousetab = id_sousetab)
                #print("***Config Groupes")
                for g in groupes:
                    dt  = LesDivisionTemps()
                    dt.niveau_division_temps = niveau_division_temps
                    dt.archived = "0"
                    dt.id_sousetab = id_sousetab
                    dt.nom_sousetab = nom_sousetab
                    dt.save()
                    g.divisions_temps.add(dt)


                cours = Cours.objects.filter(id_sousetab = id_sousetab)
                #print("***Config Cours")

                for c in cours:
                    dt  = LesDivisionTemps()
                    dt.niveau_division_temps = niveau_division_temps
                    dt.archived = "0"
                    dt.id_sousetab = id_sousetab
                    dt.nom_sousetab = nom_sousetab
                    dt.save()
                    c.divisions_temps.add(dt)
                    elvs = c.eleves.all()
                    for e in elvs:
                        # dt  = LesDivisionTemps()
                        # dt.niveau_division_temps = niveau_division_temps
                        # dt.archived = "0"
                        # dt.id_sousetab = id_sousetab
                        # dt.nom_sousetab = nom_sousetab
                        # dt.save()
                        divt = DivisionTemps()
                        divt.id_sousetab = id_sousetab
                        divt.nom_sousetab = nom_sousetab
                        divt.niveau_division_temps = niveau_division_temps
                        divt.save()
                        # divt.type_divisions_temps.add(dt)
                        e.divisions_temps.add(divt)
                        # e.divisions_temps.add(dt)


            # print("date_deb_",indice, dt.date_deb)
            # print("date_fin_",indice, dt.date_fin)
            indice += 1
    # Dans ce cas il y a +sieurs divisions du temps
    else:
        # hierarchie = request.POST['hierarchie'+str(indice)]
        # print("hierarchie", indice, hierarchie)
        

        nombre_hierarchie = 0
        mode_saisie = 0
        cpt = 0
        k = 0
        
        # i = 1
        # m = 0
        ind = 1
        nbrehierarchie_i_total= 0
        d_deb, d_deb_en, d_fin, d_fin_en = "","","",""
        is_active = False

        
        indice = 2


        while indice <= nb_hierarchies:
            hierarchie = request.POST['hierarchie'+str(indice)]
            # dt  = LesDivisionTemps()
            # dt.libelle = hierarchie+str(indice)
            # dt.niveau_division_temps = niveau_division_temps
            # print(dt.libelle, dt.niveau_division_temps)
            # print(dt.libelle)
            nom_hierarchie_suiv = ""
            libelle =  hierarchie+str(indice)
            # print("££ LIBELLE: ", libelle,hierarchie+str(ind))
            j = 1
            # On save d'abord les infos annuelles
        

            if indice < nb_hierarchies:
                nom_hierarchie_suiv = request.POST['hierarchie'+str(indice+1)]
                nombre_hierarchie = int(request.POST['nombre_hierarchie'+str(indice)])
                # print("nbrehierarchie_",indice, nbrehierarchie)
                
                m = 0
                i = 1
                while i <= nombre_hierarchie:
                    nbrehierarchie_i = int(request.POST['nbrehierarchie_'+str(ind)])
                    date_deb = request.POST['date_deb_'+str(ind)]
                    date_fin = request.POST['date_fin_'+str(ind)]
                    d_deb, d_deb_en = date_correct(date_deb)
                    d_fin, d_fin_en = date_correct(date_fin)
                    is_active = set_divisiontemps_status(d_deb_en, d_fin_en,today)
                    # added
                    libelle = hierarchie+str(i)
                    # m += 1
                    # print("** LIBELLE: ", libelle, niveau_division_temps, date_deb, date_fin)
                    if indice == 2:
                        # print("----save ", libelle, niveau_division_temps, date_deb, date_fin)
                        if id_sousetab == "all":
                            # sousetab_id = SousEtab.objects.values('id','nom_sousetab')
                            sousetab_id = SousEtab.objects.all()
                            for s in sousetab_id:
                                print(s.nom_sousetab)
                                print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                                cpte_evolution += 1
                                dt  = LesDivisionTempsSousEtab()
                                dt.libelle = libelle
                                dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                                dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                                dt.is_active = is_active
                                dt.niveau_division_temps = niveau_division_temps
                                dt.mode = "saisi" if dt.niveau_division_temps == nb_hierarchies else "calculé"
                                dt.nom_sous_hierarchie = nom_hierarchie_suiv
                                dt.archived = "0"
                                dt.id_sousetab = s.id
                                dt.nom_sousetab = s.nom_sousetab
                                dt.save()
                                s.divisions_temps.add(dt)
                                
                                groupes = Groupe.objects.filter(id_sousetab = s.id)
                                for g in groupes:
                                    #print(g)
                                    dt  = LesDivisionTemps()
                                    dt.niveau_division_temps = niveau_division_temps
                                    dt.archived = "0"
                                    dt.id_sousetab = s.id
                                    dt.nom_sousetab = s.nom_sousetab
                                    dt.save()
                                    g.divisions_temps.add(dt)

                                cours = Cours.objects.filter(id_sousetab = s.id)
                                for c in cours:
                                    #print(c)
                                    dt  = LesDivisionTemps()
                                    dt.niveau_division_temps = niveau_division_temps
                                    dt.archived = "0"
                                    dt.id_sousetab = s.id
                                    dt.nom_sousetab = s.nom_sousetab
                                    dt.save()
                                    c.divisions_temps.add(dt)
                                    elvs = c.eleves.all()
                                    for e in elvs:
                                        # dt  = LesDivisionTemps()
                                        # dt.niveau_division_temps = niveau_division_temps
                                        # dt.archived = "0"
                                        # dt.id_sousetab = s.id
                                        # dt.nom_sousetab = s.nom_sousetab
                                        # dt.save()
                                        divt = DivisionTemps()
                                        divt.id_sousetab = s.id
                                        divt.nom_sousetab = s.nom_sousetab
                                        divt.niveau_division_temps = niveau_division_temps
                                        divt.save()
                                        # divt.type_divisions_temps.add(dt)
                                        e.divisions_temps.add(divt)

                        else:
                            sousetab = SousEtab.objects.filter(pk = id_sousetab)[0]
                            print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                            cpte_evolution += 1
                            dt  = LesDivisionTempsSousEtab()
                            dt.libelle = libelle
                            dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                            dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                            dt.is_active = is_active
                            dt.niveau_division_temps = niveau_division_temps
                            dt.mode = "saisi" if dt.niveau_division_temps == nb_hierarchies else "calculé"
                            dt.nom_sous_hierarchie = nom_hierarchie_suiv
                            dt.archived = "0"
                            dt.id_sousetab = id_sousetab
                            dt.nom_sousetab = nom_sousetab
                            dt.save()
                            sousetab.divisions_temps.add(dt)
                            groupes = Groupe.objects.filter(id_sousetab = id_sousetab)
                            for g in groupes:
                                #print(g)
                                dt  = LesDivisionTemps()
                                dt.archived = "0"
                                dt.niveau_division_temps = niveau_division_temps
                                dt.id_sousetab = id_sousetab
                                dt.nom_sousetab = nom_sousetab
                                dt.save()
                                g.divisions_temps.add(dt)

                            cours = Cours.objects.filter(id_sousetab = id_sousetab)
                            for c in cours:
                                #print(c)
                                dt  = LesDivisionTemps()
                                dt.archived = "0"
                                dt.niveau_division_temps = niveau_division_temps
                                dt.id_sousetab = id_sousetab
                                dt.nom_sousetab = nom_sousetab
                                dt.save()
                                c.divisions_temps.add(dt)
                                elvs = c.eleves.all()
                                for e in elvs:
                                    # dt  = LesDivisionTemps()
                                    # dt.archived = "0"
                                    # dt.niveau_division_temps = niveau_division_temps
                                    # dt.nom_sousetab = nom_sousetab
                                    # dt.id_sousetab = id_sousetab
                                    # dt.save()
                                    divt = DivisionTemps()
                                    divt.nom_sousetab = nom_sousetab
                                    divt.id_sousetab = id_sousetab
                                    divt.niveau_division_temps = niveau_division_temps
                                    divt.save()
                                    # divt.type_divisions_temps.add(dt)
                                    e.divisions_temps.add(divt)

                    # else:
                    #     print("----NoT ", libelle, niveau_division_temps, date_deb, date_fin)


                    j = 1
                    print("nbrehierarchie_i: ", nbrehierarchie_i)
                    while j <= nbrehierarchie_i:
                        if j == 1:
                            nbrehierarchie_i_total += nbrehierarchie_i
                        
                        # print("**++:{}_{}_{}_{}_{}_{}".format(hierarchie, i, nom_hierarchie_suiv, j+m, date_deb, date_fin))
                        # print("**++:{}_{}_{}_{}_{}".format(hierarchie, i, nom_hierarchie_suiv, j+m, nbrehierarchie_i))
                        libelle = nom_hierarchie_suiv+str(j+m)
                        if j == nbrehierarchie_i:
                            m += nbrehierarchie_i

                        date_deb = request.POST['date_deb_'+str(j+nbrehierarchie_i_total)]
                        date_fin = request.POST['date_fin_'+str(j+nbrehierarchie_i_total)]
                        d_deb, d_deb_en = date_correct(date_deb)
                        d_fin, d_fin_en = date_correct(date_fin)
                        is_active = set_divisiontemps_status(d_deb_en, d_fin_en,today)
                        # print("** LIBELLE: ", libelle, niveau_division_temps+1, j+nbrehierarchie_i_total, date_deb, date_fin)

                        if id_sousetab == "all":
                            sousetab_id = SousEtab.objects.all()
                            for s in sousetab_id:
                                print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                                cpte_evolution += 1
                                dt  = LesDivisionTempsSousEtab()
                                dt.libelle = libelle
                                dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                                dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                                dt.is_active = is_active
                                dt.niveau_division_temps = niveau_division_temps + 1
                                dt.mode = "saisi" if dt.niveau_division_temps == nb_hierarchies else "calculé"
                                if dt.mode == "saisi":
                                    s.nom_division_temps_saisisable = nom_hierarchie_suiv
                                    s.save()
                                dt.archived = "0"
                                dt.id_sousetab = s.id
                                dt.nom_sousetab = s.nom_sousetab
                                dt.save()
                                s.divisions_temps.add(dt)
                                groupes = Groupe.objects.filter(id_sousetab = s.id)
                                for g in groupes:
                                    #print(g)
                                    dt2  = LesDivisionTemps()
                                    dt2.niveau_division_temps = niveau_division_temps + 1
                                    dt2.archived = "0"
                                    dt2.id_sousetab = s.id
                                    dt2.nom_sousetab = s.nom_sousetab
                                    dt2.save()
                                    g.divisions_temps.add(dt2)

                                cours = Cours.objects.filter(id_sousetab = s.id)
                                for c in cours:
                                    #print(c)
                                    dt2  = LesDivisionTemps()
                                    dt2.niveau_division_temps = niveau_division_temps + 1
                                    dt2.archived = "0"
                                    dt2.id_sousetab = s.id
                                    dt2.nom_sousetab = s.nom_sousetab
                                    dt2.save()
                                    c.divisions_temps.add(dt2)
                                    elvs = c.eleves.all()
                                    for e in elvs:
                                        # dt2  = LesDivisionTemps()
                                        # dt2.niveau_division_temps = niveau_division_temps + 1
                                        # dt2.archived = "0"
                                        # dt2.id_sousetab = s.id
                                        # dt2.nom_sousetab = s.nom_sousetab
                                        # dt2.save()
                                        divt = DivisionTemps()
                                        divt.id_sousetab = s.id
                                        divt.nom_sousetab = s.nom_sousetab
                                        divt.niveau_division_temps = niveau_division_temps + 1
                                        divt.save()
                                        # divt.type_divisions_temps.add(dt2)
                                        e.divisions_temps.add(divt)

                        else:
                           
                            print("____ETAPE -{}/{}-____".format(cpte_evolution, evolution))
                            cpte_evolution += 1
                            sousetab = SousEtab.objects.filter(pk = id_sousetab)[0]
                            dt  = LesDivisionTempsSousEtab()
                            dt.libelle = libelle
                            dt.date_deb, dt.date_deb_en =  d_deb, d_deb_en
                            dt.date_fin, dt.date_fin_en =  d_fin, d_fin_en
                            dt.is_active = is_active
                            dt.niveau_division_temps = niveau_division_temps + 1
                            dt.mode = "saisi" if dt.niveau_division_temps == nb_hierarchies else "calculé"
                            if dt.mode == "saisi" :
                                sousetab.nom_division_temps_saisisable = nom_hierarchie_suiv
                                sousetab.save()
                            dt.archived = "0"
                            dt.id_sousetab = sousetab_id
                            dt.nom_sousetab = nom_sousetab
                            dt.save()
                            sousetab.divisions_temps.add(dt)
                            groupes = Groupe.objects.filter(id_sousetab = id_sousetab)
                            for g in groupes:
                                #print(g)
                                dt2  = LesDivisionTemps()
                                dt2.archived = "0"
                                dt2.niveau_division_temps = niveau_division_temps + 1
                                dt2.id_sousetab = id_sousetab
                                dt2.nom_sousetab = nom_sousetab
                                dt2.save()
                                g.divisions_temps.add(dt2)

                            cours = Cours.objects.filter(id_sousetab = id_sousetab)
                            for c in cours:
                                #print(c)
                                dt2  = LesDivisionTemps()
                                dt2.archived = "0"
                                dt2.niveau_division_temps = niveau_division_temps + 1
                                dt2.id_sousetab = id_sousetab
                                dt2.nom_sousetab = nom_sousetab
                                dt2.save()
                                c.divisions_temps.add(dt2)
                                elvs = c.eleves.all()
                                for e in elvs:
                                    # dt2  = LesDivisionTemps()
                                    # dt2.archived = "0"
                                    # dt2.niveau_division_temps = niveau_division_temps + 1
                                    # dt2.id_sousetab = id_sousetab
                                    # dt2.nom_sousetab = nom_sousetab
                                    # dt2.save()
                                    divt = DivisionTemps()
                                    divt.id_sousetab = id_sousetab
                                    divt.nom_sousetab = nom_sousetab
                                    divt.niveau_division_temps = niveau_division_temps + 1
                                    divt.save()
                                    # divt.type_divisions_temps.add(dt2)
                                    e.divisions_temps.add(divt)

                        j += 1
                    i += 1
                    ind += 1
                    k += nombre_hierarchie
            # break
            niveau_division_temps += 1
            indice += 1
    end = time.time()
    print("EXECUTION TIME DIVISIONS TEMPS: {}, Soit: {} '".format(end - start, (end - start)/60))
    return redirect('mainapp:liste_divisionstemps')

def etats_paiements_eleves_fonction(request, imprimer=False, donnees=[]):
    
    sousetabs = []
    cycles = []
    niveaux = []
    classes = []
    specialites = []
    order_by = []
    info_classes = []
    info_eleves = []
    choix =""
    etat = ""
    kwargs_date = {}
    kwargs_classes = {}
    # choix_retour permet de connaitre quel data renvoyer au js
    choix_retour = 0
    montant_previsionnel = 0
    bourse_total = 0
    montant_total_eleves = 0
    excedent_total_eleves = 0
    taux_recouvrement = 0
    type_paiements_associes = []
    niveau = ""
    terminer = False
    sousetab_id = 0
    id_elem = 0
    data = []
    id_etab = 0
    id_sousetab = 0
    id_cycle = 0
    id_niveau = 0
    

    if imprimer == False:
        donnees = request.POST['form_data']

    donnees = donnees.split("²²~~")
        
    print("Les donnees: ", donnees)
    position = donnees[0]

    param2 = donnees[1] if donnees[1] == "all" else int(donnees[1])
    param3 = donnees[2]
    # param4 represente l'id du parent et peut etre all ou un id
    param4 = donnees[3]
    print("PYTHON: ",position,param2, param3,param4)
    # position == "0" on veut juste voir les paiements
    if position == "0":
        date_deb = donnees[2]
        date_fin = donnees[3]
        choix = "voir_paiements_associes"
        choix_retour = 3

        etat, genre, date_deb, date_fin, order_by, sens_tri = "", "", "", "", "", ""
        parent, id_parent, element, id_element, classes = "", "", "", "", ""
        # kwargs va contenir de manière dynamique les params du filter
        kwargs = {}
        kwargs['archived'] = "0"
        indicateur_liste_classes = ""
        classe_display = ""
        liste_classes = []
        classes_selectionnees = []
        les_classes = []
        les_classes_afficher = ""
        id_des_classes = []
        # etape1: Récupération des paramètres
        niveau_recherche = int(donnees[1])
        print("Les données ici: ", donnees)
        print("niveau_recherche: ", niveau_recherche)
        
        if niveau_recherche == 1: #id_sousetab == all
            # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + etab + "²²~~" + id_etab;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            # on cherche les TypePaiementEleve dont le indicateur_liste_classes est sous la forme
            # "etab_nom_etab_id_etab
            etat = donnees[2]
            genre = donnees[5]
            parent = donnees[3]
            id_parent = donnees[4]
            date_deb = donnees[6]
            date_fin = donnees[7]
            order_by = donnees[8]
            sens_tri = donnees[9]

            indicateur_liste_classes = "etab_"+parent+"_"+id_parent
            classe_display = parent
            kwargs['id_etab'] = int(id_parent)

            # if genre != "tous":
            #     kwargs['sexe'] = genre

            
            # kwargs['date_deb_en'] = date_deb
            # kwargs['date_fin_en'] = date_fin
            # print("1date_deb: ",date_deb, "date_fin: ",date_fin)

        elif niveau_recherche == 2: #id_cycle == all
        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + sousetab  + "²²~~" + id_sousetab;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            # on cherche les TypePaiementEleve dont le indicateur_liste_classes est sous la forme
            # sousetab_nom_sousetab_id_sousetab
            etat = donnees[2]
            genre = donnees[5]
            parent = donnees[3]
            id_parent = donnees[4]
            date_deb = donnees[6]
            date_fin = donnees[7]
            order_by = donnees[8]
            sens_tri = donnees[9]

            indicateur_liste_classes = "sousetab_"+parent+"_"+id_parent
            classe_display = parent

            kwargs['id_sousetab'] = int(id_parent)

            # if genre != "tous":
            #     kwargs['sexe'] = genre
        elif niveau_recherche == 3: #id_niveau == all
        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + cycle  + "²²~~" + id_cycle;
        # + "²²~~" + sousetab  + "²²~~" + id_sousetab;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;

            etat = donnees[2]
            element = donnees[3]
            id_element = donnees[4]
            parent = donnees[5]
            id_parent = donnees[6]
            genre = donnees[7]
            date_deb = donnees[8]
            date_fin = donnees[9]
            order_by = donnees[10]
            sens_tri = donnees[11]

            kwargs['id_cycle'] = int(id_element)

            # if genre != "tous":
            #     kwargs['sexe'] = genre
            indicateur_liste_classes = "cycle_"+parent+"_"+id_parent
            classe_display = parent


        elif niveau_recherche == 4: #sinon
        
            # etats + "²²~~" + niveau  + "²²~~" + id_niveau + "²²~~" + specialite  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal+ "²²~~" +nbre_classes+ "²²~~" + nbre_classes_selected;
            # donnees += "²²~~" + sousetab + "²²~~" + id_sousetab + "²²~~" + cycle + "²²~~" + id_cycle
            etat = donnees[2]
            parent = donnees[3]
            id_parent = donnees[4] #id_niveau
            element = donnees[5]
            id_element = donnees[6] #id_specialite
            classes = donnees[7]
        # equal permet de savoir si le nbre de classes affichées est égal au nbre de classe selected
            equal = donnees[8]
            nbre_classes = int(donnees[9])
            nbre_classe_selected = int(donnees[10])
            id_sousetab = int(donnees[12])
            id_cycle = int(donnees[14])
            genre = donnees[15]
            date_deb = donnees[16]
            date_fin = donnees[17]
            order_by = donnees[18]
            sens_tri = donnees[19]
            # sousetab_id = int(donnees[16])

            # if genre != "tous":
            #     kwargs['sexe'] = genre
            if element == "tous":
                if nbre_classe_selected == 0:
                    indicateur_liste_classes = "niveau_"+parent+"_"+id_parent
                    classe_display = parent
                    kwargs['id_niveau'] = int(id_parent)
                    
                else:
                    if equal == "yes":
                        indicateur_liste_classes = "niveau_"+parent+"_"+id_parent
                        classe_display = parent
                        kwargs['id_niveau'] = int(id_parent)


                    else:
                        # kwargs['id_niveau'] = int(id_parent)
                        indicateur_liste_classes = "classe"
                        # kwargs['{0}__{1}'.format('indicateur_liste_classes', 'iexact')] = indicateur_liste_classes

            else:
                print("ICI")
                if nbre_classe_selected == 0:
                    indicateur_liste_classes = "specialite_"+element+"_"+id_element
                    classe_display = parent + " " + element

                    kwargs['id_niveau'] = int(id_parent)
                    kwargs['{0}__{1}'.format('indicateur_liste_classes', 'iexact')] = indicateur_liste_classes
                    


                else:
                    if equal == "yes":
                        indicateur_liste_classes = "specialite_"+element+"_"+id_element
                        classe_display = parent + " " + element
                        kwargs['id_niveau'] = int(id_parent)
                        kwargs['{0}__{1}'.format('indicateur_liste_classes', 'iexact')] = indicateur_liste_classes
                        
                    else:
                        # kwargs['id_niveau'] = int(id_parent)
                        indicateur_liste_classes = "classe"
        id_parent =int(id_parent)
        kwargs['entree_sortie_caisee'] = "e"
        if date_deb != "" and date_fin != "":
            kwargs['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb
            kwargs['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin
            kwargs_date['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb
            kwargs_date['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin

        elif date_deb != "" and date_fin == "":
            kwargs['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb
            kwargs_date['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb

        elif date_deb == "" and date_fin != "":
            kwargs['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin
            kwargs_date['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin

        if indicateur_liste_classes == "classe":
            clss = classes.split(",")
            les_classes_listes = ""
            result =[]
            liste_classes =[]

            for cl in clss:
                c, id_c = cl.split("_")
                les_classes.append(c)
                les_classes_afficher +=c+", "
                les_classes_listes += id_c+"_"+c+"_"
                id_des_classes.append(id_c)
                classes_selectionnees.append(id_c+"_"+c+"_")
                kwargs['{0}__{1}'.format('liste_classes', 'icontains')] = les_classes_listes
                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','libelle',
                    'date_deb','date_fin','montant','indicateur_liste_classes','liste_classes_afficher').filter(**kwargs)
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            ind_liste_cl = l['niveau']+" "+"sans spécialité"
                        else:
                            ind_liste_cl = l['liste_classes_afficher']
                    else:
                        ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
        else:

            print("indicateur_liste_classes", indicateur_liste_classes)
            
            if niveau_recherche == 1:
                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','libelle',
                    'date_deb','date_fin','montant','indicateur_liste_classes','liste_classes_afficher').filter(**kwargs)
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            ind_liste_cl = l['niveau']+" "+"sans spécialité"
                        else:
                            ind_liste_cl = l['liste_classes_afficher']
                    else:
                        ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                        
            if niveau_recherche == 2:
                liste_classes = TypePayementEleve.objects.values('id_etab','id_sousetab',
                    'id_cycle','id_niveau','niveau','ordre_paiement','liste_classes_afficher',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes',
                    'liste_classes_afficher').filter(**kwargs)
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            ind_liste_cl = l['niveau']+" "+"sans spécialité"
                        else:
                            ind_liste_cl = l['liste_classes_afficher']
                    else:
                        ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                # if liste_classes.count()>0:
                #     id_etab = liste_classes[0]['id_etab']

                liste_classes = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher', 'libelle','date_deb','date_fin',
                    'montant','indicateur_liste_classes','liste_classes_afficher').filter(
                    ~Q(id_etab = 0) & Q(archived="0") & Q(id_sousetab = 0) & Q(id_cycle = 0) & Q(id_niveau = 0))
                for l in liste_classes:
                    ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                    print("liste_classes: ", liste_classes)
                    type_paiements_associes = sorted(type_paiements_associes, key=lambda k: k['ordre_paiement'])
            elif niveau_recherche == 3:
                print("kwargs 3: ", kwargs)
                liste_classes = TypePayementEleve.objects.values('id_etab','id_sousetab',
                    'id_cycle','id_niveau','niveau','ordre_paiement','liste_classes_afficher',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes',
                    'liste_classes_afficher').filter(**kwargs).order_by('-id_sousetab')
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            ind_liste_cl = l['niveau']+" "+"sans spécialité"
                        else:
                            ind_liste_cl = l['liste_classes_afficher']
                    else:
                        ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                
                id_sousetab = int(id_parent)
                print("kwargs_date: ", kwargs_date)
                
                liste_classes = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher', 'libelle','date_deb','date_fin',
                    'montant','indicateur_liste_classes','liste_classes_afficher').filter( 
                    ((~Q(id_etab = 0) & Q(id_sousetab = 0) & Q(archived="0")  & Q(id_cycle = 0) & Q(id_niveau = 0))|
                     (~Q(id_etab = 0) & Q(id_sousetab = id_sousetab) & Q(archived="0") & Q(id_cycle = 0) & Q(id_niveau = 0)))
                    ,**kwargs_date)#.order_by('-id_sousetab')
                for l in liste_classes:
                    ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                print("liste_classes: ", liste_classes)
                type_paiements_associes = sorted(type_paiements_associes, key=lambda k: k['ordre_paiement'])
            elif niveau_recherche == 4:
                print("kwargs4: ", kwargs)
                liste_classes = TypePayementEleve.objects.values('id_etab','id_sousetab',
                    'id_cycle','id_niveau','niveau','ordre_paiement','liste_classes_afficher',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes',
                    'liste_classes_afficher').filter(**kwargs)#.order_by('-id_sousetab')
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            ind_liste_cl = l['niveau']+" "+"sans spécialité"
                        else:
                            ind_liste_cl = l['liste_classes_afficher']
                    else:
                        ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                
                     # (~Q(id_etab = 0) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(id_niveau = id_parent) & Q(archived="0"))
                print("id_cycle: ", id_cycle, "id_setb: ", id_sousetab)
                liste_classes = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher', 'libelle','date_deb','date_fin',
                    'montant','indicateur_liste_classes','liste_classes_afficher').filter(
                    ((~Q(id_etab = 0) & Q(id_sousetab = 0) & Q(archived="0")  & Q(id_cycle = 0) & Q(id_niveau = 0))|
                     (~Q(id_etab = 0) & Q(id_sousetab = id_sousetab) & Q(archived="0") & Q(id_cycle = 0) & Q(id_niveau = 0))|
                     (~Q(id_etab = 0) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(archived="0") & Q(id_niveau = 0))
                     # |(~Q(id_etab = 0) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(id_niveau = id_parent) & Q(archived="0"))
                     )
                    ,**kwargs_date
                    )#.order_by('-id_niveau','-id_cycle','-id_sousetab')
                for l in liste_classes:
                    ind_liste_cl = l['liste_classes_afficher']
                    type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':ind_liste_cl})
                print("liste_classes: ", liste_classes)
                liste_classes = TypePayementEleve.objects.values('liste_classes').filter(indicateur_liste_classes = indicateur_liste_classes)
                if liste_classes.count() > 0:
                    classes_selectionnees = []
                    liste_classes = liste_classes[0]['liste_classes']
                    print(liste_classes)
                    if element != "tous":
                        if liste_classes.count("_") == 2:
                            ligne = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher', 'libelle','date_deb','date_fin',
                        'montant','indicateur_liste_classes','liste_classes_afficher').filter(archived="0",liste_classes__icontains = liste_classes,
                        indicateur_liste_classes="classe",**kwargs_date )
                            for l in ligne:
                                type_paiements_associes.append({'libelle':l['libelle'], 
                            'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                            'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':l['liste_classes_afficher']}) 
                        elif liste_classes.count("_") > 2:
                            current = liste_classes.split("_")
                            id_des_classes = current[0:][::2]
                            les_classes = current[1:][::2]

                            id_des_classes.pop(len(id_des_classes) - 1)
                            i = 0
                            for j in les_classes:
                                classes_selectionnees.append(id_des_classes[i]+"_"+j+"_")
                                cl = id_des_classes[i]+"_"+j+"_"
                                ligne = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher', 'libelle','date_deb','date_fin',
                        'montant','indicateur_liste_classes','liste_classes_afficher').filter(archived="0",liste_classes__icontains = cl,
                        indicateur_liste_classes="classe",**kwargs_date )
                                for l in ligne:
                                    type_paiements_associes.append({'libelle':l['libelle'], 
                                'ordre_paiement':l['ordre_paiement'],'date_deb':l['date_deb'],
                                'date_fin':l['date_fin'],'montant':l['montant'],'classe_display':l['liste_classes_afficher']})
                                i += 1
                            print("ici", classes_selectionnees)
                type_paiements_associes = sorted(type_paiements_associes, key=lambda k: k['ordre_paiement'])

        [print("-* \n", l) for l in liste_classes]
        

    # L'etab a changé on cherche les sousetabs associés
    if position == "1":
        param2 = 1
        choix = "etab"
        sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(id_etab = param2)
        
    # Le sousetab a changé on cherche les niveaux et spécialités associés
    if position == "2":
        choix = "sousetab"
        
        cycles = Cycle.objects.values('id', 'nom_cycle').filter(id_sousetab = param2)
        # print("cycles count: ", cycles.count())
        print("cycles", cycles)

    
    # Le cycle a changé
    if position == "3":
        print("PARAM2: ",param2)
        choix = "cycle"
        # if param3 == "tous":
        #     print("cycle tous: ", param4)
        #     niveaux = Niveau.objects.values('id', 'nom_niveau').filter(archived = "0", id_cycle = int(param4))
        # else:
        niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_cycle = param2)

    # Le niveau a changé
    if position == "4":
        print("PARAM2: ",param2)
        choix = "niveau"
        # if param3 == "tous":
        #     print("tous niveau")
        #     specialites = Specialite.objects.values('id', 'specialite').filter(archived = "0", id_niveau = int(param4))
        # else:
        specialites = Specialite.objects.values('id', 'specialite').filter(archived = "0", id_niveau = param2)
        classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2)

    # La spécialité a changé
    if position == "5":
        choix = "specialite"
        print("PARAM2: ",param2, "PARAM3:",param3)
        if param3 == "aucune":
            print("DANS AUCUNE")
            classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = "")
        elif param3 == "tous":
            classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2)
        else:
            classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = param3)
        print("# classes: ", classes.count())
    # On veut charger le order_by
    if position == "6":
        print("** ", donnees)
        
        print(order_by)
        etat = donnees[2]
        if etat == "eleves_inscrits" or etat == "eleves_tous":
            order_by.append("Nom")
            order_by.append("Classe")
            order_by.append("Matricule")
            order_by.append("Total")
            # order_by.append("Payé")
            # order_by.append("Bourse")
            order_by.append("Excédent")
            order_by.append("Prénom")
            order_by.append("Versé")

            if etat == "eleves_tous":
                order_by.append("Reste")


        elif etat == "eleves_non_inscrits":
            order_by.append("Nom")
            order_by.append("Classe")
            order_by.append("Matricule")
            order_by.append("Total")
            # order_by.append("Payé")
            # order_by.append("Bourse")
            order_by.append("Excédent")
            order_by.append("Prénom")
            order_by.append("Total")
            order_by.append("Versé")

        choix = "order_by"
    # On veut afficher les états maintenant
    if position == "7":
        choix_retour = 1
        etat, genre, date_deb, date_fin, order_by, sens_tri = "", "", "", "", "", ""
        parent, id_parent, element, id_element, classes = "", "", "", "", ""
        # kwargs va contenir de manière dynamique les params du filter
        kwargs = {}
        kwargs['archived'] = "0"
        indicateur_liste_classes = ""
        liste_classes = []
        classes_selectionnees = []
        les_classes = []
        id_des_classes = []
        # etape1: Récupération des paramètres
        niveau_recherche = int(donnees[1])
        print("Les données ici: ", donnees)
        print("niveau_recherche: ", niveau_recherche)
        choix = donnees[2]
        if niveau_recherche == 1: #id_sousetab == all
            # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + etab + "²²~~" + id_etab;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            # on cherche les TypePaiementEleve dont le indicateur_liste_classes est sous la forme
            # "etab_nom_etab_id_etab
            etat = donnees[2]
            genre = donnees[5]
            parent = donnees[3]
            id_parent = donnees[4]
            date_deb = donnees[6]
            date_fin = donnees[7]
            order_by = donnees[8]
            sens_tri = donnees[9]

            indicateur_liste_classes = "etab_"+parent+"_"+id_parent

            print(genre)
            if genre != "tous":
                kwargs['sexe'] = genre

            
            # kwargs['date_deb_en'] = date_deb
            # kwargs['date_fin_en'] = date_fin
            # print("1date_deb: ",date_deb, "date_fin: ",date_fin)

        elif niveau_recherche == 2: #id_cycle == all
        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + sousetab  + "²²~~" + id_sousetab;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            # on cherche les TypePaiementEleve dont le indicateur_liste_classes est sous la forme
            # sousetab_nom_sousetab_id_sousetab
            etat = donnees[2]
            genre = donnees[5]
            parent = donnees[3]
            id_parent = donnees[4]
            date_deb = donnees[6]
            date_fin = donnees[7]
            order_by = donnees[8]
            sens_tri = donnees[9]

            indicateur_liste_classes = "sousetab_"+parent+"_"+id_parent
            if genre != "tous":
                kwargs['sexe'] = genre
        elif niveau_recherche == 3: #id_niveau == all
        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + cycle  + "²²~~" + id_cycle;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            etat = donnees[2]
            genre = donnees[5]
            parent = donnees[3]
            id_parent = donnees[4]
            date_deb = donnees[6]
            date_fin = donnees[7]
            order_by = donnees[8]
            sens_tri = donnees[9]

            if genre != "tous":
                kwargs['sexe'] = genre
            indicateur_liste_classes = "cycle_"+parent+"_"+id_parent

        elif niveau_recherche == 4: #sinon
        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + niveau  + "²²~~" + id_niveau + "²²~~" + specialite  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by;
            etat = donnees[2]
            genre = donnees[11]
            parent = donnees[3]
            id_parent = donnees[4]
            element = donnees[5]
            id_element = donnees[6]
            classes = donnees[7]
            date_deb = donnees[12]
            date_fin = donnees[13]
            order_by = donnees[14]
            sens_tri = donnees[15]
            sousetab_id = int(donnees[16])
        # equal permet de savoir si le nbre de classes affichées est égal au nbre de classe selected
            equal = donnees[8]
            nbre_classes = int(donnees[9])
            nbre_classe_selected = int(donnees[10])

            if genre != "tous":
                kwargs['sexe'] = genre
            if element == "tous":
                if nbre_classe_selected == 0:
                    indicateur_liste_classes = "niveau_"+parent+"_"+id_parent
                else:
                    if equal == "yes":
                        indicateur_liste_classes = "niveau_"+parent+"_"+id_parent
                    else:
                        indicateur_liste_classes = "classe"
            else:
                print("ICI")
                if nbre_classe_selected == 0:
                    indicateur_liste_classes = "specialite_"+element+"_"+id_element
                else:
                    if equal == "yes":
                        indicateur_liste_classes = "specialite_"+element+"_"+id_element
                    else:
                        indicateur_liste_classes = "classe"


        print("indicateur_liste_classes", indicateur_liste_classes)

        if indicateur_liste_classes != "classe":
            # if "specialite" in indicateur_liste_classes and ("aucune" in indicateur_liste_classes or "all" in indicateur_liste_classes):
            if "specialite" in indicateur_liste_classes and ("aucune" in indicateur_liste_classes or "tous" in indicateur_liste_classes):
                liste_classes = TypePayementEleve.objects.values('liste_classes').filter(indicateur_liste_classes = indicateur_liste_classes, id_sousetab = sousetab_id)
            else:
                liste_classes = TypePayementEleve.objects.values('liste_classes').filter(indicateur_liste_classes = indicateur_liste_classes)
            

            if liste_classes.count()>0:
                liste_classes = liste_classes[0]
                current = liste_classes['liste_classes'].split("_")
                id_des_classes = current[0:][::2]
                les_classes = current[1:][::2]

                id_des_classes.pop(len(id_des_classes) - 1)
                i = 0
                for j in les_classes:
                    classes_selectionnees.append(id_des_classes[i]+"_"+j+"_")
                    i += 1
                # print("ici", classes_selectionnees)
            else:
                terminer = True
        else:
            clss = classes.split(",")
            for cl in clss:
                c, id_c = cl.split("_")
                les_classes.append(c)
                id_des_classes.append(id_c)
                classes_selectionnees.append(id_c+"_"+c+"_")
        print("liste_classes: ", classes_selectionnees)

        # if indicateur_liste_classes != "classe":
        #     liste_classes = TypePayementEleve.objects.values('liste_classes').filter(indicateur_liste_classes = indicateur_liste_classes)[0]
        #     current = liste_classes['liste_classes'].split("_")
        #     id_des_classes = current[0:][::2]
        #     les_classes = current[1:][::2]

        #     id_des_classes.pop(len(id_des_classes) - 1)
        #     i = 0
        #     for j in les_classes:
        #         classes_selectionnees.append(id_des_classes[i]+"_"+j+"_")
        #         i += 1
        #     print("id_des_classes: ", id_des_classes)
        #     print("les_classes: ", les_classes)
        # else:
        #     clss = classes.split(",")
        #     for cl in clss:
        #         c, id_c = cl.split("_")
        #         les_classes.append(c)
        #         id_des_classes.append(id_c)
        #         classes_selectionnees.append(id_c+"_"+c+"_")
        # print("liste_classes: ", classes_selectionnees)
        if terminer == False:
        # gestion de la date
            kwargs_date['entree_sortie_caisee'] = "e"
            if date_deb != "" and date_fin != "":
                kwargs_date['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb
                kwargs_date['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin

            elif date_deb != "" and date_fin == "":
                kwargs_date['{0}__{1}'.format('date_deb_en', 'lte')] = date_deb

            elif date_deb == "" and date_fin != "":
                kwargs_date['{0}__{1}'.format('date_fin_en', 'gte')] = date_fin
                
                
            print(kwargs_date)
            print(kwargs)
            tpes = TypePayementEleve.objects.values('libelle','date_deb_en','date_fin_en','ordre_paiement','date_deb','date_fin','liste_classes','indicateur_liste_classes','entree_sortie_caisee','montant').filter(**kwargs_date).order_by('ordre_paiement')
            [print("yo ",t['libelle']) for t in tpes]
            
            t_liste_classes = []
            t_liste_montants = []
            t_liste_libelles = []
            for t in tpes:
                t_liste_classes.append(t['liste_classes'])
                t_liste_montants.append(t['montant'])
                t_liste_libelles.append(t['libelle'])
            # print(t_liste_classes)
            print(t_liste_montants)
            etat = donnees[2]
            print("etat: ", etat, " niveau_recherche: ", niveau_recherche)

            # argument_list = []
            order_by = order_by.lower()
            if order_by == "excédent":
                order_by = "excedent"
            if order_by == "prénom":
                order_by = "prenom" 
            if order_by == "classe":
                order_by = "id_classe_actuelle"
            if order_by == "versé":
                order_by = "verse"

            

            i = 0
            
            if etat == "previsions":
                for c in classes_selectionnees:
                    montant_previsionnel_classe = 0
                    montant_total_eleves_classe = 0
                    taux_recouvrement_classe = 0
                    kwargs['id_classe_actuelle'] = int(id_des_classes[i])
                    nb_eleve_classe = Eleve.objects.filter(**kwargs).count()
                    bourse_total += Eleve.objects.filter(**kwargs).aggregate(Sum('bourse'))['bourse__sum'] 
                    montant_total_eleves_classe = Eleve.objects.filter(**kwargs).aggregate(Sum('compte'))['compte__sum']
                    montant_total_eleves +=  montant_total_eleves_classe
                    excedent_total_eleves += Eleve.objects.filter(**kwargs).aggregate(Sum('excedent'))['excedent__sum'] 
                    print(kwargs,les_classes[i],nb_eleve_classe)
                    # print("t_liste_classes: ", t_liste_classes)
                    print("**classe: ", c)
                    k = 0
                    for t in t_liste_classes:
                        if c in t:
                            print(t_liste_libelles[k], t_liste_montants[k])
                            montant_previsionnel_classe += t_liste_montants[k] * nb_eleve_classe
                        k += 1
                    montant_previsionnel += montant_previsionnel_classe
                    taux_recouvrement_classe = montant_total_eleves_classe * 100/montant_previsionnel_classe if montant_previsionnel_classe > 0 else 0
                    taux_recouvrement_classe = "{:.2f}".format(taux_recouvrement_classe);

                    info_classes.append({'classe':les_classes[i], 'montant_previsionnel_classe':montant_previsionnel_classe,'montant_total_eleves_classe':montant_total_eleves_classe,'taux_recouvrement_classe':taux_recouvrement_classe})
                    i += 1
                    print(bourse_total,montant_total_eleves,excedent_total_eleves, nb_eleve_classe)
                    # on prend montant_previsionnel montant_total_eleves et excedent_total_eleves

                taux_recouvrement = montant_total_eleves * 100/montant_previsionnel if montant_previsionnel > 0 else 0
                # print(taux_recouvrement)
                taux_recouvrement = "{:.2f}".format(taux_recouvrement);
                print(montant_previsionnel, bourse_total,montant_total_eleves,excedent_total_eleves, taux_recouvrement)
                # for c in classes_selectionnees:
                #     if c in tpes[]
                # Pr chaque classe selectionnée on cherches les tranches associées puis pr chq elv de cette
                # classe on calcule le montant de toutes ces tranches - le montant de sa bourse
                # on somme tout cela --> montant prévisionel
                # puis on parcourt les eleves prend montants deja versé
                # moins les bourses --> montant existant
            elif etat == "eleves_inscrits":
                print(etat)
                choix_retour = 2
                ind = 0
                nb_classes = len(les_classes) - 1
                while ind <= nb_classes:
                    # argument_list.append( Q(**{'id_classe_actuelle':int(id_cl)} )) 
                    j = 0
                    # nb_tranches = len(t_liste_classes) - 1
                    nb_tranches = len(t_liste_classes)
                    total = 0
                    # print("*** NB TRANCHES: ", nb_tranches)
                    while j < nb_tranches:
                        print("**t_liste_montants[j]: ", t_liste_montants[j], total)
                        if classes_selectionnees[ind] in t_liste_classes[j]:
                            total += t_liste_montants[j]
                        j += 1
                    reste = 0
                    eleves = []
                    if genre == "tous":
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])))
                    else:
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])) &
                            Q(sexe=genre))

                    for e in eleves:
                        compte = e.compte
                        reste = total - compte
                        if reste <= 0:
                            excedent = reste*(-1) + e.excedent
                            info_eleves.append({'matricule':e.matricule, 'nom':e.nom, 'prenom': e.prenom,
                             'classe':e.classe_actuelle, 'id_classe':e.id_classe_actuelle,'total':total,
                             'excedent':excedent, 'verse':compte})
                    ind += 1

                if sens_tri == "desc":
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by], reverse=True)
                else:
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by])

                # Pr chaque classe ds tpes on recupere les tranches puis pr chq elv de cette
                # classe on calcule le montant de toutes ces tranches - le montant de sa bourse
                # On retient ceux qui sont en règle sur la période considérée
            elif etat == "eleves_non_inscrits":
                print(etat)
                choix_retour = 2
                ind = 0
                nb_classes = len(les_classes) - 1
                while ind <= nb_classes:
                    # argument_list.append( Q(**{'id_classe_actuelle':int(id_cl)} )) 
                    j = 0
                    # nb_tranches = len(t_liste_classes) - 1
                    nb_tranches = len(t_liste_classes)
                    total = 0
                    while j < nb_tranches:
                        if classes_selectionnees[ind] in t_liste_classes[j]:
                            total += t_liste_montants[j]
                        j += 1
                    reste = 0
                    eleves = []
                    if genre == "tous":
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])))
                    else:
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])) &
                            Q(sexe=genre))

                    for e in eleves:
                        compte = e.compte
                        reste = total - compte
                        if reste > 0:
                            info_eleves.append({'matricule':e.matricule, 'nom':e.nom, 'prenom': e.prenom,
                             'classe':e.classe_actuelle, 'verse':compte, 'id_classe':e.id_classe_actuelle,'total':total})
                    ind += 1

                if sens_tri == "desc":
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by], reverse=True)
                else:
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by])

                # Pr chaque classe ds tpes on recupere les tranches puis pr chq elv de cette
                # classe on calcule le montant de toutes ces tranches - le montant de sa bourse
                # On retient ceux qui sont en règle sur la période considérée
            else: # etat == "eleves_tous"
                print(etat)
                choix_retour = 2
            # Pr chaque classe ds tpes on recupere les tranches puis pr chq elv de cette
            # classe on calcule le montant de toutes ces tranches - le montant de sa bourse
                ind = 0
                nb_classes = len(les_classes) - 1
                print("nb_classes: ", nb_classes, classes_selectionnees[0])

                while ind <= nb_classes:
                    # argument_list.append( Q(**{'id_classe_actuelle':int(id_cl)} )) 
                    j = 0
                    nb_tranches = len(t_liste_classes) - 1
                    total = 0
                    while j <= nb_tranches:
                        if classes_selectionnees[ind] in t_liste_classes[j]:
                            total += t_liste_montants[j]
                        j += 1
                    reste = 0
                    eleves = []
                    if genre == "tous":
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])))
                    else:
                        eleves = Eleve.objects.filter( Q(archived="0") & Q(id_classe_actuelle=int(id_des_classes[ind])) &
                            Q(sexe=genre))
                    for e in eleves:
                        print("eleve: ", e.nom)
                        compte = e.compte
                        reste = total - compte
                        info_eleves.append({'matricule':e.matricule, 'nom':e.nom, 'prenom': e.prenom,
                         'classe':e.classe_actuelle, 'verse':compte,'id_classe':e.id_classe_actuelle,'total':total,
                         'reste':reste, 'excedent':e.excedent})
                    ind += 1


                if sens_tri == "desc":
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by], reverse=True)
                else:
                    info_eleves = sorted(info_eleves, key=lambda k: k[order_by])

            if choix_retour == 2:
                [print(e['nom'],e['matricule']) for e in info_eleves]

                # for e in info_eleves:
                #     print(e)
                #     break


    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default
    print("AVANT RETOUR AJAX")
    if imprimer == False:
        if terminer == True:
            data = {
                "choix":choix,
                "montant_previsionnel": 0,
                "montant_total_eleves": 0,
                "excedent_total_eleves": 0,
                "taux_recouvrement": 0,
                "type_paiements_associes": [],
                "info_classes": [],
                "info_eleves": [],
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }
        else:
            if choix_retour == 0: #Pr la selection des classes, niveaux, specialite
                data = {
                    "choix":choix,
                    "sousetabs": sousetabs,
                    "cycles": cycles,
                    "niveaux": niveaux,
                    "classes": classes,
                    "specialites": specialites,
                    "order_by": order_by,
                    "permissions" : permissions_of_a_user(request.user),
                    "data_color" : data_color,
                    "sidebar_class" : sidebar_class,
                    "theme_class" : theme_class,
                }
            elif choix_retour == 1: # previsions - existant
                # montant_previsionnel, bourse_total,montant_total_eleves,excedent_total_eleves, taux_recouvrement
                data = {
                    "choix":choix,
                    "montant_previsionnel": montant_previsionnel,
                    "montant_total_eleves": montant_total_eleves,
                    "excedent_total_eleves": excedent_total_eleves,
                    "taux_recouvrement": taux_recouvrement,
                    "info_classes": info_classes,
                    "order_by": order_by,
                    "permissions" : permissions_of_a_user(request.user),
                    "data_color" : data_color,
                    "sidebar_class" : sidebar_class,
                    "theme_class" : theme_class,
                }
            elif choix_retour == 2: #apprenant en regle, pas en regle, tous
                data = {
                    "choix":choix,
                    "info_eleves":info_eleves,
                    "order_by": order_by,
                    "permissions" : permissions_of_a_user(request.user),
                    "data_color" : data_color,
                    "sidebar_class" : sidebar_class,
                    "theme_class" : theme_class,
                }
            elif choix_retour == 3:
                data = {
                    "choix":choix,
                    "type_paiements_associes": type_paiements_associes,
                    "permissions" : permissions_of_a_user(request.user),
                    "data_color" : data_color,
                    "sidebar_class" : sidebar_class,
                    "theme_class" : theme_class,
                }
       
        return JSONResponse(data)
    else:
        if terminer == True:
            data = {
                "choix":choix,
                "montant_previsionnel": 0,
                "montant_total_eleves": 0,
                "excedent_total_eleves": 0,
                "taux_recouvrement": 0,
                "type_paiements_associes": [],
                "info_classes": [],
                "info_eleves": [],
            }
        elif choix_retour == 1:
            data = {
                "choix":choix,
                "montant_previsionnel": montant_previsionnel,
                "montant_total_eleves": montant_total_eleves,
                "excedent_total_eleves": excedent_total_eleves,
                "taux_recouvrement": taux_recouvrement,
                "info_classes": info_classes,
                "order_by": order_by,

            }
        elif choix_retour == 2:
            data = {
                "choix":choix,
                "info_eleves":info_eleves,
                "order_by": order_by,
            }
        elif choix_retour == 3:
            data = {
                "choix":choix,
                "type_paiements_associes": type_paiements_associes,
            }
        return data

def etats_paiements_eleves(request):
    if request.method == 'POST':

        if(request.is_ajax()):
            return etats_paiements_eleves_fonction(request)
    
        else:
            # On veut imprimer On va procéder à la réécriture de donnees au m format que lorsqu'on
            # veut effectuer la requete ajax ci-dessus et on va appeler
            # etats_paiements_eleves_fonction(request, True, donnees) qui va nous retourner les data à
            # imprimer.

            donnees = request.POST['donnees_imprimer'].split("²²~~")

            etab = donnees[0]
            sousetab = donnees[1]
            cycle = donnees[2]
            niveau = donnees[3]
            specialite = donnees[4]
            classes = donnees[5]
            nbre_classes = donnees[6]
            nbre_classes_selected = donnees[7]
            genre = donnees[8]
            etats = donnees[9]
            date_deb = donnees[10]
            date_fin = donnees[11]
            order_by = donnees[12]
            sens_tri = donnees[13]           
            niveau_recherche = "1"
            position = "7"
            donnees = ""
            titre = ""
            titre_etat = ""
            filename = ""
            print("SPECIALITE***! ", specialite)

            if etats == "previsions":
                titre = "Prévision - Existant"
                titre_etat = "Prévision - Existant: "
                filename = "Prevision_existant_"
            elif etats == "eleves_tous":
                titre = "Apprenants en règle | pas en règle"
                titre_etat = "Apprenants en règle | pas en règle: "
                filename = "Tous_les_apprenants_"
            elif etats == "eleves_inscrits":
                titre = "Apprenants en règle"
                titre_etat = "Apprenants en règle: "
                filename = "Apprenants_en_regle_"
            else :
                titre = "Apprenants pas en règle"
                titre_etat = "Apprenants pas en règle: "
                filename = "Apprenants_pas_en_regle_"



            sousetab_, id_sousetab = sousetab.split("_")[0], sousetab.split("_")[1]
            if id_sousetab == "all":
                niveau_recherche = "1"
                etab_, id_etab = etab.split("_")[0], etab.split("_")[1]
                donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + etab_ + "²²~~" + id_etab;
                donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + sens_tri;
                titre_etat += etab_
                filename += etab_

            else:
                cycle_, id_cycle = cycle.split("_")[0], cycle.split("_")[1]
                if id_cycle == "all": 
                    niveau_recherche = "2"
                    donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + sousetab_  + "²²~~" + id_sousetab;
                    donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by+ "²²~~" + sens_tri;
                    titre_etat += sousetab_
                    filename += sousetab_

                else:
                    niveau_, id_niveau = niveau.split("_")[0], niveau.split("_")[1]
                    if id_niveau == "all":
                        niveau_recherche = "3"
                        donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + cycle_  + "²²~~" + id_cycle;
                        donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by+ "²²~~" + sens_tri;
                        titre_etat += cycle_
                        filename += cycle_

                    else:
                        niveau_recherche = "4"
                        # donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + niveau  + "²²~~" + id_niveau + "²²~~" + specialite  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal;
            # donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by + "²²~~" + id_sousetab;
                        equal = "yes" if nbre_classes == nbre_classes_selected else "no"
                        specialite_, id_specialite = specialite.split("_")[0], specialite.split("_")[1]
                        donnees = position + "²²~~" + niveau_recherche + "²²~~" + etats + "²²~~" + niveau_  + "²²~~" + id_niveau + "²²~~" + specialite_  + "²²~~" + id_specialite + "²²~~" + classes + "²²~~" + equal;
                        donnees +="²²~~" + nbre_classes+ "²²~~" + nbre_classes_selected
                        donnees += "²²~~" + genre + "²²~~" + date_deb + "²²~~" + date_fin + "²²~~" + order_by+ "²²~~" + sens_tri + "²²~~" + id_sousetab;
                        if classes != "":
                            clss = classes.split(",")
                            nom_classes =""
                            for cl in clss:
                                c, id_c = cl.split("_")
                                nom_classes += c+","
                            titre_etat += nom_classes
                            filename += nom_classes

                        elif specialite_ == "tous":
                            titre_etat += niveau_
                            filename += niveau_
                            print("NIVEAU***: ",niveau_)

                        elif specialite_ == "aucune":
                            titre_etat += niveau_+" sans spécialité"
                            filename += niveau_+"sans_specialite"

                        else :
                            titre_etat += niveau_+" "+specialite_
                            filename += niveau_+" "+specialite_




            print("Les data: ", donnees)

            data = etats_paiements_eleves_fonction(request, True, donnees)
            print("Retour avec: ",data['choix'])
            etabs = Etab.objects.values('id','nom_etab').filter(archived = "0")
            sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0")
            print("On postait")

            choix = data['choix']
            infos = []
            etat_template =""
            # Variable liées au previsons
            deficit = 0
            montant_previsionnel = 0
            montant_total_eleves= 0
            excedent_total_eleves= 0
            taux_recouvrement= 0

            # Variable pour les totaux
            verses = 0;
            totaux = 0;
            restes = 0;
            excedents = 0;

            if choix == "previsions":
                etat_template = "etat_previsions_existant_paiement_eleves_template.html"            
                infos = data['info_classes']
                montant_previsionnel = data['montant_previsionnel']
                montant_total_eleves= data['montant_total_eleves']
                excedent_total_eleves= data['excedent_total_eleves']
                taux_recouvrement= data['taux_recouvrement']
                for inf in infos:
                    inf['deficit'] = inf['montant_previsionnel_classe'] - inf['montant_total_eleves_classe']
                    deficit += inf['deficit']
            elif choix == "eleves_tous":
                etat_template = "etat_eleves_en_regle_ou_pas_template.html"
                infos = data['info_eleves']
                for inf in infos:
                    verses += inf['verse'];
                    totaux += inf['total'];
                    restes += inf['reste'];
                    excedents += inf['excedent'];

                
            elif choix == "eleves_inscrits":
                etat_template = "etat_eleves_en_regle_template.html"
                infos = data['info_eleves']
                for inf in infos:
                    verses += inf['verse'];
                    totaux += inf['total'];
                    excedents += inf['excedent'];
            elif choix == "eleves_non_inscrits":
                etat_template = "etat_eleves_pas_en_regle_template.html"
                infos = data['info_eleves']
                for inf in infos:
                    verses += inf['verse'];
                    totaux += inf['total'];
                    inf['reste'] = inf['total'] - inf['verse']
                    restes += inf['reste'];

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = ('attachment; filename={}'.format(filename))
            response['Content-Transfer-Encoding'] = 'binary'

            forme = "a4"
            
            css = CSS(string='@page { size: A4; margin: 1cm }')
            template_name = 'mainapp/pages/{}'.format(etat_template)
            nb = 1
            cpte = 0
            documents = []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            font_config = FontConfiguration()
            i = 1
            

            dict1 = {
                    'pays': 'republique du cameroun',
                    'ministere': 'ministère des enseignements secondaires',
                    'etab': 'Lycee General Leclerc',
                    'devise' : 'discipline-travail-succès',
                    'contact' : 'BP. 116 Tel: 678908723',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                    'eleves': [],
                    'titre': titre,
                    'titre_etat': titre_etat,
                    'montant_previsionnel': montant_previsionnel,
                    'montant_total_eleves': montant_total_eleves,
                    'excedent_total_eleves': excedent_total_eleves,
                    'taux_recouvrement': taux_recouvrement,
                    'deficit': deficit,
                    'infos': infos,
                    'verses':  verses,
                    'totaux': totaux,
                    'restes': restes,
                    'excedents': excedents,

                    }
            dict2 = {
                    'pays2': 'republic of cameroon',
                    'ministere2': 'ministry of secondary education',
                    'etab2': 'ghs general leclerc',
                    'devise2' : 'discipline-hardwork-success',
                    'contact2' : 'PoBox. 116 Tel: 678908723',
                    'invoice_id2' : 151,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                    'today2': date.today(), 
                    'amount2': 39.99,
                    'customer_name2': 'Cooper Mann'+ str(cpte),
                    'order_id2': 1233434,
                    }
            dict3 = {**dict1, **dict2}

            

            while cpte < nb:
                html = render_to_string(template_name, dict3)
                document = HTML(string=html, base_url=request.build_absolute_uri()).render( stylesheets=[css],presentational_hints=True,font_config=font_config)
                documents.append(document)
                i += 1
                cpte += 1

            all_pages = [page for document in documents for page in document.pages]
            documents[0].copy(all_pages).write_pdf(response)
            
            return response

    else:
        etabs = Etab.objects.values('id','nom_etab').filter(archived = "0")
        sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0")
        print("GET")

    return render(request, 'mainapp/pages/etats-paiements-eleves.html', locals())

def liste_eleve_pdf(request):
    # if(request.is_ajax()):
    # donnees = request.POST['form_data']
    classe, id_classe = request.POST['classe_recherchee'].split('_')[0], int(request.POST['classe_recherchee'].split('_')[1])
    # print("request.POST['classe_recherchee']: ",request.POST['classe_recherchee'])
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = ('inline; filename="liste_eleves_6eA.pdf"')
    filename = "liste_eleves_{}.pdf".format(classe)
    response['Content-Disposition'] = "attachment; filename={}".format(filename)
    response['Content-Transfer-Encoding'] = 'binary'
    # filename = "letter.pdf"
    # content = "inline; filename=%s" %(filename)

    forme = "a4"
    eleves = Eleve.objects.filter(id_classe_actuelle = id_classe)
    # eleves = Eleve.objects.filter(pk= 1)
    # list_group = [5]*22
    list_group = []
    list_group.append(5)
    list_group.append(5)
    list_group.append(5)
    list_group.append(3)
    size_font = '20px'
    if forme == "a5":
        css = CSS(string='@page { size: A4 landscape ; margin: 0.5cm }')
        template_name = 'mainapp/pages/bulletinA5.html'  
        nb = 2/2
    else:
        css = CSS(string='@page { size: A4; margin: 0.5cm }')
        template_name = 'mainapp/pages/test.html'
        nb = 1

    # html_string = render_to_string(template_name, {
    #     'invoice_id' : 150,
    #     'today': date.today(), 
    #     'amount': 39.99,
    #     'customer_name': 'Cooper Mann',
    #     'order_id': 1233434,
    #     'etab': 'Lycee General Leclerc',
    # })
    # html = HTML(string=html_string)
    # # css = CSS(string='@page { size: A4 landscape ; margin: 0.5cm }')

    # result = html.write_pdf()

    cpte = 0
    # COMPONENTS = ['bulletinA5.html'] *4
    documents = []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    font_config = FontConfiguration()
    i = 1
    
    # for template_name in COMPONENTS:
    # list_eleve = []
    # list_eleve.append()
    # list_eleve.append()
    dict1 = {
            'pays': 'republique du cameroun',
            'ministere': 'ministère des enseignements secondaires',
            'etab': 'Lycee General Leclerc',
            'devise' : 'discipline-travail-succès',
            'contact' : 'BP. 116 Tel: 678908723',
            'invoice_id' : 150,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            'liste_apprenant' : 'liste apprenant classe de 6eA',
            'eleves': eleves,
            'nb_matiere': 20,
            'size_font': size_font,
            }
    dict2 = {
            'pays2': 'republic of cameroon',
            'ministere2': 'ministry of secondary education',
            'etab2': 'ghs general leclerc',
            'devise2' : 'discipline-hardwork-success',
            'contact2' : 'PoBox. 116 Tel: 678908723',
            'invoice_id2' : 151,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            'today2': date.today(), 
            'amount2': 39.99,
            'customer_name2': 'Cooper Mann'+ str(cpte),
            'order_id2': 1233434,
            }
    dict3 = {**dict1, **dict2}

    

    while cpte < nb:
        html = render_to_string(template_name, dict3)
        document = HTML(string=html, base_url=request.build_absolute_uri()).render( stylesheets=[css],presentational_hints=True,font_config=font_config)
        documents.append(document)
        i += 1
        cpte += 1

    all_pages = [page for document in documents for page in document.pages]
    documents[0].copy(all_pages).write_pdf(response)

    # css = CSS(string='@page { size: A5; margin: 0.5cm }')

    # # margin-left:2cm; margin-rigth: 0.5cm; margin-top: 0.5cm; margin-bottom: 0.5cm
    # html = render_to_string("mainapp/pages/test.html", {
    #     'invoice_id' : 150,
    #     'today': date.today(), 
    #     'amount': 39.99,
    #     'customer_name': 'Cooper Mann',
    #     'order_id': 1233434,
    # })

    # font_config = FontConfiguration()
    # response = HttpResponse(content_type="application/pdf")
    # HTML(string=html).write_pdf(response, stylesheets=[css], font_config=font_config)
    # # response['Content-Disposition'] = "inline; filename=result.pdf"
    # response['Content-Disposition'] = "attachment; filename=result.pdf"
    
    return response

def prendre_photos_eleve(request):

    if request.method == 'POST':
        choix =""
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            id_classe = int(donnees.split('_')[1])
            eleves = Eleve.objects.values('id','matricule','nom','prenom').filter(id_classe_actuelle = id_classe).order_by('nom')
            # donnees = donnees.split("²²~~")
            print(donnees)
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            print("LE CHOIX ...",choix)
            data = {
                "choix":"prendre_photos_eleve",
                "eleves": eleves,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
    decompte = 0
    total = 0
    valide_ip_port = True
    ip = request.POST['ip_address']
    port = request.POST['port_number']
    intervalle_ch = request.POST['intervalle'] if request.POST['intervalle'].isdigit() else "100"
    intervalle = int(intervalle_ch)
    valide_ip_port = port.isdigit() and ip.replace('.','').isdigit()
    if valide_ip_port:
        eleves = []
        nbre_eleves = len(request.POST) - 5
        for r in request.POST:
            if r.count('_') == 3:
                id_eleve, matricule, nom, prenom = r.split('_')
                id_eleve = int(id_eleve)
                eleves.append([id_eleve, matricule, nom, prenom])
        # for e in eleves:
        #     print(e[0],e[1],e[2],e[3])
        i = 0
        url = "http://"+ip+":"+port+"/shot.jpg"

        # font 
        font = cv2.FONT_HERSHEY_SIMPLEX 
          
        # org 
        org = (2, 50) 
          
        # fontScale 
        fontScale = 0.75
           
        # Blue color in BGR 
        color = (255, 0, 0) 
          
        # Line thickness of 2 px 
        thickness = 2

        while True:

            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            img2 = cv2.imdecode(img_arr, -1)
               
            # Using cv2.putText() method 
            decompte_ch =str(decompte)
            image = cv2.putText(img, (intervalle_ch)+" -- "+decompte_ch+" Pour: "+ eleves[i][1]+" "+eleves[i][2]+" "+eleves[i][3], org, font, fontScale, color, thickness, cv2.LINE_AA)

            if decompte == intervalle:
                playsound(photo_eleves_repertoire+"camera-shutter.mp3")
                decompte = 0
                eleve = eleves[i][1]+"_"+eleves[i][2]+"_"+eleves[i][3]
                cv2.imwrite(photo_eleves_repertoire+ eleve +".jpg", img2)
                Eleve.objects.filter(pk = eleves[i][0]).update(photo_url = "/media"+photo_repertoire+eleve+".jpg",\
                    photo = photo_repertoire+eleve+".jpg")
                i += 1
            cv2.imshow("AndroidCam", image)
            # time.sleep(3)
            decompte += 1
            total += 1

            if i == nbre_eleves:
                print("Decompte est: ", total)
                cv2.destroyAllWindows()
                break
            # cv2.waitKey(1) attend 1ms si on saisit: renvoie -1 si pas de saisie, 27 si c'est escape
            key = cv2.waitKey(1)
            # key == 27 alors l'utilisateur a décidé d'arrêter le processus de prise de photos
            if key == 27:
                print("Decompte est: ", total)
                cv2.destroyAllWindows()
                break
            # key != -1 and key != 27 l'user a pressé une touche # de ESC donc l'eleve etait pret avant
            # la fin de son compte à rebours
            elif key != -1 and key != 27:
                playsound(photo_eleves_repertoire+"camera-shutter.mp3")
                decompte = 0
                eleve = eleves[i][1]+"_"+eleves[i][2]+"_"+eleves[i][3]
                cv2.imwrite(photo_eleves_repertoire+ eleve +".jpg", img2)
                Eleve.objects.filter(pk = eleves[i][0]).update(photo_url = "/media"+photo_repertoire+eleve+".jpg",\
                    photo = photo_repertoire+eleve+".jpg")
                print("key # 27 pressed: ", i, nbre_eleves)

                i += 1
                if i == nbre_eleves:
                    print("fin avec key # 27: ", total)
                    cv2.destroyAllWindows()
                    break
            

    return redirect('mainapp:liste_eleves')

def dashboard(request):

    classes = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

    
    return render(request, 'mainapp/pages/dashboard.html', locals())

def changement_classe_eleve(request):
    # id+"_"+matricule+"_"+nom+"_"+prenom+"_"+sexe

    print("Changement de classe")
    classe, id_classe = request.POST['classe_selected2'].split('_')
    id_classe = int(id_classe)
    print("Cls Id: ", classe, id_classe)
    id_eleve, matricule, nom, prenom, sexe, id_classe_actuelle, classe_actuelle = request.POST['info_apprenant'].split('_')
    id_eleve = int(id_eleve)
    # id_classe_actuelle = int(id_classe_actuelle)
    eleve = Eleve.objects.get(archived = "0", pk = id_eleve)

    # print("id_eleve mat, nom, prenom, sexe, id_classe_actuelle, classe_actuelle: ", id_eleve, matricule, nom, prenom, sexe, id_classe_actuelle, classe_actuelle)
    # el2 = Eleve.objects.values('id_classe_actuelle','classe_actuelle').get(pk = id_eleve)
    # print(el2['id_classe_actuelle'], el2['classe_actuelle'])
    # # On ne verifiera plus nb_eleve_classe à la prochaine migartion
    # nb_eleve_classe = Classe.objects.filter(pk=id_classe_actuelle,annee_scolaire=ANNEE_SCOLAIRE)[0]\
    #                                 .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
    #                                 .eleves.count()
    # if nb_eleve_classe > 0:

    # L'élève est déja dans la classe si is_eleve_in_classe = 1
    is_eleve_in_classe = Classe.objects.filter(pk=id_classe,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                    .eleves.filter(pk = id_eleve).count()
    if is_eleve_in_classe == 0:                                
        Classe.objects.filter(pk=id_classe_actuelle,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                        .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                        .eleves.remove(eleve)

        classe_changee = str(id_classe_actuelle)+"_"+classe_actuelle+"_"
        liste_classes_changees  = eleve.liste_classes_changees
        # if classe_changee not in liste_classes_changees:
        liste_classes_changees += classe_changee
        print(classe_changee, liste_classes_changees)

        print("is_eleve_in_classe == 0")
        eleve.id_classe_actuelle = id_classe
        eleve.classe_actuelle = classe
        eleve.liste_classes_changees = liste_classes_changees
        eleve.save()
        eleve = Eleve.objects.get(archived = "0", pk = id_eleve)

        Classe.objects.filter(pk=id_classe,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                    .eleves.add(eleve)
    # print("Eleve.count et liste_classes_changees: ", is_eleve_in_classe, eleve.liste_classes_changees)
    return redirect('mainapp:liste_eleves')

def creation_etudiant(request):

    if request.method == 'GET': 
        return render(request, 'mainapp/pages/creation-etudiant.html',{'form':EtudiantForm})
    elif request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            # matricule = form.cleaned_data['matricule']
            matlast = Etudiant.objects.filter().order_by('-id').values_list('matricule')[0]
            # matlast = "HT19A032"
            sousEtab = SousEtab.objects.filter()[0]

            matformat = sousEtab.format_matricule
            mat_fixedindex = int(sousEtab.mat_fixedindex)
            mat_yearindex = int(sousEtab.mat_yearindex)
            mat_varyindex = int(sousEtab.mat_varyindex)
            first_matricule = sousEtab.first_matricule

            # position = [x for x in range(mat_varyindex)]

            position2 = sousEtab.position

            position3 = list(position2)
            position = [0]*mat_varyindex
            idf = 0
            for item in position3:
                if item in '0123456789':
                    position[idf] = int(item)
                    idf += 1
                    # print("position : ", position)
            
            matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast[0]))
            # matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))

            # exists_mat_nb = Etudiant.objects.filter(matricule=matlast[0]).count()
            exists_mat_nb = Etudiant.objects.filter(matricule__icontains=matricule).count()
            
            while exists_mat_nb > 0:
                matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matricule))
                exists_mat_nb = Etudiant.objects.filter(matricule__icontains=matricule).count()
                print("On Boucle ...")

            # print("Exists Mat: ", exists_mat)
            print("NEW MAT: ", matricule)
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            age = form.cleaned_data['age']

            etudiant = Etudiant(
            matricule = matricule, 
            nom = nom,
            prenom = prenom,
            age = age
            )
            etudiant.save()

            return redirect('mainapp:liste_etudiants')

def paiement_eleve(request):
    
    if request.method == 'POST':
        excedent = 18000
        bourse = 22000
        compte = 0
        # Par défaut l'eleve n'est pas en regle
        est_en_regle = "0"

        classe_courante = request.POST.get('classe_courante', None)
        montant_a_payer = float(request.POST['montant_a_payer2'].replace(",","."))
        crediter = float(request.POST['crediter'].replace(",","."))
        print("IN ",request.POST['info_eleve'])
        compte, bourse, excedent, matricule = request.POST['info_eleve'].split("_")
        compte, bourse, excedent = compte.replace(",","."), bourse.replace(",","."), excedent.replace(",",".")
        compte, bourse, excedent = float(compte), float(bourse), float(excedent)

        total = compte + crediter + bourse + excedent

        if total >= montant_a_payer:
            excedent = total - montant_a_payer
            bourse = 0
            compte = montant_a_payer
            est_en_regle = "1"
        else:
            excedent = 0
            bourse = 0
            compte = total
            est_en_regle = "0"
        Eleve.objects.filter(matricule__iexact = matricule).update(compte = compte, bourse = bourse, excedent = excedent, est_en_regle = est_en_regle)

        print("compte, bourse, excedent, matricule: ",compte)

        request.session['classe_courante'] = classe_courante

    return redirect('mainapp:liste_eleves' )

def attribution_bourse_eleve(request):
    if request.method == 'POST' or request.method == 'GET':
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            print("Les donnees: ", donnees)
            id_eleve = donnees[0]
            info = Eleve.objects.values('liste_bourses','bourse').filter(pk = id_eleve)[0]
            liste_bourses = info['liste_bourses']
            bourse = info['bourse']
            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            
            data = {
                "choix": "eleve_bourse_info",
                "montant_bourse": bourse,
                "liste_bourses": liste_bourses,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }
            return JSONResponse(data)
        liste_bourses = ""
        liste_bourses_afficher = ""
        id_eleve =  id_eleve = int(request.POST['id_eleve'])
        info = Eleve.objects.values('liste_bourses','bourse').filter(pk = id_eleve)[0]
        fini = False

        if info['bourse'] == 0 and len(info['liste_bourses'])>0:
            fini = True
        if fini == False:
            bourse = 0
            for r in request.POST:
                item = request.POST[r]
                print(r)
                if r != "id_eleve" and item.replace('.','',1).isdigit():
                    n = len(r.split("_"))
                    if n == 3:
                        libelle,id, autre = r.split("_")
                        # if float(item) != 0:
                        
                        if libelle+"_"+id in request.POST:
                            item = request.POST[libelle+"_"+id]
                            
                            if item.replace('.','',1).isdigit():
                                liste_bourses += id+"_"+libelle+"_"+item+"_"
                                liste_bourses_afficher += libelle+", "
                            else:
                                item = "0"
                        else:
                            liste_bourses += id+"_"+libelle+"_"+item+"_"
                            liste_bourses_afficher += libelle+", "

                        bourse += float(item)
                        print("libelle, montant: ", libelle, item)
            
            print("--Liste_bourses: ", liste_bourses)

            Eleve.objects.filter(pk = id_eleve).update(bourse = bourse, liste_bourses = liste_bourses, liste_bourses_afficher= liste_bourses_afficher)
        else:
            # Bourse deja utilisée
            print("Modification plus possibles!")
        return redirect('mainapp:liste_eleves')

def creation_type_paiement_eleve(request):
    print("****************creation_type_paiement_eleve")
    if request.method == 'GET':
        return render(request, 'mainapp/pages/creation-type-paiement-eleve.html',{'form':TypePayementEleveForm})
    elif request.method == 'POST':
        sousetabs = []
        cycles = []
        niveaux = []
        classes = []
        specialites = []
        choix =""
        id_sousetab_to_save, sousetab_to_save = 0,""
        id_etab_to_save = ""
        id_cycle_to_save = 0
        id_niveau_to_save, niveau_to_save = 0,""
        save_cycle = False
        save_niveau = False
        save_etab = False
        save_sousetab = False
        # niveau_id = ""


        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            print("Les donnees: ", donnees)
            position = donnees[0]
            param2 = donnees[1] if donnees[1] == "all" else int(donnees[1])
            param3 = donnees[2]
            # param4 represente l'id du parent et peut etre all ou un id
            param4 = donnees[3]
            print("PYTHON: ",position,param2, param3,param4)

            # L'etab a changé on cherche les sousetabs associés
            if position == "1":
                param2 = 1
                choix = "etab"
                sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(id_etab = param2)
                
            # Le sousetab a changé on cherche les niveaux et spécialités associés
            if position == "2":
                choix = "sousetab"
                
                cycles = Cycle.objects.values('id', 'nom_cycle').filter(id_sousetab = param2)
                # print("cycles count: ", cycles.count())
                print("cycles", cycles)

            
            # Le cycle a changé
            if position == "3":
                print("PARAM2: ",param2)
                choix = "cycle"
                # if param3 == "tous":
                #     print("cycle tous: ", param4)
                #     niveaux = Niveau.objects.values('id', 'nom_niveau').filter(archived = "0", id_cycle = int(param4))
                # else:
                niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_cycle = param2)

            # Le niveau a changé
            if position == "4":
                print("PARAM2: ",param2)
                choix = "niveau"
                # if param3 == "tous":
                #     print("tous niveau")
                #     specialites = Specialite.objects.values('id', 'specialite').filter(archived = "0", id_niveau = int(param4))
                # else:
                specialites = Specialite.objects.values('id', 'specialite').filter(archived = "0", id_niveau = param2)
                classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2)

            # La spécialité a changé
            if position == "5":
                choix = "specialite"
                print("PARAM2: ",param2, "PARAM3:",param3)
                specialite, id_specialite = param3.split('_')[0],param3.split('_')[1]
                # if id_specialite == "aucune":
                if specialite == "aucune":
                    print("DANS AUCUNE")
                    classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = "")
                # elif id_specialite == "all":
                elif specialite == "tous":
                    classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2)
                else:
                    classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = specialite)
                print("# classes: ", classes.count())

            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default

            data = {
                "choix":choix,
                "sousetabs": sousetabs,
                "cycles": cycles,
                "niveaux": niveaux,
                # "niveau_id": niveau_id,
                "classes": classes,
                "specialites": specialites,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)

        else:
            print("On va save en bd")
            liste_classes = ""
            liste_classes_afficher = ""
            indicateur_liste_classes = ""
            etab = Etab.objects.values_list('id','nom_etab').all()[0]
            nom_etab = etab[1]
            id_etab = etab[0]
            id_etab_to_save = int(id_etab)
            save_etab = True
            choix_sousetab, id_sousetab = request.POST['choix_sousetab'].split("_")
            if choix_sousetab == "tous":
                classes = Classe.objects.values_list('id','nom_classe').all()
                for c in classes:
                    liste_classes += str(c[0])+"_"+c[1]+"_"
                liste_classes_afficher = nom_etab
                indicateur_liste_classes = "etab_"+ nom_etab +"_"+ str(id_etab)
                print("Liste_classes: ",liste_classes )
            else:              
                id_sousetab = int(id_sousetab)
                id_sousetab_to_save = id_sousetab
                sousetab_to_save = choix_sousetab
                save_sousetab = True
                choix_cycle, id_cycle = request.POST.get('choix_cycle').split("_")
                if choix_cycle =="tous":
                    classes = Classe.objects.values_list('id','nom_classe').filter(id_sousetab = id_sousetab)
                    for c in classes:
                        liste_classes += str(c[0])+"_"+c[1]+"_"
                    nom_sousetab = SousEtab.objects.values_list('nom_sousetab').filter(pk = id_sousetab)[0][0]
                    liste_classes_afficher = nom_sousetab
                    indicateur_liste_classes = "sousetab_" + nom_sousetab +"_"+ str(id_sousetab)
                    print("Liste_classes: ",liste_classes)
                else:
                    id_cycle = int(id_cycle)
                    id_cycle_to_save = id_cycle
                    save_cycle = True

                    choix_niveau, id_niveau = request.POST.get('choix_niveau').split("_")
                    if choix_niveau =="tous":
                        classes = Classe.objects.values_list('id','nom_classe').filter(id_cycle = id_cycle)
                        for c in classes:
                            liste_classes += str(c[0])+"_"+c[1]+"_"
                        nom_cycle = Cycle.objects.values_list('nom_cycle').filter(pk = id_cycle)[0][0]
                        liste_classes_afficher = nom_cycle
                        indicateur_liste_classes = "cycle_" + nom_cycle +"_"+ str(id_cycle)
                        print("Liste_classes: ",liste_classes)
                    else:
                        id_niveau = int(id_niveau)
                        specialite, id_specialite = request.POST.get('specialite').split("_")
                        choix_classes = request.POST.getlist('choix_classes')
                        equal = request.POST['equal']
                        # equal == yes si nb classes affichéesv == nb classes selected
                        print("equal: ", equal)
                        save_niveau = True
                        id_niveau_to_save = id_niveau
                        niveau_to_save = choix_niveau

                        # id_sousetab_to_save = id_sousetab
                        # sousetab_to_save = sousetab

                        if specialite =="tous":
                            if len(choix_classes) == 0:
                                classes = Classe.objects.values_list('id','nom_classe').filter(id_niveau = id_niveau)
                                nom_niveau = Niveau.objects.values_list('nom_niveau').filter(pk = id_niveau)[0][0]
                                liste_classes_afficher = nom_niveau
                                indicateur_liste_classes = "niveau_" + nom_niveau +"_"+ str(id_niveau)
                                for c in classes:
                                    liste_classes += str(c[0])+"_"+c[1]+"_"
                            else:
                                classes = []
                                for cl in choix_classes:
                                    classe, id_classe = cl.split("_")
                                    id_classe = int(id_classe)
                                    classes += Classe.objects.values_list('id','nom_classe').filter(pk = id_classe)
                                indicateur_liste_classes = "classe"
                                if equal == "yes":
                                    nom_niveau = Niveau.objects.values_list('nom_niveau').filter(pk = id_niveau)[0][0]
                                    indicateur_liste_classes = "niveau_" + nom_niveau +"_"+ str(id_niveau)
                                    liste_classes_afficher = nom_niveau

                                for c in classes:
                                    liste_classes += str(c[0])+"_"+c[1]+"_"
                                    if indicateur_liste_classes == "classe":
                                        liste_classes_afficher += c[1]+", "
                        else:
                            print("***Choix_niveaux: ",choix_niveau)
                            if len(choix_classes) == 0:
                                if specialite == "aucune":
                                    classes = Classe.objects.values_list('id','nom_classe').filter(id_niveau = id_niveau, specialite = "")
                                    print("aucune: ", classes.count())
                                    # indicateur_liste_classes = "specialite_"+ specialite+ "_" + id_specialite
                                    indicateur_liste_classes = "specialite_"+ specialite+ "_" + str(id_niveau)
                                    liste_classes_afficher = choix_niveau
                                else:
                                    classes = Classe.objects.values_list('id','nom_classe').filter(id_niveau = id_niveau, specialite__iexact = specialite)
                                    indicateur_liste_classes = "specialite_" + specialite + "_" + id_specialite
                                    liste_classes_afficher = choix_niveau+" "+specialite
                                for c in classes:
                                    liste_classes += str(c[0])+"_"+c[1]+"_"
                            else:
                                indicateur_liste_classes = "classe"
                                if equal == "yes":
                                    indicateur_liste_classes = "specialite_" + specialite + "_" + id_specialite
                                    liste_classes_afficher = choix_niveau+" "+specialite

                                classes = []
                                for cl in choix_classes:
                                    classe, id_classe = cl.split("_")
                                    id_classe = int(id_classe)
                                    classes += Classe.objects.values_list('id','nom_classe').filter(pk = id_classe)
                                for c in classes:
                                    liste_classes += str(c[0])+"_"+c[1]+"_"
                                    if indicateur_liste_classes == "classe":
                                        liste_classes_afficher += c[1]+", "

                                
                        print("*Liste_classes: ",liste_classes)
                        print("*indicateur_liste_classes: ",indicateur_liste_classes)
                        print("*liste_classes_afficher: ",liste_classes_afficher)
                                

            type_paiement_eleve = TypePayementEleve()
            type_paiement_eleve.liste_classes = liste_classes
            type_paiement_eleve.liste_classes_afficher = liste_classes_afficher
            type_paiement_eleve.indicateur_liste_classes = indicateur_liste_classes

            form = TypePayementEleveForm(request.POST)
            entree_sortie_caisee = request.POST['entree_sortie_caisee']
            # print(form.errors)
            # if form.is_valid():
            # libelle = form.cleaned_data['libelle']
            libelle = request.POST.get('libelle', None)
            montant = request.POST.get('montant', None)
            if montant == "":
                montant = 0
            # print("popoli ",isinstance(montant, numbers.Number))
            # if montant is empty:
            # montant = 0
            # if isinstance(montant, numbers.Number) == False:
            #     montant = 0
            # print("---montant: ", montant)
            
            # montant = form.cleaned_data['montant'] if form.cleaned_data['montant'] != None else 0
                
            if entree_sortie_caisee == "e":
                # montant = form.cleaned_data['montant']
                # ordre_paiement = form.cleaned_data['ordre_paiement']
                montant = request.POST['montant']
                ordre_paiement = request.POST['ordre_paiement']
                date_deb = request.POST['date_deb'].strip().split(" ")[0]
                date_fin = request.POST['date_fin'].strip().split(" ")[0]
                type_paiement_eleve.ordre_paiement = ordre_paiement
                mois, jour, annee = date_deb.split('/')
                date_deb_en = annee+"-"+mois+"-"+jour
                type_paiement_eleve.date_deb = jour+"-"+mois+"-"+annee
                mois, jour, annee = date_fin.split('/')
                date_fin_en = annee+"-"+mois+"-"+jour
                type_paiement_eleve.date_fin = jour+"-"+mois+"-"+annee
                type_paiement_eleve.date_deb_en = date_deb_en
                type_paiement_eleve.date_fin_en = date_fin_en
                print("date_deb_en: ", date_deb_en, " date_fin_en: ", date_fin_en)

           
            type_paiement_eleve.montant = montant
            type_paiement_eleve.libelle = libelle
            type_paiement_eleve.entree_sortie_caisee = entree_sortie_caisee
            if save_etab == True:
                type_paiement_eleve.id_etab = id_etab_to_save
            if save_sousetab == True:
                type_paiement_eleve.sousetab = sousetab_to_save
                type_paiement_eleve.id_sousetab = id_sousetab_to_save
            if save_cycle == True:
                type_paiement_eleve.id_cycle = id_cycle_to_save
            if save_niveau == True:
                type_paiement_eleve.niveau = niveau_to_save
                type_paiement_eleve.id_niveau = id_niveau_to_save
                

            type_paiement_eleve.save()
            print("*type_paiement_eleve ", type_paiement_eleve)
            return redirect('mainapp:liste_types_paiements_eleve')

def creation_eleve(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-eleve.html',{'form':EleveForm})
    elif request.method == 'POST':
        sousetabs = []
        niveaux = []
        classes = []
        specialites = []
        choix =""
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            print("Les donnees: ", donnees)
            # donnees = position + "²²~~" + id_etab + "²²~~" + etab;
            position = donnees[0]
            param2 = int(donnees[1])
            param3 = donnees[2]
            print("PYTHON: ",position,param2, param3)
            # cycles = _load_specialites_ajax(donnees_recherche,trier_par)

            # L'etab a changé on cherche les sousetabs associés
            if position == "1" or position == "1*":
                param2 = 1
                choix = "etab" if position == "1" else "etab2"
                # sousetabs = SousEtab.objects.values_list('id','nom_sousetab').filter(id_etab = param2)
                sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(id_etab = param2)
                id_sousetab0 = sousetabs[0]['id']
                cycles = Cycle.objects.values('id', 'nom_cycle').filter(id_sousetab = id_sousetab0)
                id_cycle0 = cycles[0]['id']
                niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_sousetab = id_cycle0)
                id_niveau0 = niveaux[0]['id']
                specialites = Specialite.objects.values('id_niveau', 'specialite').filter(archived = "0", id_niveau = id_niveau0)            
                classes = Classe.objects.values('id', 'nom_classe','code').filter(archived = "0",id_niveau = id_niveau0)
                # print("VALUES_LIST", sousetabs[0][1])
                # print("VALUES", sousetabs2[0]['nom_sousetab'])
            # Le sousetab a changé on cherche les niveaux et spécialités associés
            if position == "2" or position == "2*":
                choix = "sousetab" if position == "2" else "sousetab2"
                niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_sousetab = param2)
                id_niveau0 = niveaux[0]['id']
                specialites = Specialite.objects.values('id_niveau', 'specialite').filter(archived = "0", id_niveau = id_niveau0)            
                classes = Classe.objects.values('id', 'nom_classe','code').filter(archived = "0", id_niveau = id_niveau0, specialite= "")
                # specialites = Specialite.objects.values('specialite').filter(archived = "0", id_sousetab = param2).order_by('specialite').distinct()
                print("LES SPECS:", specialites.count())
            # Le niveau a changé
            if position == "3" or position == "3*":
                print("PARAM2: ",param2)
                choix = "niveau" if position == "3" else "niveau2"
                nb_niv_spe = Specialite.objects.values('id_niveau', 'specialite').filter(archived = "0", id_niveau = param2).count()                        
                specialites = Specialite.objects.values('id_niveau', 'specialite').filter(archived = "0", id_niveau = param2)                        
                # if nb_niv_spe > 0:
                #     spe = specialites[0]['specialite']
                #     print("SPEEE: ", spe)
                #     classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = spe)
                # else:
                classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite= "" )
                [print(cl) for cl in classes]
            # La spécialité a changé
            if position == "4" or position == "4*":
                choix = "specialite" if position == "4" else "specialite2"
                # id_niv = Specialite.objects.values('id').filter(archived = "0", id_niveau = param2).count()
                print("PARAM2: ",param2, "PARAM3:",param3)
                if param3 == "Aucune":
                    print("DANS AUCUNE")
                    classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = "")
                else:
                    classes = Classe.objects.values('id', 'nom_classe', 'code').filter(archived = "0", id_niveau = param2, specialite__iexact = param3)
                print("# classes: ", classes.count())
            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            print("LE CHOIX ...",choix)
            data = {
                "choix":choix,
                "sousetabs": sousetabs,
                "niveaux": niveaux,
                "classes": classes,
                "specialites": specialites,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
        else:
            form = EleveForm(request.POST)
            # Pr savoir si c'est a cursus de choisir la classe ou pas
            choix_classe = request.POST.get('choix_classe', 0)
            classe_selected =""
            classe = ""
            id_classe = ""
            # L'utilisateur à deja choisi une classe
            if choix_classe == 0:
                classe_selected = request.POST['classe_selected']
                print(classe_selected)
                # classe, id_classe, etoile = classe_selected.split('_')
                classe, id_classe = classe_selected.split('_')
                id_classe = int(id_classe)
                # print("classe selected radio: ",classe, id_classe)
            else:
                print("choix classe checkbox: ",choix_classe)


            # classe_selected = request.POST['classe_selected']
            # print("Selected class: ", classe_selected)
            print(form.errors)
            if form.is_valid():            
                # matricule = form.cleaned_data['matricule']
                matlast = Eleve.objects.filter().order_by('-id').values_list('matricule')[0]
                # matlast = "HT19A032"
                sousEtab = SousEtab.objects.filter()[0]

                matformat = sousEtab.format_matricule
                mat_fixedindex = int(sousEtab.mat_fixedindex)
                mat_yearindex = int(sousEtab.mat_yearindex)
                mat_varyindex = int(sousEtab.mat_varyindex)
                first_matricule = sousEtab.first_matricule

                position = [x for x in range(mat_varyindex)]
                
                matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast[0]))
                # matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))

                # exists_mat_nb = Etudiant.objects.filter(matricule=matlast[0]).count()
                exists_mat_nb = Eleve.objects.filter(matricule__icontains=matricule).count()
                
                while exists_mat_nb > 0:
                    matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matricule))
                    exists_mat_nb = Eleve.objects.filter(matricule__icontains=matricule).count()
                    print("On Boucle ...")

                # print("Exists Mat: ", exists_mat)
                print("NEW MAT: ", matricule)
                nom = form.cleaned_data['nom']
                prenom = form.cleaned_data['prenom']
                sexe = request.POST['sexe']
                date_naissance = request.POST['date_naissance']
                lieu_naissance = form.cleaned_data['lieu_naissance']
                date_entree = form.cleaned_data['date_entree']
                nom_pere = form.cleaned_data['nom_pere']
                prenom_pere = form.cleaned_data['prenom_pere']
                nom_mere = form.cleaned_data['nom_mere']
                prenom_mere = form.cleaned_data['prenom_mere']
                tel_pere = form.cleaned_data['tel_pere']
                tel_mere = form.cleaned_data['tel_mere']
                email_pere = form.cleaned_data['email_pere']
                email_mere = form.cleaned_data['email_mere']
                redouble = request.POST['redouble']

                etab, id_etab = request.POST['choix_etab'].split('_')
                sousetab, id_sousetab = request.POST['choix_sousetab'].split('_')
                # niveau, id_niveau = request.POST['choix_niveau'].split('_')
                specialite, id_niveau = request.POST['specialite'].split('_')
                id_etab = int(id_etab)
                id_sousetab = int(id_sousetab)
                id_niveau = int(id_niveau)
                # id_spe = int(id_spe)
                # print("ID_NIV et ID_SPE", id_niveau)
                print("sexe: ", nom,"date naiss: ", date_naissance)

                photo_webcam = request.POST.get("webcam_photo", False)
                photo = request.FILES.get('photo', "/photos/profil.jpg")

                eleve = Eleve(
                matricule = matricule, 
                nom = nom,
                prenom = prenom,
                sexe = sexe,
                redouble = redouble,
                date_naissance = date_naissance,
                lieu_naissance = lieu_naissance,
                date_entree =  date_entree,
                nom_pere = nom_pere,
                prenom_pere = prenom_pere, 
                nom_mere = nom_mere,
                prenom_mere = prenom_mere,
                tel_pere = tel_pere,
                tel_mere = tel_mere,
                email_pere = email_pere,
                email_mere = email_mere,
                annee_scolaire = "2019-2020"
                )
                eleve.save()


                if (photo_webcam != ""):
                    forma, imgstr = photo_webcam.split(';base64,')
                    print("format", forma)
                    ext = forma.split('/')[-1]

                    photo_raw = b64decode(imgstr)
                    photo_content = ContentFile(photo_raw)
                    photo = photo_content

                    file_name = "myphoto." + ext
                    eleve.photo.save(file_name, photo_content, save=True) # image is User's model field
                else:
                    eleve.photo = photo
                eleve.save()


                eleve.photo_url = eleve.photo.url
                ext = eleve.photo.name.split(".")
                ext = ext[len(ext)-1]

                eleve.photo.name = photo_repertoire + str(eleve.matricule)+ '_' + nom + '_' + prenom + '.' + ext
                eleve.save()
                ANNEE_SCOLAIRE = "2019-2020"
                # print("PreAjout de ",eleve.matricule, eleve.nom ," en ", classe)
                # Checkbox non cliqué c'est a cursus de choisir
                if choix_classe != 0:
                    liste_classes = Specialite.objects.values("liste_classes").filter(specialite__iexact = specialite, id_niveau = id_niveau)[0]['liste_classes']
                    print("liste classes ", liste_classes)
                    # [0:][::2] recupere les elts pairs de la liste pr les impair ciest [1:][::2]
                    liste_ids = liste_classes.split('_')
                    liste_ids = liste_ids[0:][::2]
                    nbre_ = len(liste_ids) - 1
                    liste_ids.pop(nbre_)
                    print(liste_ids)
                    best_classe_id = 0
                    nbre_eleve_classe = 0

                    for id in liste_ids:
                        cl = Classe.objects.filter(pk=int(id),annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                    .eleves
                        if best_classe_id == 0:
                            best_classe_id = int(id)
                            nbre_eleve_classe = cl.count()
                            print("deb nbre el cl et id", nbre_eleve_classe, best_classe_id)
                        elif cl.count() < nbre_eleve_classe:
                             best_classe_id = int(id)
                             nbre_eleve_classe = cl.count()
                             print("nbre el cl et id", nbre_eleve_classe, best_classe_id)

                    Classe.objects.filter(pk=best_classe_id,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                    .eleves.add(eleve)
                    print("Eleve créé en classe_id: ",best_classe_id )


                    # classes, id_classe = [],[]
                    # for c in 
                    # classe, id_classe = liste_classes.split('_')
                else:
                    print("hello")
                    print("Ajout de ",eleve.matricule, eleve.nom ," en ", classe)
                    Classe.objects.filter(pk=id_classe,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                    .eleves.add(eleve)


            return redirect('mainapp:liste_eleves')

def creation_etablissement(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-etablissement.html',{'form':EtablissementForm})
    elif request.method == 'POST':
        form = EtablissementForm(request.POST)
        if form.is_valid():

            nom_etab = form.cleaned_data['nom_etab']
            date_creation = form.cleaned_data['date_creation']
            nom_fondateur = form.cleaned_data['nom_fondateur']
            localisation = form.cleaned_data['localisation']
            bp = form.cleaned_data['bp']
            email = form.cleaned_data['email']
            tel = form.cleaned_data['tel']
            devise = form.cleaned_data['devise']
            langue = form.cleaned_data['langue']
            annee_scolaire = form.cleaned_data['annee_scolaire']
            site_web = form.cleaned_data['site_web']

            etab = Etab()
            etab.nom_etab = nom_etab
            etab.date_creation = date_creation
            etab.nom_fondateur = nom_fondateur
            etab.localisation = localisation
            etab.bp = bp
            etab.email = email
            etab.tel = tel
            etab.devise = devise
            etab.langue = langue
            etab.annee_scolaire = annee_scolaire
            etab.site_web = site_web

            etab.save()

        return redirect('mainapp:liste_etablissements')

def creation_cycle(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-cycle.html',{'form':CycleForm})
    elif request.method == 'POST':
        form = CycleForm(request.POST)
        if form.is_valid():
            nom_etab = form.cleaned_data['nom_etab']
            nom_sousetab = form.cleaned_data['nom_sousetab']
            nom_cycle = form.cleaned_data['nom_cycle']
            print(nom_etab," ",nom_sousetab," ",nom_cycle)

            cycle = Cycle()
            cycle.nom_cycle = nom_cycle
            cycle.nom_etab = nom_etab
            cycle.nom_sousetab = nom_sousetab
            cycle.save()

        return redirect('mainapp:liste_cycles')

def creation_boursier(request):

    if request.method == 'POST':
        form = BoursierForm(request.POST)
        if form.is_valid():
            nom_etab = form.cleaned_data['nom_etab']
            nom_sousetab = form.cleaned_data['nom_sousetab']
            nom_cycle = form.cleaned_data['nom_cycle']
            print(nom_etab," ",nom_sousetab," ",nom_cycle)

            cycle = Cycle()
            cycle.nom_cycle = nom_cycle
            cycle.nom_etab = nom_etab
            cycle.nom_sousetab = nom_sousetab
            cycle.save()

        return redirect('mainapp:liste_boursiers')

def creation_niveau(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-niveau.html',{'form':NiveauForm})
    elif request.method == 'POST':
        form = NiveauForm(request.POST)
        if form.is_valid():
            nom_etab = form.cleaned_data['nom_etab']
            nom_sousetab = form.cleaned_data['nom_sousetab']
            nom_cycle = form.cleaned_data['nom_cycle']
            nom_niveau = form.cleaned_data['nom_niveau']
            print(nom_etab," ",nom_sousetab," ",nom_cycle, " ", nom_niveau)

            niveau = Niveau()
            niveau.nom_niveau = nom_niveau
            niveau.nom_cycle = nom_cycle
            niveau.nom_etab = nom_etab
            niveau.nom_sousetab = nom_sousetab
            niveau.save()

        return redirect('mainapp:liste_niveaux')

def creation_classe(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-classe.html',{'form':ClasseForm})
    elif request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            nom_etab = form.cleaned_data['nom_etab']
            nom_sousetab = form.cleaned_data['nom_sousetab']
            nom_cycle = form.cleaned_data['nom_cycle']
            nom_niveau = form.cleaned_data['nom_niveau']
            nom_classe = form.cleaned_data['nom_classe']
            specialite = request.POST['choix_specialite'].strip()
            print(nom_etab," ",nom_sousetab," ",nom_cycle, " ", nom_niveau, " ", nom_classe," ",specialite)
            print("ICI")
            # On s'assure que la classe n'existe pas déjà
            # __iexact pertmet la comparaison en ignorant la casse
            if Classe.objects.filter(nom_sousetab__iexact = nom_sousetab, nom_classe__iexact = nom_classe, nom_niveau__iexact = nom_niveau).count()== 0:
                print("Nouvelle classe")
                classe = Classe()
                classe.nom_classe = nom_classe
                classe.nom_niveau = nom_niveau
                classe.nom_cycle = nom_cycle
                classe.nom_etab = nom_etab
                classe.nom_sousetab = nom_sousetab
                classe.save()
                id = Classe.objects.values('id').filter(Q( nom_classe__iexact = nom_classe))[0]['id']

                # La classe a été créée avec une spécialité
                if specialite != "":
                    classe.specialite = specialite
                    id_sousetab = SousEtab.objects.values('id').filter(nom_sousetab__iexact = nom_sousetab)[0]['id']
                    nbre_specialites = Specialite.objects.filter(specialite__iexact = specialite, id_sousetab = id_sousetab).count()
                    print(nbre_specialites)
                    id_niveau = Niveau.objects.values('id').filter(nom_niveau__iexact = nom_niveau)[0]['id']
                    nbre_spe_niv = Specialite.objects.filter(specialite__iexact = specialite, id_sousetab = id_sousetab, id_niveau = id_niveau).count()
                    liste_classes = str(id)+"_"+nom_classe+"_"
                    liste_classes_afficher = nom_classe+", "
                    #  C'est une nouvelle spécialité à enrégistrer
                    if nbre_spe_niv > 0:
                        sp = Specialite.objects.filter(specialite__iexact = specialite, id_sousetab = id_sousetab, id_niveau = id_niveau)[0]
                        sp.liste_classes += liste_classes
                        sp.liste_classes_afficher += liste_classes_afficher
                        sp.save()
                        print("OLD", liste_classes," ", liste_classes_afficher)
                    elif nbre_specialites == 0:
                        id_etab = Etab.objects.values('id').filter(nom_etab__iexact = nom_etab)[0]['id']

                        sp = Specialite()
                        sp.nom_etab = nom_etab
                        sp.id_etab = id_etab
                        sp.nom_sousetab = nom_sousetab
                        sp.id_sousetab = id_sousetab
                        sp.nom_niveau = nom_niveau
                        sp.id_niveau = id_niveau
                        sp.specialite = specialite
                        sp.liste_classes += liste_classes
                        sp.liste_classes_afficher = liste_classes_afficher
                        print("NEW", liste_classes)
                        print("NEW", liste_classes_afficher)
                        sp.save()
                classe.save()


        return redirect('mainapp:liste_classes')

def creation_specialite(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-specialite.html',{'form':SpecialiteForm})
    elif request.method == 'POST':
        choix_etab = request.POST["choix_etab"]
        choix_sousetab = request.POST["choix_sousetab"]
        specialite = request.POST["specialite"]
        specialite = specialite.strip()

        if specialite != "":

            specialites = Specialite.objects.values_list('specialite').filter(archived = "0")
            specialites = [spe[0].lower() for spe in specialites]
            
            print(" LA SPECIALITE ", specialite)
            print(" etab ", choix_etab)
            nom_etab = choix_etab.split('_')[0].strip()
            id_etab = int(choix_etab.split('_')[1])
            if choix_sousetab.lower() == "all":
                sousetabs = SousEtab.objects.values('id','nom_sousetab','id_etab').all()            
                for se in sousetabs:
                    nom_sousetab = se['nom_sousetab']
                    nbre = Specialite.objects.values('id').filter(Q(specialite__iexact=specialite),Q(nom_sousetab__iexact=nom_sousetab)).count()
                    if nbre == 0:
                        spe = Specialite()
                        spe.id_sousetab = se['id']
                        spe.id_etab = se['id_etab']
                        spe.specialite = specialite
                        spe.nom_etab = nom_etab
                        spe.nom_sousetab = nom_sousetab
                        spe.save()
            else:
                nom_sousetab = choix_sousetab.split('_')[0].strip()
                id_sousetab = int(choix_sousetab.split('_')[1])
                print("NomSousEtab", nom_sousetab)
                # sousetab = SousEtab.objects.values('id','id_etab','nom_sousetab').filter( )[0]
                # print(" en BD",sousetab.nom_sousetab)
                # id_sousetab, id_etab = sousetabs['id'], sousetabs['id_etab']
                # id_sousetab = int(choix_sousetab.split('_')[1])
                # [print(spe[0].lower()) for spe in specialites]
                nbre = Specialite.objects.values('id').filter(Q(specialite__iexact=specialite),Q(nom_sousetab__iexact=nom_sousetab)).count()
                if nbre == 0:
                    print("il y est pas encore")
                    spe = Specialite()
                    spe.id_sousetab = id_sousetab
                    spe.id_etab = id_etab
                    spe.specialite = specialite
                    spe.nom_etab = nom_etab
                    spe.nom_sousetab = nom_sousetab
                    spe.save()

        return redirect('mainapp:liste_specialites')

def creation_cours(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-cours.html',{'form':CoursForm})
    elif request.method == 'POST':
        form = CoursForm(request.POST)
        print("++++++",form.is_valid())
        if form.is_valid():
            #nom_etab = request.POST.get("nom_etab")
            
            nom_matiere = form.cleaned_data['nom_matiere'].split('²²~~')[1]
            id_matiere = int(form.cleaned_data['nom_matiere'].split('²²~~')[0])
            
            id_classe = int(form.cleaned_data['nom_classe'].split('²²~~')[0])
            nom_classe = form.cleaned_data['nom_classe'].split('²²~~')[1]

            nom_cycle = form.cleaned_data['nom_cycle'].split('²²~~')[1]
            id_cycle = int(form.cleaned_data['nom_cycle'].split('²²~~')[0])

            id_sousetab = int(form.cleaned_data['nom_sousetab'].split('²²~~')[0])
            nom_sousetab = form.cleaned_data['nom_sousetab'].split('²²~~')[1]

            id_etab = int(form.cleaned_data['nom_etab'].split('²²~~')[0])
            nom_etab = form.cleaned_data['nom_etab'].split('²²~~')[1]
            
            code_matiere = form.cleaned_data['code_matiere']
            coef = float(form.cleaned_data['coef'])
            volume_horaire_hebdo = form.cleaned_data['volume_horaire_hebdo']
            volume_horaire_annuel = form.cleaned_data['volume_horaire_annuel']

            # print(nom_etab," ",nom_sousetab," ",nom_cycle, " ", nom_niveau, " ", nom_classe)

            cours = Cours()
            cours.nom_classe = nom_classe
            cours.id_classe = id_classe
            cours.nom_matiere = nom_matiere
            cours.id_matiere = id_matiere
            cours.code_matiere = code_matiere
            cours.nom_cycle = nom_cycle
            cours.id_cycle = id_cycle
            cours.volume_horaire_hebdo = volume_horaire_hebdo
            cours.volume_horaire_annuel = volume_horaire_annuel
            cours.nom_etab = nom_etab
            cours.id_etab = id_etab
            cours.nom_sousetab = nom_sousetab
            cours.id_sousetab = id_sousetab
            cours.coef = coef
            cours.save()

        return redirect('mainapp:liste_cours')

def creation_matiere(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-matiere.html',{'form':MatiereForm})
    elif request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            nom_matiere = form.cleaned_data['nom_matiere']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            print(nom_matiere," ",code," ",nom_sousetab)

            matiere = Matiere()
            matiere.nom_matiere = nom_matiere
            matiere.code = code
            matiere.nom_sousetab = nom_sousetab
            matiere.save()

        return redirect('mainapp:liste_matieres')

def creation_appellation_apprenant_formateur(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-appellation-apprenant-formateur.html',{'form':AppellationApprenantFormateurForm})
    elif request.method == 'POST':
        form = AppellationApprenantFormateurForm(request.POST)
        if form.is_valid():
            formateur = form.cleaned_data['formateur']
            apprenant = form.cleaned_data['apprenant']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            # print(nom_matiere," ",code," ",nom_sousetab)

            app = AppellationApprenantFormateur()
            app.appellation_apprenant = apprenant
            app.appellation_formateur = formateur
            app.nom_sousetab = nom_sousetab
            app.save()

        return redirect('mainapp:liste_appellation_apprenant_formateur')

def creation_type_apprenant(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-apprenant.html',{'form':TypeApprenantForm})
    elif request.method == 'POST':
        form = TypeApprenantForm(request.POST)
        if form.is_valid():
            nom_type_apprenant = form.cleaned_data['nom_type_apprenant']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            type_apprenant = TypeApprenant()
            type_apprenant.nom_type_apprenant = nom_type_apprenant
            type_apprenant.nom_sousetab = nom_sousetab
            type_apprenant.save()

        return redirect('mainapp:liste_type_apprenants')

def creation_sous_etablissement(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-sous-etablissement.html',{'form':SousEtablissementForm})
    elif request.method == 'POST':
        form = SousEtablissementForm(request.POST)
        if form.is_valid():

            nom_sousetab = form.cleaned_data['nom_sousetab']
            date_creation = form.cleaned_data['date_creation']
            nom_fondateur = form.cleaned_data['nom_fondateur']
            localisation = form.cleaned_data['localisation']
            # bp = form.cleaned_data['bp']
            # email = form.cleaned_data['email']
            # tel = form.cleaned_data['tel']
            # devise = form.cleaned_data['devise']
            # langue = form.cleaned_data['langue']
            # annee_scolaire = form.cleaned_data['annee_scolaire']
            # site_web = form.cleaned_data['site_web']

            sousEtab = SousEtab()
            sousEtab.nom_sousetab = nom_sousetab
            sousEtab.date_creation = date_creation
            sousEtab.nom_fondateur = nom_fondateur
            sousEtab.localisation = localisation
            # etab.bp = bp
            # etab.email = email
            # etab.tel = tel
            # etab.devise = devise
            # etab.langue = langue
            # etab.annee_scolaire = annee_scolaire
            # etab.site_web = site_web

            sousEtab.save()

        return redirect('mainapp:liste_sous_etablissements')

def creation_discipline(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-discipline.html',{'form':DisciplineForm})
    elif request.method == 'POST':
        form = DisciplineForm(request.POST)
        if form.is_valid():
            fait = form.cleaned_data['fait']
            description = form.cleaned_data['description']
            nb_heures_min = form.cleaned_data['nb_heures_min']
            nb_heures_max = form.cleaned_data['nb_heures_max']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            print(nb_heures_min," ",fait," ",nom_sousetab)

            discipline = Discipline()
            discipline.fait = fait
            discipline.description = description
            discipline.nb_heures_min = nb_heures_min
            discipline.nb_heures_max = nb_heures_max
            discipline.nom_sousetab = nom_sousetab
            discipline.save()

        return redirect('mainapp:liste_disciplines')

def creation_condition_renvoi(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-condition-renvoi.html',{'form':ConditionRenvoiForm})
    elif request.method == 'POST':
        form = ConditionRenvoiForm(request.POST)
        if form.is_valid():
            nb_heures_max = form.cleaned_data['nb_heures_max']
            age = form.cleaned_data['age']
            moyenne = form.cleaned_data['moyenne']
            nb_jours = form.cleaned_data['nb_jours']
            nom_niveau = form.cleaned_data['nom_niveau']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            print(nb_heures_max," ",age," ",moyenne)

            c_renvoi = ConditionRenvoi()
            c_renvoi.nb_heures_max = nb_heures_max
            c_renvoi.age = age
            c_renvoi.moyenne = moyenne
            c_renvoi.nb_jours = nb_jours
            c_renvoi.nom_niveau = nom_niveau
            c_renvoi.nom_sousetab = nom_sousetab
            c_renvoi.save()

        return redirect('mainapp:liste_condition_renvois')

def creation_condition_succes(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-condition-succes.html',{'form':ConditionSuccesForm})
    elif request.method == 'POST':
        form = ConditionSuccesForm(request.POST)
        if form.is_valid():
            moyenne = form.cleaned_data['moyenne']
            nom_niveau = form.cleaned_data['nom_niveau']
            nom_sousetab = form.cleaned_data['nom_sousetab']

            print(moyenne," ",nom_niveau," ",nom_sousetab)

            c_succes = ConditionSucces()
            c_succes.moyenne = moyenne
            c_succes.nom_niveau = nom_niveau
            c_succes.nom_sousetab = nom_sousetab
            c_succes.save()

        return redirect('mainapp:liste_condition_succes')

def creation_type_paiement_pers_enseignant(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-enseignant.html',{'form':TypePayementPersAdministratifForm})
    elif request.method == 'POST':
        form = TypePayementPersAdministratifForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            type_payement = form.cleaned_data['type_payement']
            person = form.cleaned_data['person']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            print(person," ",libelle," ",montant)

            type_paiement = TypePayementAdminStaff()
            type_paiement.libelle = libelle
            type_paiement.type_payement = type_payement
            type_paiement.person = person
            type_paiement.entree_sortie_caisee = entree_sortie_caisee
            type_paiement.montant = montant
            type_paiement.save()

        return redirect('mainapp:liste_types_paiements_pers_enseignant')

def creation_type_paiement_pers_appui(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-appui.html',{'form':TypePayementPersAdministratifForm})
    elif request.method == 'POST':
        form = TypePayementPersAdministratifForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            type_payement = form.cleaned_data['type_payement']
            person = form.cleaned_data['person']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            print(person," ",libelle," ",montant)

            type_paiement = TypePayementAdminStaff()
            type_paiement.libelle = libelle
            type_paiement.type_payement = type_payement
            type_paiement.person = person
            type_paiement.entree_sortie_caisee = entree_sortie_caisee
            type_paiement.montant = montant
            type_paiement.save()

        return redirect('mainapp:liste_types_paiements_pers_appui')

def creation_type_paiement_divers(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-divers.html',{'form':TypePayementDiversForm})
    elif request.method == 'POST':
        form = TypePayementDiversForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            date_deb = form.cleaned_data['date_deb']
            date_fin = form.cleaned_data['date_fin']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            print(date_fin," ",libelle," ",montant)

            tpd = TypePayementDivers()
            tpd.libelle = libelle
            tpd.date_deb = date_deb
            tpd.date_fin = date_fin
            tpd.type_payement = "Divers"
            tpd.entree_sortie_caisee = entree_sortie_caisee
            tpd.montant = montant
            tpd.save()

        return redirect('mainapp:liste_types_paiements_divers')

def creation_type_paiement_cantine(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-cantine.html',{'form':TypePayementDiversForm})
    elif request.method == 'POST':
        form = TypePayementDiversForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            date_deb = form.cleaned_data['date_deb']
            date_fin = form.cleaned_data['date_fin']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            tpd = TypePayementDivers()
            tpd.libelle = libelle
            tpd.date_deb = date_deb
            tpd.date_fin = date_fin
            tpd.type_payement = "Cantine"
            tpd.entree_sortie_caisee = entree_sortie_caisee
            tpd.montant = montant
            tpd.save()

        return redirect('mainapp:liste_types_paiements_cantine')

def creation_type_paiement_transport(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-transport.html',{'form':TypePayementDiversForm})
    elif request.method == 'POST':
        form = TypePayementDiversForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            date_deb = form.cleaned_data['date_deb']
            date_fin = form.cleaned_data['date_fin']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            tpd = TypePayementDivers()
            tpd.libelle = libelle
            tpd.date_deb = date_deb
            tpd.date_fin = date_fin
            tpd.type_payement = "Transport"
            tpd.entree_sortie_caisee = entree_sortie_caisee
            tpd.montant = montant
            tpd.save()

        return redirect('mainapp:liste_types_paiements_transport')

def creation_type_paiement_dortoir(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-dortoir.html',{'form':TypePayementDiversForm})
    elif request.method == 'POST':
        form = TypePayementDiversForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            date_deb = form.cleaned_data['date_deb']
            date_fin = form.cleaned_data['date_fin']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            tpd = TypePayementDivers()
            tpd.libelle = libelle
            tpd.date_deb = date_deb
            tpd.date_fin = date_fin
            tpd.type_payement = "Dortoir"
            tpd.entree_sortie_caisee = entree_sortie_caisee
            tpd.montant = montant
            tpd.save()

        return redirect('mainapp:liste_types_paiements_dortoir')

def creation_type_paiement_facture(request):
    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-facture.html',{'form':TypePayementDiversForm})
    elif request.method == 'POST':
        form = TypePayementDiversForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            date_deb = form.cleaned_data['date_deb']
            date_fin = form.cleaned_data['date_fin']
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
            montant = float(form.cleaned_data['montant'])

            tpd = TypePayementDivers()
            tpd.libelle = libelle
            tpd.date_deb = date_deb
            tpd.date_fin = date_fin
            tpd.type_payement = "Facture"
            tpd.entree_sortie_caisee = entree_sortie_caisee
            tpd.montant = montant
            tpd.save()

        return redirect('mainapp:liste_types_paiements_facture')

def creation_type_paiement_pers_administratif(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-type-paiement-pers-administratif.html',{'form':TypePayementPersAdministratifForm})
    elif request.method == 'POST':
        form = TypePayementPersAdministratifForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            type_payement = form.cleaned_data['type_payement']
            person = form.cleaned_data['person']
            montant = float(form.cleaned_data['montant'])
            entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']

            print(person," ",libelle)

            tpas = TypePayementAdminStaff()
            tpas.libelle = libelle
            tpas.type_payement = type_payement
            tpas.person = person
            tpas.type_payement = "Pers Administratif"
            tpas.montant = montant
            tpas.entree_sortie_caisee = entree_sortie_caisee
            tpas.save()

        return redirect('mainapp:liste_types_paiements_pers_administratif')

def creation_profil(request):


    if request.method == 'POST':
        form = ProfilForm(request.POST)
        #print(form)
        #if form.is_valid():

        pseudo = request.POST.get('pseudo', False)
        nom = request.POST.get('nom', False)
        prenom = request.POST.get('prenom', False)
        telephone = request.POST.get('telephone', False)
        ville = request.POST.get('ville', False)
        quartier = request.POST.get('quartier', False)
        
        photo_webcam = request.POST.get("webcam_photo", False)


        photo = request.FILES.get('photo', "/photos/profil.jpg")


        groupes = request.POST.getlist('ajout_groupe_liste_profil')
        print("mes groupes")
        print(groupes)
        print("fin groupes")

        print("ville et quartier")
        print(ville)
        print(quartier)
        print("fin ville et quartier")

        print("telephone")
        print(telephone)
        print("fin telephone")

        print("photo_webcam")
        print(photo_webcam)
        print("fin photo_webcam")

        # Nous créons un nouvel utilisateur
        user = User.objects.create_user(
        username = pseudo,
        last_name = nom,
        first_name = prenom,
        )

        # Nous créons un nouveau profil utilisateur en associant avec l'utilisateur deja créé
        profil = Profil(
        user = user, 
        telephone = telephone,
        ville = ville,
        quartier = quartier,
        #photo = photo,
        )
        profil.save()

        if (photo_webcam != ""):
            forma, imgstr = photo_webcam.split(';base64,')
            print("format", forma)
            ext = forma.split('/')[-1]

            photo_raw = b64decode(imgstr)
            photo_content = ContentFile(photo_raw)
            photo = photo_content

            file_name = "myphoto." + ext
            profil.photo.save(file_name, photo_content, save=True) # image is User's model field
        else:
            profil.photo = photo
        profil.save()


        profil.photo_url = profil.photo.url
        ext = profil.photo.name.split(".")
        ext = ext[len(ext)-1]

        name = profil.user.last_name
        name = name.strip()

        name = "_".join(name.split())

        profil.photo.name = photo_repertoire + str(profil.user.id)+ '_' + name + '.' + ext
        profil.save()

        # status = add_user_group(user, "proviseur")
        # status = add_user_group(user, "enseignant")

        for groupe in groupes:
            status = add_user_group(user, groupe)
        #     print(status)

        #   status = del_user_group(user, "proviseur")
        #print(status)

        return redirect('mainapp:liste_profils')
        # else:
        #     return render(request, '400.html')

def periodes_saisie_actives(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):
    id_sousetab_session = request.session.get('id_sousetab', None)
    request.session.modified = True
    passe = False
    id_sousetab_selected = 1
    if request.method == 'POST':
        choix =""
        if(request.is_ajax()):
            choix = "sousetab_recherche"
            sousetabs = []
            id_sousetabs = []
            periode_saisies = []
            nom_evaluation = ""
            passe = True
            donnees = request.POST['form_data'].split('²²~~')
            print(donnees)
            id_sousetab = int(donnees[4])
            
            sousetabs = SousEtab.objects.values('nom_sousetab','id').filter(archived="0").order_by('id')
            id_sousetabs = [s['id'] for s in sousetabs]
            id_sousetab_selected = id_sousetabs[0]
            sousetabs = [s['nom_sousetab'] for s in sousetabs]
            periode_saisies = LesDivisionTempsSousEtab.objects.filter(archived = "0", id_sousetab = id_sousetab, mode = "saisi").order_by('libelle')
            nom_evaluation = SousEtab.objects.values('nom_division_temps_saisisable').filter(id=id_sousetab)[0]['nom_division_temps_saisisable']


            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            # trier_par = donnees[3]
            
            periode_saisies_serializers = LesDivisionTempsSousEtabSerializer(periode_saisies, many=True)

            periode_saisies = periode_saisies_serializers.data
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(periode_saisies)

            #form = EtudiantForm
            paginator = Paginator(periode_saisies, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default

            

            data = {
                "choix": choix,
                "message_resultat":"",
                "sousetabs": sousetabs,
                "id_sousetabs": id_sousetabs,
                "periode_saisies": periode_saisies,
                "nom_evaluation": nom_evaluation,
                "id_sousetab_selected": id_sousetab_selected,
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }


            # data = {
            #     "periode_saisies": periode_saisies,
            #     "message_resultat":"",
            #     "numero_page_active" : int(numero_page_active),
            #     "liste_page" : liste_page,
            #     "possede_page_precedente" : possede_page_precedente,
            #     "page_precedente" : page_precedente,
            #     "possede_page_suivante" : possede_page_suivante,
            #     "page_suivante" : page_suivante,
            #     "nbre_element_par_page" : nbre_element_par_page,
            #     "permissions" : permissions_of_a_user(request.user),
            #     "data_color" : data_color,
            #     "sidebar_class" : sidebar_class,
            #     "theme_class" : theme_class,
            # }
    
            return JSONResponse(data)
        else:
            passe = False
    
    if passe == False:
        sousetabs = SousEtab.objects.filter(archived="0").order_by('id')
        id_sousetab = sousetabs[0].id
        id_sousetab_selected = id_sousetab  
        if id_sousetab_session != None:
            id_sousetab_selected = int(id_sousetab_session)
            id_sousetab = id_sousetab_selected

        periode_saisies = LesDivisionTempsSousEtab.objects.filter(archived = "0", id_sousetab = id_sousetab, mode = "saisi").order_by('libelle')
        nom_evaluation = SousEtab.objects.values('nom_division_temps_saisisable').filter(id=id_sousetab)[0]['nom_division_temps_saisisable']

        paginator = Paginator(periode_saisies, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

        try:
            # La définition de nos URL autorise comme argument « page » uniquement 
            # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
            page_active = paginator.page(page)
        except PageNotAnInteger:
            page_active = paginator.page(1)
        except EmptyPage:
            # Nous vérifions toutefois que nous ne dépassons pas la limite de page
            # Par convention, nous renvoyons la dernière page dans ce cas
            page_active = paginator.page(paginator.num_pages)


        #gerer les preferences utilisateur en terme de theme et couleur
        if (request.user.id != None):
            if(request.user.is_superuser == True):
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            else:          
                #print(request.user.is_superuser)
                prof = Profil.objects.get(user=request.user)
                data_color = prof.data_color
                sidebar_class = prof.sidebar_class
                theme_class = prof.theme_class
        else:
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default

        return render(request, 'mainapp/pages/periodes-saisie-actives.html', locals())

def jours_ouvrables(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):
    
    jours_ouvrables = SousEtab.objects.values('id','nom_sousetab',
        'liste_jours_ouvrables','duree_tranche_horaire','heure_deb_cours',
        'liste_pauses','liste_pauses_afficher').filter().order_by('id')

    sousetabs = SousEtab.objects.values('id', 'nom_sousetab')
    paginator = Paginator(jours_ouvrables, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/jours-ouvrables.html', locals())

def definition_tranches_horaires(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):
    if request.method == 'POST':
        choix ="change_sousetab_def_tranche_horaire"
        if(request.is_ajax()):
            id_sousetabs = []
            nom_sousetabs = []
            duree_tranche_horaire, heure_deb_cours = [], []
            jours, id_jours = [], []
            pauses, id_pauses, durees = [], [], []
            # donnees = request.POST['form_data']
            id_sousetab = int(request.POST['form_data'])
            
            sousetabs = SousEtab.objects.values('id', 'nom_sousetab')
            id_sousetabs = [s['id'] for s in sousetabs]
            nom_sousetabs = [s['nom_sousetab'] for s in sousetabs]

            items = SousEtab.objects.values('duree_tranche_horaire','heure_deb_cours').filter(id = id_sousetab)[0]
            duree_tranche_horaire, heure_deb_cours = items['duree_tranche_horaire'], items['heure_deb_cours']
            jours = Jour.objects.values('libelle','id').filter(id_sousetab = id_sousetab)
            id_jours = [j['id'] for j in jours]
            jours = [j['libelle'] for j in jours]
            pauses = Pause.objects.values('id','libelle','duree').filter(id_sousetab=id_sousetab)
            id_pauses = [j['id'] for j in pauses]
            durees = [j['duree'] for j in pauses]
            pauses = [j['libelle'] for j in pauses]

            
            jrs = Jour.objects.filter(id_sousetab = id_sousetab)
            max_id =0
            liste_th_max = []
            liste = []
            n = 0
            id_jour_max = 0
            les_tranches = ""
            nb_tranches = 0
            passe = False
            for j in jrs:
                n = len(j.tranche_horaires_id)
                if n > max_id:
                    max_id = n
                    id_jour_max = j.id
                    liste_th_max = j.tranche_horaires_id
            if max_id > 0:
                for t in liste_th_max:
                    liste.append(t)
                liste =sorted(liste)
                print(liste)
                for t in liste:
                    item = TrancheHoraire.objects.values('heure_deb','heure_fin').filter(id=t).order_by('numero_tranche')[0]
                    les_tranches += item['heure_deb']+" - "+item['heure_fin']+"²²"
                    passe = True
                    nb_tranches += 1
                if passe == True:
                    n = len(les_tranches)
                    les_tranches = les_tranches[:n- 2]
                    print("**les_tranches: ",les_tranches )
                    print("**n_tranches: ",nb_tranches )

            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            print("** les_tranches ...",les_tranches)
            data = {
                "choix":choix,
                "duree_tranche_horaire":duree_tranche_horaire,
                "heure_deb_cours":heure_deb_cours,
                "id_jours":id_jours,
                "jours":jours,
                "pauses":pauses,
                "id_pauses":id_pauses,
                "les_tranches":les_tranches,
                "nb_tranches":nb_tranches,
                "durees":durees,
                "id_sousetabs":id_sousetabs,
                "nom_sousetabs": nom_sousetabs,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
    id_sousetab = request.session.get('id_sousetab_tranche', None)
    request.session.modified = True

    sousetabs = SousEtab.objects.values('id', 'nom_sousetab')
    if id_sousetab != None:
        id_sousetab = int(id_sousetab)
    else:
        id_sousetab = sousetabs[0]['id']
        # id_sousetab_selected = id_sousetab
   
    jrs = Jour.objects.filter(id_sousetab = id_sousetab)
    max_id =0
    liste_th_max = []
    n = 0
    id_jour_max = 0
    les_tranches = []
    liste = []
    for j in jrs:
        n = len(j.tranche_horaires_id)
        if n > max_id:
            max_id = n
            id_jour_max = j.id
            liste_th_max = j.tranche_horaires_id
    if max_id > 0:
        for t in liste_th_max:
            liste.append(t)
        liste =sorted(liste)
        print(liste)
        for t in liste:
            item = TrancheHoraire.objects.values('heure_deb','heure_fin').filter(id=t).order_by('numero_tranche')[0]
            les_tranches.append(item['heure_deb']+" - "+item['heure_fin'])
    print(les_tranches)

    
    pauses = Pause.objects.values('id','libelle','duree').filter(id_sousetab=id_sousetab)
    items = SousEtab.objects.values('duree_tranche_horaire','heure_deb_cours').filter(id = id_sousetab)[0]
    duree_tranche_horaire, heure_deb_cours = items['duree_tranche_horaire'], items['heure_deb_cours']
    jours = Jour.objects.values('libelle','id').filter(id_sousetab = id_sousetab)
    nb_jours = range(jours.count())

    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/definition-tranches-horaires.html', locals())

def liste_etudiants(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    data =[]

    etabs = Etab.objects.all()
    for e in etabs:
        for s in e.sous_etabs_id:
            se = SousEtab.objects.filter(pk=s)
            for p in se:
                for c in p.cycles_id:
                    cy = Cycle.objects.filter(pk=c)
                    cycle = dict(
                            nom_etab = e.nom_etab,
                            nom_sousetab = p.nom_sousetab,
                            nom_cycle = cy[0].nom_cycle,
                            cycle_id = cy[0].id
                    )
                    data.append(cycle)
    for d in data:
        print(d['nom_etab'],"_",d['nom_sousetab'],"_",d['nom_cycle'],"_",d['cycle_id'])
    recherche ="etoilek"

    infos = []
    # s.lower()
    for dictn in data:
        if recherche in dictn['nom_etab'] or recherche in dictn['nom_sousetab'] or recherche in dictn['nom_cycle']:
            infos.append(dictn)

    [print(info) for info in infos]
                    # print(e.nom_etab," "," ",e.nom_fondateur," ",p," ",cy[0])
                    # for niv in cy[0].niveaux_id:
                    #     nivs = Niveau.objects.filter(pk=niv)
                    #     for n in nivs:
                    #         for clss_id in n.classes_id:
                    #             clss = Classe.objects.filter(pk=clss_id)
                    #             print(n," ",clss[0])



    etudiants = Etudiant.objects.filter(archived="0").order_by('-id')

    
    form = EtudiantForm  
    paginator = Paginator(etudiants, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-etudiants.html', locals())

def liste_eleves(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    # On enlevera ~Q(~id=1) à la prochaine migration
    # classe_recherchees = Classe.objects.values('id','nom_classe').filter(~Q(id=1), archived = "0")
    classe_recherchees = Classe.objects.values('id','nom_classe').filter(archived = "0")
    # classe_courante = request.POST.get('classe_courante', None)
    classe_courante = request.session.get('classe_courante', None)

    montant_a_payer = 0
    
    if classe_courante == None:
        id_classe_courante = classe_recherchees[0]['id']
        classe = str(id_classe_courante)+"_"+classe_recherchees[0]['nom_classe']+"_"
    else:
        classe_courante, id_classe_courante = classe_courante.split('_')
        classe = id_classe_courante+"_"+classe_courante+"_"
        id_classe_courante = int(id_classe_courante)
        del request.session['classe_courante']
        request.session.modified = True
    # print("id_classe_courante------ ",id_classe_courante)

    tranches = TypePayementEleve.objects.values('id','libelle','montant','ordre_paiement').filter(liste_classes__icontains = classe, entree_sortie_caisee = "e").order_by('ordre_paiement')
    tranches_paiements = ""
    for t in tranches:
        montant_a_payer += t['montant']
        tranches_paiements += str(t['id'])+"²²"+t['libelle']+"²²"+str(t['montant'])+"²²"+str(t['ordre_paiement'])+"*²*"

    tranches = TypePayementEleve.objects.values('id','libelle','montant').filter(liste_classes__icontains = classe, entree_sortie_caisee = "s").order_by('libelle')
    bourses = ""
    for t in tranches:
        bourses += str(t['id'])+"²²"+t['libelle']+"²²"+str(t['montant'])+"*²*"

    # tranches_paiements = [tranches_paiements+str(t['id'])+"²²"+t['libelle']+"²²"+str(t['montant'])+"²²"+str(t['ordre_paiement']) for t in tranches ]
    # print("montant, tranches_paiements",montant_a_payer, tranches_paiements)
    # tpe = TypePayementEleve()
    # TypePayementEleve.objects.filter()
    #         type_paiement_eleve.liste_classes = liste_classes
    #         type_paiement_eleve.liste_classes_afficher = liste_classes_afficher
    #         type_paiement_eleve.indicateur_liste_classes = indicateur_liste_classes
    
    etabs = Etab.objects.values('id','nom_etab').filter(archived = "0")
    sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0")
    niveaux = []
    classes_init = []
    classes = []
    cycles = []
    specialitess = []
    specialites = Specialite.objects.values('specialite').filter(~Q(nom_niveau=""),archived = "0")
    
    # eleves = Eleve.objects.all().order_by('-id')[:10]
    eleves = Eleve.objects.filter(archived = "0", id_classe_actuelle = id_classe_courante\
            ).order_by('matricule')
    
    print("classe_", id_classe_courante)
    if etabs.count() > 0:
        id_sousetab0 = sousetabs[0]['id']
        # cycles = Cycle.objects.values('id','nom_cycle').filter(archived = "0",id_sousetab = id_sousetab0)
        niveaux = Niveau.objects.values('id','nom_niveau').filter(archived = "0",id_sousetab = id_sousetab0)
        if niveaux.count() > 0:
            # spe_vide = dict(
            #                 id_niveau = 0,
            #                 specialite = "Aucune"
            #         )
            id_niveau0 = niveaux[0]['id']
            # specialitess = Specialite.objects.values('id','specialite').filter(archived = "0").order_by('specialite').distinct()
            specialitess = Specialite.objects.values('id_niveau','specialite').filter(archived = "0", id_niveau= id_niveau0)
            # spec0 = specialitess[0]['specialite']
            # print("spec0 ", spec0, "SPECS: ", specialitess.count()," IDNIV: ", id_niveau0)
            # if specialitess.count() > 0:
            #     classes_init = Classe.objects.values('id','nom_classe','code').filter(archived = "0",specialite__iexact = spec0, id_niveau = id_niveau0)
            #     if Classe.objects.values('id','nom_classe','code').filter(archived = "0",specialite = "", id_niveau = id_niveau0).count() > 0:
            #         # specialitess.append(spe_vide)
            #         # specialitess = dict(specialitess, **spe_vide)
            # else:
            classes_init = Classe.objects.values('id','nom_classe','code').filter(archived = "0", id_niveau = id_niveau0, specialite = "")
                # specialitess.append(spe_vide)
                # specialitess = dict(specialitess, **spe_vide)

    form = EleveForm  
    paginator = Paginator(eleves, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-eleves.html', locals())

def liste_boursiers(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    bourses = Eleve.objects.filter(~Q(liste_bourses = ""),archived = "0").order_by('matricule')
    print("boursiers: ", bourses)
    form = BoursierForm  
    paginator = Paginator(bourses, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-boursiers.html', locals())

def liste_etablissements(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    etablissement = Etab.objects.all().order_by('-id')

    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    form = EtablissementForm  
    paginator = Paginator(etablissement, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-etablissements.html', locals())

def liste_sous_etablissements(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    s_etablissements = SousEtab.objects.all().order_by('-id')

    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')
    
    form = SousEtablissementForm  
    paginator = Paginator(s_etablissements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-sous-etablissements.html', locals())

def liste_cycles(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    cycles = Cycle.objects.filter(archived = "0").order_by('-id')

    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    form = CycleForm  
    paginator = Paginator(cycles, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-cycles.html', locals())

def liste_niveaux(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    niveaux = Niveau.objects.filter(archived = "0").order_by('-id')

    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    form = NiveauForm  
    paginator = Paginator(niveaux, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-niveaux.html', locals())

def liste_classes(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    classesAll = Classe.objects.filter(archived = "0").order_by('nom_classe')
    classes = Classe.objects.filter(archived = "0").order_by('nom_classe')
    specialitess = Specialite.objects.values('specialite').filter(archived = "0").order_by('specialite').distinct()

    # liste_classes = "1_3eAll1_2_3eAll2_3_3eAll3_"
    # liste_afficher = "3eAll1, 3eAll2, 3eAll3, "
    


    form = ClasseForm  
    paginator = Paginator(classesAll, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gestion de la description textuelle de la pagination
    nbre_item = len(classesAll)

    first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

    if(int(page_active.number)-1 != 0):
        last_item_page = first_item_page + len(list(paginator.page_range)) -1
    else:
        last_item_page = int(page_active.number) * nbre_element_par_page


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-classes.html', locals())

def liste_specialites(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    etabs = Etab.objects.values('id','nom_etab').filter(archived = "0",)
    sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0",)
    specialitess = Specialite.objects.values('specialite').filter(archived = "0").order_by('specialite').distinct()

    specialites = Specialite.objects.values('id','specialite','nom_etab','nom_sousetab').filter(archived = "0").order_by('specialite').distinct()
    for s in specialites:
        print(s)
        break

    form = SpecialiteForm  
    paginator = Paginator(specialites, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gestion de la description textuelle de la pagination
    nbre_item = len(specialites)

    first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

    if(int(page_active.number)-1 != 0):
        last_item_page = first_item_page + len(list(paginator.page_range)) -1
    else:
        last_item_page = int(page_active.number) * nbre_element_par_page


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-specialites.html', locals())

def liste_classe_specialites(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):
    
    # tab = "24_TleC_25_TleD_27_TleAll_29_TleEsp_"
    # tab = tab.split("_")
    # nbre_ = len(tab) - 1
    # if nbre_ > 0:
    #     tab.pop(nbre_)
    #     # clss = [tab[item] for item in range(nbre_) if item % 2 == 1]

    #     clss = ""
    #     inds = ""
    #     ind = 0
    #     for cl in tab:
    #         if ind % 2 == 1:
    #             clss += cl+", "
    #         else:
    #             inds += cl+", "
    #         ind += 1
    #     print(clss)
    #     print(inds)
    # classes = Classe.objects.filter(archived = "0").order_by('-specialite')
    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    etabs = Etab.objects.values('id','nom_etab').filter(archived = "0")
    sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0")
    niveaux = []
    classes_init = []
    classes = []
    specialites = Specialite.objects.values('specialite').filter(~Q(nom_niveau=""),archived = "0")
    
    # specialites = [spe[0].lower() for spe in specialites]
    # [print(s) for s in specialites]
    if etabs.count() > 0:
        id_sousetab0 = sousetabs[0]['id']
        niveaux = Niveau.objects.values('id','nom_niveau').filter(archived = "0",id_sousetab = id_sousetab0)
        specialitess = Specialite.objects.values('specialite').filter(archived = "0", id_sousetab = id_sousetab0).order_by('specialite').distinct()
        if niveaux.count() > 0:
            id_niveau0 = niveaux[0]['id']
            classes_init = Classe.objects.values('id','nom_classe','code').filter(archived = "0",id_niveau = id_niveau0)

    classes = Specialite.objects.\
            values('id_niveau','liste_classes_afficher','nom_etab','nom_sousetab','nom_niveau','specialite','liste_classes')\
            .filter(~Q(nom_niveau=""),archived = "0").distinct().order_by('specialite')
    for classe in classes:
        # tab = classe['liste_classes_afficher'].split("_")
        break
    #     print("RRR")
    #     nbre_ = len(tab) - 1
    #     if nbre_ > 0:
    #         tab.pop(nbre_)
    #         # clss = [tab[item] for item in range(nbre_) if item % 2 == 1]

    #         clss = ""
    #         inds = ""
    #         ind = 0
    #         for cl in tab:
    #             if ind % 2 == 1:
    #                 clss += cl+", "
    #             else:
    #                 inds += cl+", "
    #             ind += 1
    #         classe['liste_classes'] = clss
    #         print(classe)

    # [print(classe) for classe in classes]

    # classes = Classe.objects.values('id_niveau','nom_etab','nom_sousetab','nom_cycle','nom_niveau','specialite')\
    #             .filter(archived = "0").distinct().order_by('-specialite')

    form = ClasseSpecialiteForm  
    paginator = Paginator(classes, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gestion de la description textuelle de la pagination
    nbre_item = len(classes)

    first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

    if(int(page_active.number)-1 != 0):
        last_item_page = first_item_page + len(list(paginator.page_range)) -1
    else:
        last_item_page = int(page_active.number) * nbre_element_par_page


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-classe-specialites.html', locals())

def liste_matieres(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    matieres = Matiere.objects.filter(archived = "0").order_by('-id')

    classes = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    form = MatiereForm  
    paginator = Paginator(matieres, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-matieres.html', locals())

def liste_appellation_apprenant_formateur(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    appellations = AppellationApprenantFormateur.objects.filter(archived = "0").order_by('-id')
    print("Nbre appellation ",appellations.count())

    classes = Classe.objects.filter(archived = "0").order_by('-nom_classe')


    form = AppellationApprenantFormateurForm  
    paginator = Paginator(appellations, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/appellation-apprenant-formateur.html', locals())

def liste_type_apprenants(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    type_apprenants = TypeApprenant.objects.filter(archived = "0").order_by('-id')


    form = TypeApprenantForm  
    paginator = Paginator(type_apprenants, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-type-apprenants.html', locals())

def liste_disciplines(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    disciplines = Discipline.objects.filter(archived = "0").order_by('-id')

    classes = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    form = DisciplineForm  
    paginator = Paginator(disciplines, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-disciplines.html', locals())

def liste_types_paiements_eleve(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementEleve.objects.filter(archived = "0").order_by('ordre_paiement')
    etabs = Etab.objects.values('id','nom_etab').filter(archived = "0")
    sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(archived = "0")
    # classe_recherchees = Classe.objects.values('id','nom_classe').filter(archived = "0")
    type_paiements_eleves = TypePayementEleve.objects.values('liste_classes_afficher', 'indicateur_liste_classes', 'liste_classes').filter(archived = "0")
    # c_r: classe_recherchees, c_r_a: classe_recherchees_afficher
    c_r = []
    c_r_a = []
    type_paiements_eleves_afficher, type_paiements_eleves_ = [], []
    passee = False
    for tpe in type_paiements_eleves:
        passee = True
        taille = len(tpe['indicateur_liste_classes'].split("_"))
        # taille == 1 si c'est une classe
        # print("***taille tpe['indicateur_liste_classes']:", taille,tpe['indicateur_liste_classes'])
        if taille == 1:
            # ici on veut fabriquer les pairs du genre: 6eA_1, 6eB_2
            liste_classes = tpe['liste_classes'].split("_")
            # print("* avant liste_classes",liste_classes)
            pair = liste_classes[0:][::2]
            impair = liste_classes[1:][::2]
            # print("#pair",pair)
            # print("#impair",impair)
            liste_classes = []
            i = 0
            for j in impair:
                liste_classes.append(j+"_"+pair[i])
                i += 1
            # print("##liste_classes",liste_classes)
            i = 0
            for c in liste_classes:
                if c not in c_r:
                    c_r_a.append(c.split('_')[0])
                    c_r.append(c)
                i += 1
        elif tpe['indicateur_liste_classes'] not in c_r:
            print("tpe['indicateur_liste_classes']",tpe['indicateur_liste_classes'])
            c_r_a.append(tpe['liste_classes_afficher'] )
            c_r.append(tpe['indicateur_liste_classes'])
    if passee == True:
        zipped_lists = zip(c_r_a, c_r)
        sorted_pairs = sorted(zipped_lists)

        tuples = zip(*sorted_pairs)
        if len(sorted_pairs) == 0:
            type_paiements_eleves_afficher, type_paiements_eleves_ = [], []
        else:
            type_paiements_eleves_afficher, type_paiements_eleves_ = [ list(tuple) for tuple in  tuples]
        # print(type_paiements_eleves_afficher)
        # print(type_paiements_eleves_)

    form = TypePayementEleveForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-eleve.html', locals())

def liste_types_paiements_pers_administratif(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementAdminStaff.objects.filter(archived = "0",type_payement="Pers Administratif").order_by('-id')

    form = TypePayementPersAdministratifForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-pers-administratif.html', locals())

def liste_condition_renvois(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    c_renvois = ConditionRenvoi.objects.filter(archived = "0").order_by('-id')


    form = ConditionRenvoiForm  
    paginator = Paginator(c_renvois, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-condition-renvois.html', locals())

def liste_condition_succes(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    c_success = ConditionSucces.objects.filter(archived = "0").order_by('-id')


    form = ConditionSuccesForm  
    paginator = Paginator(c_success, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-condition-succes.html', locals())

def liste_cours(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = Cours.objects.all().order_by('code_matiere')
    
    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')
    
    form = CoursForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)

      #gestion de la description textuelle de la pagination
    nbre_item = len(cours)

    first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

    if(int(page_active.number)-1 != 0):
        last_item_page = first_item_page + len(list(paginator.page_range)) -1
    else:
        last_item_page = int(page_active.number) * nbre_element_par_page


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-cours.html', locals())

def liste_progressions(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-progressions.html', locals())

def liste_reunions(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-reunions.html', locals())

def liste_types_paiements_pers_enseignant(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):


    paiements = TypePayementAdminStaff.objects.filter(archived = "0",type_payement="Enseignant").order_by('-id')

    form = TypePayementPersAdministratifForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

    return render(request, 'mainapp/pages/liste-types-paiements-pers-enseignant.html', locals())

def liste_types_paiements_pers_appui(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementAdminStaff.objects.filter(archived = "0",type_payement="Pers Appui").order_by('-id')

    form = TypePayementPersAdministratifForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-pers-appui.html', locals())

def liste_types_paiements_divers(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementDivers.objects.filter(archived = "0",type_payement="Divers").order_by('-id')

    form = TypePayementDiversForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-divers.html', locals())

def liste_types_paiements_cantine(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementDivers.objects.filter(archived = "0",type_payement="Cantine").order_by('-id')

    form = TypePayementDiversForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-cantine.html', locals())

def liste_types_paiements_transport(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementDivers.objects.filter(archived = "0",type_payement="Transport").order_by('-id')

    form = TypePayementDiversForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-transport.html', locals())

def liste_types_paiements_dortoir(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementDivers.objects.filter(archived = "0",type_payement="Dortoir").order_by('-id')

    form = TypePayementDiversForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-dortoir.html', locals())

def liste_types_paiements_facture(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    paiements = TypePayementDivers.objects.filter(archived = "0",type_payement="Facture").order_by('-id')

    form = TypePayementDiversForm  
    paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/liste-types-paiements-facture.html', locals())

def parametres_progression(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/parametres-progression.html', locals())

def parametres_reunion(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/parametres-reunion.html', locals())

def parametres_cours(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    cours = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

  
    return render(request, 'mainapp/pages/parametres-cours.html', locals())

def liste_profils(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    profils = Profil.objects.filter(archived="0").order_by('-id')
    
    form = ProfilForm
    paginator = Paginator(profils, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)

    groupes = Group.objects.all().order_by('name')


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default
        

    return render(request, 'mainapp/pages/liste-profils.html', locals())

def liste_divisionstemps(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    divisionstemps = []
    # divisionstemps = LesDivisionTemps.objects.filter(archived="0").order_by('-id')
    sousetabs = SousEtab.objects.filter(archived="0").order_by('-id')
    
    # form = ProfilForm
    paginator = Paginator(divisionstemps, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)

    # groupes = Group.objects.all().order_by('name')


    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default
        

    return render(request, 'mainapp/pages/liste-divisionstemps.html', locals())

def accueil(request):
    verrou = "Verrouiller"
    return render(request, 'mainapp/pages/accueil.html', locals())

def suppression_profil(request):

    id = int(request.POST['id_supp'])

    profil = Profil.objects.get(pk=id)
    profil.archived = "1"
    profil.save()

    return redirect('mainapp:liste_profils')

def suppression_etudiant(request):

    id = int(request.POST['id_supp'])

    # try:
    #     services.suppression_etudiant(id)

    # except ConnectionError:
    #     message_title = "Service de gestion des étudiants indisponible !!!"
    #     message_body = "Ce service est indisponible pour l'instant, veuillez reéssayer plus tard ou contacter l'administrateur"
    #     message_phone1 = "(+237) 676 06 94 52"
    #     message_phone2 = "(+237) 674 90 58 41"
    #     message_email1 = "ulrichguebayi@gmail.com"
    #     message_email2 = "agathe.signe@gmail.com"

    #     return render(request, 'mainapp/pages/erreur-service-indisponible.html', locals())
    Etudiant.objects.filter(pk=id).update(archived="1")
    return redirect('mainapp:liste_etudiants')

def suppression_eleve(request):

    id = int(request.POST['id_supp'])

    eleve = Eleve.objects.get(pk=id)
    eleve.archived = "1"
    eleve.save()

    return redirect('mainapp:liste_eleves')

def suppression_boursier(request):

    id = int(request.POST['id_supp'])

    eleve = Eleve.objects.get(pk=id).update(bourse = 0, liste_bourses_afficher = "", liste_bourses = "")

    return redirect('mainapp:liste_boursiers')

def suppression_etablissement(request):

    id = int(request.POST['id_supp'])
    # Etab.objects.get(pk=id).delete()
    
    Etab.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_etablissements')

def suppression_sous_etablissement(request):

    id = int(request.POST['id_supp'])
    # SousEtab.objects.get(pk=id).delete()
    SousEtab.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_sous_etablissements')

def suppression_cycle(request):

    id = int(request.POST['id_supp'])
    print("id= ", id)    
    Cycle.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_cycles')

def suppression_niveau(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    Niveau.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_niveaux')

def suppression_classe(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)
    nom_classe = Classe.objects.values('nom_classe').filter(pk = id)[0]['nom_classe']
    clss = str(id)+"_"+nom_classe+"_"   
    # Classe.objects.filter(pk=id).update(archived="1", specialite = "")
    Classe.objects.filter(pk=id).delete()
    specialites = Specialite.objects.filter(Q(liste_classes__icontains = clss))

    for s in specialites:
        # print("Inside ...")
        liste = s.liste_classes.replace(clss,"")
        liste_classes_afficher = s.liste_classes_afficher.replace(nom_classe+", ","")
        s.liste_classes = liste
        s.liste_classes_afficher = liste_classes_afficher
        if liste == "":
            # print("Specialite delete ...", s.specialite)
            # s.nom_niveau = ""
            s.delete()
        else:
            s.save()

    return redirect('mainapp:liste_classes')

def suppression_specialite(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    
    specialite_to_delete = Specialite.objects.filter(id = id)[0]
    print("Specialite", specialite_to_delete)

    inds = []
    tab = specialite_to_delete.liste_classes.split("_")
    nbre_ = len(tab) - 1
    if nbre_ > 0:
        tab.pop(nbre_)
        inds = [tab[item] for item in range(nbre_) if item % 2 == 0]
    print("Classe to delete: ",inds)

    for id_classe in inds:
        Classe.objects.filter( id = int(id_classe)).update(specialite = "")
    Specialite.objects.filter(id = id).delete()

    return redirect('mainapp:liste_specialites')

def suppression_classe_specialite(request):

    # Obtenir les classes associées au niveau id et à la spécialité et supprimer
    id = int(request.POST['id_supp'])
    print("id = ", id)
    specialite_to_delete = Specialite.objects.filter(id_niveau = id)[0]
    print("Specialite", specialite_to_delete)

    inds = []
    tab = specialite_to_delete.liste_classes.split("_")
    nbre_ = len(tab) - 1
    if nbre_ > 0:
        tab.pop(nbre_)
        inds = [tab[item] for item in range(nbre_) if item % 2 == 0]
    print("Classe to delete: ",inds)

    for id_classe in inds:
        Classe.objects.filter( id = int(id_classe)).update(specialite = "")
    Specialite.objects.filter(id_niveau = id).delete()
    # Specialite.objects.filter(id_niveau = id).update(archived="1")

    return redirect('mainapp:liste_classe_specialites')

def suppression_matiere(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    Matiere.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_matieres')

def suppression_appellation_apprenant_formateur(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    AppellationApprenantFormateur.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_appellation_apprenant_formateur')

def suppression_type_apprenant(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypeApprenant.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_type_apprenants')

def suppression_discipline(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    Discipline.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_disciplines')

def suppression_type_paiement_eleve(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementEleve.objects.filter(pk=id).delete()
    # TypePayementEleve.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_eleve')

def suppression_type_paiement_pers_administratif(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementAdminStaff.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_pers_administratif')

def suppression_type_paiement_pers_enseignant(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementAdminStaff.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_pers_enseignant')

def suppression_type_paiement_pers_appui(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementAdminStaff.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_pers_appui')

def suppression_type_paiement_divers(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementDivers.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_divers')

def suppression_type_paiement_cantine(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementDivers.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_cantine')

def suppression_type_paiement_transport(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementDivers.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_transport')

def suppression_type_paiement_dortoir(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementDivers.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_dortoir')

def suppression_type_paiement_facture(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    TypePayementDivers.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_types_paiements_facture')

def suppression_condition_renvoi(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    ConditionRenvoi.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_condition_renvois')

def suppression_condition_succes(request):

    id = int(request.POST['id_supp'])
    print("id = ", id)    
    ConditionSucces.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_condition_succes')

def modification_etudiant(request):

    id = int(request.POST['id_modif'])

    form = EtudiantForm(request.POST)

    if form.is_valid():

        matricule = form.cleaned_data['matricule']
        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prenom']
        age = form.cleaned_data['age']

        etudiant_data = {
            'matricule' : matricule,
            'nom' : nom,
            'prenom' : prenom,
            'age' : age
        }

        try:
            etudiant = services.modification_etudiant(id, etudiant_data)

        except ConnectionError:
            message_title = "Service de gestion des étudiants indisponible !!!"
            message_body = "Ce service est indisponible pour l'instant, veuillez reéssayer plus tard ou contacter l'administrateur"
            message_phone1 = "(+237) 676 06 94 52"
            message_phone2 = "(+237) 674 90 58 41"
            message_email1 = "ulrichguebayi@gmail.com"
            message_email2 = "agathe.signe@gmail.com"

            return render(request, 'mainapp/pages/erreur-service-indisponible.html', locals())
        return redirect('mainapp:liste_etudiants')

def modification_etablissement(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')

    form = EtablissementForm(request.POST)

    if form.is_valid():

        nom_etab = form.cleaned_data['nom_etab']
        date_creation = form.cleaned_data['date_creation']
        nom_fondateur = form.cleaned_data['nom_fondateur']
        localisation = form.cleaned_data['localisation']
        bp = form.cleaned_data['bp']
        email = form.cleaned_data['email']
        tel = form.cleaned_data['tel']
        devise = form.cleaned_data['devise']
        langue = form.cleaned_data['langue']
        annee_scolaire = form.cleaned_data['annee_scolaire']
        site_web = form.cleaned_data['site_web']

        # etab = Etab.objects.filter(pk=id)[0]

        # etab.nom_etab = nom_etab
        # etab.date_creation = date_creation
        # etab.nom_fondateur = nom_fondateur
        # etab.localisation = localisation
        # etab.bp = bp
        # etab.email = email
        # etab.tel = tel
        # etab.devise = devise
        # etab.langue = langue
        # etab.annee_scolaire = annee_scolaire
        # etab.site_web = site_web

        # etab.save()

        ####ajouter une transaction
        with transaction.atomic():

            if(Etab.objects.filter(pk=id)[0].nom_etab.lower() != nom_etab.lower()):
                Cycle.objects.filter(id_etab = id).update(nom_etab = nom_etab)
                Niveau.objects.filter(id_etab = id).update(nom_etab = nom_etab)
                Classe.objects.filter(id_etab = id).update(nom_etab = nom_etab)
                Cours.objects.filter(id_etab = id).update(nom_etab = nom_etab)
                SousEtab.objects.filter(id_etab = id).update(nom_etab = nom_etab)
                Specialite.objects.filter(id_etab = id).update(nom_etab = nom_etab)

                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "etab_"))
                for t in tpes:
                    t.indicateur_liste_classes = "etab_"+nom_etab+"_"+str(id)
                    t.liste_classes_afficher = nom_etab
                    t.save()

            Etab.objects.filter(pk=id).update(nom_etab=nom_etab,date_creation=date_creation,nom_fondateur=nom_fondateur,\
                localisation=localisation,bp=bp,email=email,tel=tel,devise=devise,langue=langue,\
                annee_scolaire=annee_scolaire,site_web=site_web)


        return redirect('mainapp:liste_etablissements')

def modification_sous_etablissement(request):

    id = int(request.POST['id_modif'])

    form = SousEtablissementForm(request.POST)

    if form.is_valid():

        nom_sousetab = form.cleaned_data['nom_sousetab']
        date_creation = form.cleaned_data['date_creation']
        nom_fondateur = form.cleaned_data['nom_fondateur']
        localisation = form.cleaned_data['localisation']
        # bp = form.cleaned_data['bp']
        # email = form.cleaned_data['email']
        # tel = form.cleaned_data['tel']
        # devise = form.cleaned_data['devise']
        # langue = form.cleaned_data['langue']
        # annee_scolaire = form.cleaned_data['annee_scolaire']
        # site_web = form.cleaned_data['site_web']

        # etab = Etab.objects.filter(pk=id)[0]

        # etab.nom_etab = nom_etab
        # etab.date_creation = date_creation
        # etab.nom_fondateur = nom_fondateur
        # etab.localisation = localisation
        # etab.bp = bp
        # etab.email = email
        # etab.tel = tel
        # etab.devise = devise
        # etab.langue = langue
        # etab.annee_scolaire = annee_scolaire
        # etab.site_web = site_web

        # etab.save()
        i = "toto"

        with transaction.atomic():

            if(SousEtab.objects.filter(pk=id)[0].nom_sousetab.lower() != nom_sousetab.lower()):
                Cycle.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Niveau.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Classe.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Cours.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Groupe.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Matiere.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                AppellationApprenantFormateur.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Discipline.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)
                Specialite.objects.filter(id_sousetab = id).update(nom_sousetab = nom_sousetab)

                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "sousetab_"))
                for t in tpes:
                    t.indicateur_liste_classes = "sousetab_"+nom_sousetab+"_"+str(id)
                    t.liste_classes_afficher = nom_sousetab
                    t.save()

            SousEtab.objects.filter(pk=id).update(nom_sousetab=nom_sousetab,date_creation=date_creation,nom_fondateur=nom_fondateur,\
                localisation=localisation)

        return redirect('mainapp:liste_sous_etablissements')

def modification_cycle(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = CycleForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom_cycle = form.cleaned_data['nom_cycle']
        nom_etab = form.cleaned_data['nom_etab']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        with transaction.atomic():

            if(Cycle.objects.filter(pk=id)[0].nom_cycle.lower() != nom_cycle.lower()):
                Niveau.objects.filter(id_cycle = id).update(nom_cycle = nom_cycle)
                Classe.objects.filter(id_cycle = id).update(nom_cycle = nom_cycle)
                Cours.objects.filter(id_cycle = id).update(nom_cycle = nom_cycle)

                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "cycle_"))
                for t in tpes:
                    ind = t.indicateur_liste_classes.split('_')[2]
                    if ind == str(id):
                        t.indicateur_liste_classes = "cycle_"+nom_cycle+"_"+str(id)
                        t.liste_classes_afficher = nom_cycle
                        t.save()


            Cycle.objects.filter(pk=id).update(nom_cycle=nom_cycle)

        return redirect('mainapp:liste_cycles')

def modification_niveau(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = NiveauForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom_cycle = form.cleaned_data['nom_cycle']
        nom_niveau = form.cleaned_data['nom_niveau']
        nom_etab = form.cleaned_data['nom_etab']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        with transaction.atomic():

            if(Niveau.objects.filter(pk=id)[0].nom_niveau.lower() != nom_niveau.lower()):
                Classe.objects.filter(id_niveau = id).update(nom_niveau = nom_niveau)
                ConditionRenvoi.objects.filter(id_niveau = id).update(nom_niveau = nom_niveau)
                Specialite.objects.filter(id_niveau = id).update(nom_niveau = nom_niveau)

                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "niveau_"))
                for t in tpes:
                    ind = t.indicateur_liste_classes.split('_')[2]
                    if ind == str(id):
                        t.indicateur_liste_classes = "niveau_"+nom_niveau+"_"+str(id)
                        t.liste_classes_afficher = nom_niveau
                        t.save()
                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "specialite_"))
                for t in tpes:
                    ind = t.indicateur_liste_classes.split('_')[2]
                    spe = t.indicateur_liste_classes.split('_')[1]
                    if ind == str(id):
                        t.indicateur_liste_classes = "specialite_"+spe+"_"+str(id)
                        t.liste_classes_afficher = nom_niveau+" "+spe
                        # t.id_niveau = str(id)
                        t.niveau = nom_niveau
                        t.save()
                    elif t.id_niveau == id and (ind == "all" or ind == "aucune"):
                        t.liste_classes_afficher = nom_niveau
                        t.niveau = nom_niveau
                        t.save()


            Niveau.objects.filter(pk=id).update(nom_niveau = nom_niveau)

        return redirect('mainapp:liste_niveaux')

def modifier_classe(id, nom_classe, nom_niveau, nom_etab, nom_sousetab, specialite):
    
    liste_classes = id+"_"+nom_classe+"_"
    liste_classes_afficher = nom_classe+", "
    ids = Classe.objects.values('id_etab','id_sousetab','id_niveau').filter(pk = int(id))[0]
    id_etab, id_sousetab, id_niveau = ids['id_etab'], ids['id_sousetab'], ids['id_niveau']
    c = Classe.objects.filter(pk = id)[0]

    if c.nom_classe.lower() == nom_classe.lower():
        if c.specialite.lower() != specialite.lower():
            # La classe n'était dans aucune spécialité
            if c.specialite == "":
                c.specialite = specialite
                c.save()

                # On cherche la spécialité ou insérer la classe
                if Specialite.objects.filter(specialite__iexact = specialite, nom_niveau__iexact = nom_niveau).count() > 0:
                    spe = Specialite.objects.filter(specialite__iexact = specialite, nom_niveau__iexact = nom_niveau)[0]
                    if liste_classes not in spe.liste_classes:
                        spe.liste_classes = spe.liste_classes + liste_classes
                        spe.liste_classes_afficher = spe.liste_classes_afficher + liste_classes_afficher
                        spe.save()
                    specialites = Specialite.objects.filter(~Q(pk = spe.id), Q(liste_classes__icontains = liste_classes))
                    for s in specialites:
                        s.liste_classes = s.liste_classes.replace(liste_classes, "")
                        s.liste_classes_afficher = s.liste_classes_afficher.replace(liste_classes_afficher, "")
                        s.save()
                # C'est une nouvelle spécialité
                else:
                    sp = Specialite()
                    sp.nom_etab = nom_etab
                    sp.id_etab = id_etab
                    sp.nom_sousetab = nom_sousetab
                    sp.id_sousetab = id_sousetab
                    sp.nom_niveau = nom_niveau
                    sp.id_niveau = id_niveau
                    sp.specialite = specialite
                    sp.liste_classes = liste_classes
                    sp.liste_classes_afficher = liste_classes_afficher
                    sp.save()
                    
            elif specialite == "":
                c.specialite = ""
                c.save()
                specs = Specialite.objects.filter(Q(liste_classes__icontains = liste_classes))
                for sp in specs:
                    sp.liste_classes = sp.liste_classes.replace(liste_classes,"")
                    sp.liste_classes_afficher = sp.liste_classes_afficher.replace(liste_classes_afficher,"")
                    if sp.liste_classes == "":
                        sp.delete()
                    else:
                        sp.save()
            # Ancienne et nouvelle spécialité sont différentes
            elif specialite != "":
                c.specialite = specialite
                c.save()
                print("DEBUT")
                # On cherche la spécialité ou insérer la classe
                if Specialite.objects.filter(specialite__iexact = specialite, nom_niveau__iexact = nom_niveau).count() > 0:
                    spe = Specialite.objects.filter(specialite__iexact = specialite, nom_niveau__iexact = nom_niveau)[0]
                    if liste_classes not in spe.liste_classes:
                        spe.liste_classes = spe.liste_classes + liste_classes
                        spe.liste_classes_afficher = spe.liste_classes_afficher + liste_classes_afficher
                        spe.save()
                    specialites = Specialite.objects.filter(~Q(pk = spe.id), Q(liste_classes__icontains = liste_classes))
                    for s in specialites:
                        s.liste_classes = s.liste_classes.replace(liste_classes, "")
                        s.liste_classes_afficher = s.liste_classes_afficher.replace(liste_classes_afficher, "")
                        if s.liste_classes == "":
                            s.delete()
                        else:
                            s.save()
                # C'est une nouvelle spécialité
                else:
                    sp = Specialite()
                    sp.nom_etab = nom_etab
                    sp.id_etab = id_etab
                    sp.nom_sousetab = nom_sousetab
                    sp.id_sousetab = id_sousetab
                    sp.nom_niveau = nom_niveau
                    sp.id_niveau = id_niveau
                    sp.specialite = specialite
                    sp.liste_classes = liste_classes
                    sp.liste_classes_afficher = liste_classes_afficher
                    sp.save()

                    print("**ICI")
                    specs = Specialite.objects.filter(~Q(pk = sp.id), Q(liste_classes__icontains = liste_classes))
                    print("**count, ", specs.count())
                    for sp in specs:
                        print("**On Boucle...")
                        sp.liste_classes = sp.liste_classes.replace(liste_classes,"")
                        sp.liste_classes_afficher = sp.liste_classes_afficher.replace(liste_classes_afficher,"")
                        if sp.liste_classes == "":
                            sp.delete()
                        else:
                            sp.save()

def modification_classe(request):

    id = request.POST['id_modif']
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = ClasseForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom_classe = form.cleaned_data['nom_classe']
        nom_cycle = form.cleaned_data['nom_cycle']
        nom_niveau = form.cleaned_data['nom_niveau']
        nom_etab = form.cleaned_data['nom_etab']
        nom_sousetab = form.cleaned_data['nom_sousetab']
        specialite = request.POST['choix_specialite'].strip()
        # specialite = specialite.lower()

        liste_classes = id+"_"+nom_classe+"_"
        liste_classes_afficher = nom_classe+", "
        c = Classe.objects.filter(pk = id)[0]

        with transaction.atomic():
            c = Classe.objects.filter(pk = id)[0]
            if c.nom_classe.lower() == nom_classe.lower():
                modifier_classe(id, nom_classe, nom_niveau, nom_etab, nom_sousetab, specialite)
            else:
                # On effectue d'abord le rennomage de la classe dans la bd puis on appelle
                #  la fonction modifier_classe coe ci-dessus car on aura la meme configuration
                Cours.objects.filter(id_classe = id).update(nom_classe = nom_classe)
                nom_classe_old = c.nom_classe
                c.nom_classe = nom_classe
                c.save()

                classe = id+"_"+nom_classe+"_"
                classe_afficher = nom_classe+", "
                classe_old = id+"_"+nom_classe_old+"_"
                classe_afficher_old = nom_classe_old+", "

                specialites = Specialite.objects.filter(Q(liste_classes__icontains = classe_old))
                for s in specialites:
                    s.liste_classes = s.liste_classes.replace(classe_old, classe)
                    s.liste_classes_afficher = s.liste_classes_afficher.replace(classe_afficher_old, classe_afficher)
                    s.save()
                modifier_classe(id, nom_classe, nom_niveau, nom_etab, nom_sousetab, specialite)

        return redirect('mainapp:liste_classes')

def modification_specialite(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = SpecialiteForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        specialite = form.cleaned_data['specialite']
        id_etab = form.cleaned_data['id_etab']
        id_sousetab = form.cleaned_data['id_sousetab']
        nom_etab = form.cleaned_data['nom_etab']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        with transaction.atomic():
            old_spe = Specialite.objects.filter(pk=id)[0].specialite
            if old_spe.lower() != specialite.lower():
                Classe.objects.filter(specialite__iexact = old_spe).update(specialite = specialite)

                tpes = TypePayementEleve.objects.filter(Q(indicateur_liste_classes__istartswith = "specialite_"))
                for t in tpes:
                    ind = t.indicateur_liste_classes.split('_')[2]
                    spe = t.indicateur_liste_classes.split('_')[1]
                    if ind == str(id):
                        t.indicateur_liste_classes = "specialite_"+specialite+"_"+str(id)
                        t.liste_classes_afficher = nom_niveau+" "+specialite
                        t.save()

        Specialite.objects.filter(pk=id).update(specialite = specialite)

        

        return redirect('mainapp:liste_specialites')

def modification_classe_specialite(request):

    id = request.POST['id_modif']
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = ClasseSpecialiteForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    # On selectionne les classes impactées par la modif grace à l'id du niveau et la specialite
    # On update la specialite des classes concernées

    # if form.is_valid():

    #     nom_classe = form.cleaned_data['nom_classe']
    #     nom_cycle = form.cleaned_data['nom_cycle']
    #     nom_niveau = form.cleaned_data['nom_niveau']
    #     nom_etab = form.cleaned_data['nom_etab']
    #     nom_sousetab = form.cleaned_data['nom_sousetab']

    #     with transaction.atomic():

    #         if(Classe.objects.filter(pk=id)[0].nom_classe.lower() != nom_classe.lower()):
    #             Cours.objects.filter(id_classe = id).update(nom_classe = nom_classe)

    #         Classe.objects.filter(pk=id).update(nom_classe = nom_classe)

        # return redirect('mainapp:liste_classes')
    return redirect('mainapp:liste_classe_specialites')

def modification_matiere(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = MatiereForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom_matiere = form.cleaned_data['nom_matiere']
        code = form.cleaned_data['code']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        with transaction.atomic():

            if(Matiere.objects.filter(pk=id)[0].nom_matiere.lower() != nom_matiere.lower()):
                Cours.objects.filter(id_matiere = id).update(nom_matiere = nom_matiere)       

            Matiere.objects.filter(pk=id).update(nom_matiere = nom_matiere, code= code, nom_sousetab=nom_sousetab)

        return redirect('mainapp:liste_matieres')

def modification_eleve(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = EleveForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prenom']
        sexe = form.cleaned_data['sexe']
        redouble = form.cleaned_data['redouble']
        date_naissance = form.cleaned_data['date_naissance'].split('T')[0]
        lieu_naissance = form.cleaned_data['lieu_naissance']
        date_entree = form.cleaned_data['date_entree']
        nom_pere = form.cleaned_data['nom_pere']
        prenom_pere = form.cleaned_data['prenom_pere']
        nom_mere = form.cleaned_data['nom_mere']
        prenom_mere = form.cleaned_data['prenom_mere']
        tel_pere = form.cleaned_data['tel_pere']
        tel_mere = form.cleaned_data['tel_mere']
        email_pere = form.cleaned_data['email_pere']
        email_mere = form.cleaned_data['email_mere']
        # sexe = form.cleaned_data['sexe']  
        print("PRENOM PERE:", prenom_pere)
        Eleve.objects.filter(pk=id).update(
        # matricule = matricule,
        nom = nom,
        prenom= prenom,
        sexe=sexe,
        redouble=redouble,
        date_naissance=date_naissance,
        lieu_naissance=lieu_naissance,
        date_entree=date_entree,
        nom_pere=nom_pere,
        prenom_pere=prenom_pere,
        nom_mere=nom_mere,
        prenom_mere=prenom_mere,
        tel_pere=tel_pere,
        tel_mere=tel_mere,
        email_pere=email_pere,
        email_mere=email_mere,
        )

    return redirect('mainapp:liste_eleves')

# modification_eleve2 en lieu et place de modification_periodes_saisie_actives j'ai eu qlq soucis avec les urls
def modification_eleve2(request):

    date_deb_saisie, date_deb_saisie_en = "", ""
    date_fin_saisie, date_fin_saisie_en = "", ""
    is_active = False
    activer = "yes" if 'activer' in  request.POST else 'no'
    id = int(request.POST['id_modif'])
    evaluations_id = request.POST.getlist('evaluation')
    
    indicateur_date, ok = request.POST['dates_ok'].split("_");
    if activer == 'yes':
        # date_deb et date_fin fournies
        if indicateur_date == "all":
            date_deb_saisie, date_deb_saisie_en = date_correct(request.POST['date_deb_saisie'])
            date_fin_saisie, date_fin_saisie_en = date_correct(request.POST['date_fin_saisie'])
            is_active = True
        elif indicateur_date == "deb":
            date_deb_saisie, date_deb_saisie_en = date_correct(request.POST['date_deb_saisie'])
            is_active = True
        elif indicateur_date == "fin":
            date_fin_saisie, date_fin_saisie_en = date_correct(request.POST['date_fin_saisie'])
            is_active = True
        elif indicateur_date == "bad":
            is_active = True
    else:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        p, today = date_correct(today)

        date_deb_saisie = request.POST['date_deb_saisie']
        date_fin_saisie = request.POST['date_fin_saisie']
        date_deb_saisie, date_deb_saisie_en = date_correct(date_deb_saisie)
        date_fin_saisie, date_fin_saisie_en = date_correct(date_fin_saisie)
        is_active = set_divisiontemps_status(date_deb_saisie_en, date_fin_saisie_en,today)


        # is_active = True if 'is_active' in request.POST['is_active'] else False
        # if is_active == False:
        #     today = date.today()
        #     today = today.strftime("%d/%m/%Y")
        #     p, today = date_correct(today)
        #     is_active = set_divisiontemps_status(date_deb_saisie_en, date_fin_saisie_en,today)


    # print(request.POST['dates_ok'])
    # print(request.POST.getlist('evaluation'))
    id_sousetab_selected = request.POST['id_sousetab_selected']
    for evaluation_id in evaluations_id:
        print("evaluation_id: ", evaluation_id)
        LesDivisionTempsSousEtab.objects.filter(pk = int(evaluation_id)).update(date_deb_saisie= date_deb_saisie,
            date_fin_saisie= date_fin_saisie, date_deb_saisie_en= date_deb_saisie_en, 
            date_fin_saisie_en = date_fin_saisie_en, is_active=is_active)
    request.session['id_sousetab'] = id_sousetab_selected
    return redirect('mainapp:periodes_saisie_actives')

    # return redirect('mainapp:liste_eleves')

# modification_eleve3 en lieu et place de modification_jours_ouvrables j'ai eu qlq soucis avec les urls
def modification_eleve3(request):
    for r in request.POST:
        print(r,request.POST[r])
    jours = ["","","","","","",""]
    jours_afficher =""
    id_sousetab = request.POST["id_sousetab"]
    cpt = 1
    heure_deb_cours = request.POST["heure_deb_cours_h"]+"h"+request.POST["heure_deb_cours_m"] if request.POST["heure_deb_cours_h"]!="" else ""
    duree_tranche_horaire = request.POST["duree_tranche_horaire"]
    nb_pauses = int(request.POST['nb_pauses'])
    libelle_pauses = []
    heure_pauses = []

    while cpt <= nb_pauses:
        print(cpt)
        libelle_pause = request.POST["libelle_pause"+str(cpt)]
        print("libelle_pause ",libelle_pause)
        pause = request.POST["pause"+str(cpt)]
        libelle_pauses.append(libelle_pause)
        heure_pauses.append(pause)
        
        # print("libelle, pause: ", libelle_pause, pause)
        cpt += 1
    
    sousetabs = SousEtab.objects.filter(id = int(id_sousetab))

    Pause.objects.filter(id_sousetab=id_sousetab).delete()

    for i in range(nb_pauses):
        pause = Pause()
        pause.libelle = libelle_pauses[i]
        pause.duree = int(heure_pauses[i])
        pause.id_sousetab = id_sousetab
        pause.archived = 0
        pause.save()
    pauses = Pause.objects.filter(id_sousetab=id_sousetab)
    liste_pauses = ""
    liste_pauses_afficher = ""
    for p in pauses:
        liste_pauses += str(p.id)+"~"+p.libelle+"##"+str(p.duree)+"]"
        liste_pauses_afficher += p.libelle+": "+str(p.duree)+", "
    
    Jour.objects.filter(id_sousetab=id_sousetab).delete()
    for i in range(1,8):
        jour = "jour"+str(i)
        if jour in request.POST:
            if i == 1:
                jour = 'lundi'
                jours[0] = jour
            if i == 2:
                jour = 'mardi'
                jours[1] = jour
            if i == 3:
                jour = 'mercredi'
                jours[2] = jour
            if i == 4:
                jour = 'jeudi'
                jours[3] = jour
            if i == 5:
                jour = 'vendredi'
                jours[4] = jour
            if i == 6:
                jour = 'samedi'
                jours[5] = jour
            if i == 7:
                jour = 'dimanche'
                jours[6] = jour

    for i in range(7):
        if jours[i] != "":
            jours_afficher += jours[i]+", "
            jour = Jour()
            jour.libelle = jours[i]
            jour.id_sousetab = id_sousetab
            jour.nom_sousetab = sousetabs[0].nom_sousetab
            jour.archived = 0
            jour.save()
    print("jours_afficher: ",jours_afficher)
    
    SousEtab.objects.filter(id = int(id_sousetab)).update(liste_jours_ouvrables = jours_afficher,
        heure_deb_cours=heure_deb_cours, duree_tranche_horaire=duree_tranche_horaire,
        liste_pauses_afficher=liste_pauses_afficher, liste_pauses=liste_pauses)
    # print("liste_jours_ouvrables: ", liste_jours_ouvrables)

    # On récupère la langue pour faire l'internationalisation des jours
    # current_lang peut être fr, en, ar
    # Non c'est plutôt à l'affichage dans jours_ouvrables qu'on fera l'internationalisation
    current_lang = request.POST['current_lang']
    # _('A')
    
    return redirect('mainapp:jours_ouvrables')

    # return redirect('mainapp:liste_eleves')

# h, m are int
def hour_format(h,m):

    heure = "0"+ str(h) +"h" if h < 10 else str(h)+"h"
    heure += "0"+ str(m)  if m < 10 else str(m)

    return heure
# deb_tranche du type 07h50
def get_fin_tranche_hour(deb_tranche, duree):

    h,m = deb_tranche.split("h")
    last_heure_h = int(h)
    last_heure_m = int(m)
    minutes = duree%60
    heures = duree//60
    last_heure_m += minutes
    last_heure_h += heures
    last_heure_h += last_heure_m//60
    last_heure_m = last_heure_m % 60
    last_heure_h = last_heure_h % 24

    return hour_format(last_heure_h, last_heure_m)

def modification_def_tranche_horaire(request):
    id_jours = request.POST.getlist('jours')
    nb_jours = len(id_jours)
    # On efface d'abord les tranche de la journee si elle existe car elle sera overwrite
    nb_jrs = 0

    for id_jour in id_jours:
        jour = Jour.objects.filter(id=int(id_jour))[0]
        tranches = jour.tranche_horaires_id
        nb_jrs = 0
        for t in tranches:
            print(t)
            nb_jrs = TrancheHoraire.objects.values('nb_jours').filter(id=t)[0]['nb_jours']
            print(nb_jrs)
            nbr_jrs = nb_jrs - 1
            if nbr_jrs < 0:
                nbr_jrs = 0
            TrancheHoraire.objects.filter(id=t).update(nb_jours = nbr_jrs)

    TrancheHoraire.objects.filter(nb_jours=0).delete()

    indicateur_tranche = request.POST['indicateur_tranche'].split("²²")
    duree_tranche_horaire = int(request.POST['duree_tranche_horaire'])
    heure_deb_cours = request.POST['heure_deb_cours'].split("h")
    deb_h = hour_format(int(heure_deb_cours[0]), int(heure_deb_cours[1]))
    deb_h_jour = deb_h
    id_sousetab = int(request.POST["id_sousetab"])
    nom_sousetab =SousEtab.objects.values('nom_sousetab').filter(id=id_sousetab)[0]['nom_sousetab']
    numero_tranche = 1
    numero_tranche_only = 1
    for tranche in indicateur_tranche:
        th = TrancheHoraire()
        th.archived = "0"
        th.numero_tranche = numero_tranche
        th.heure_deb = deb_h
        th.id_sousetab = id_sousetab
        th.nom_sousetab = nom_sousetab
        th.nb_jours = nb_jours
        # C'est une pause avec sa duree
        if len(tranche.split("$$")) == 2:
            tranche = tranche.split("$$")
            th.type_tranche = 1
            th.libelle = tranche[0].strip()
            duree = int(tranche[1])
            # print(tranche, tranche[0].strip())
            # print(id_sousetab)
            th.id_pause = Pause.objects.values('id').filter(id_sousetab=id_sousetab,
             libelle__icontains=th.libelle, duree = duree)[0]['id']
            th.heure_fin = get_fin_tranche_hour(deb_h, duree)
            print(numero_tranche,deb_h,th.heure_fin)
            deb_h = th.heure_fin
            th.save()
        else:
            th.libelle = "Tranche"+str(numero_tranche_only)
            th.heure_fin = get_fin_tranche_hour(deb_h, duree_tranche_horaire)
            print(numero_tranche,deb_h,th.heure_fin)
            deb_h = th.heure_fin
            th.numero_tranche_only = numero_tranche_only
            numero_tranche_only += 1
            th.save()

        for id_jour in id_jours:
            jour = Jour.objects.filter(id=int(id_jour))[0]
            jour.id_sousetab = id_sousetab
            jour.nom_sousetab = nom_sousetab
            jour.heure_deb_cours = deb_h_jour
            jour.heure_fin_cours = th.heure_fin
            jour.archived = 0
            jour.tranche_horaires.add(th)
            jour.save()
           
        numero_tranche += 1
        print("***  ",th)
    
    return redirect('mainapp:definition_tranches_horaires')

    # return redirect('mainapp:liste_eleves')

def modification_jours_ouvrables(request):
    print("On est la...")
    # date_deb_saisie, date_deb_saisie_en = "", ""
    # date_fin_saisie, date_fin_saisie_en = "", ""
    # is_active = False
    # activer = "yes" if 'activer' in  request.POST else 'no'
    # id = int(request.POST['id_modif'])
    # evaluations_id = request.POST.getlist('evaluation')
    
    # indicateur_date, ok = request.POST['dates_ok'].split("_");
    # if activer == 'yes':
    #     # date_deb et date_fin fournies
    #     if indicateur_date == "all":
    #         date_deb_saisie, date_deb_saisie_en = date_correct(request.POST['date_deb_saisie'])
    #         date_fin_saisie, date_fin_saisie_en = date_correct(request.POST['date_fin_saisie'])
    #         is_active = True
    #     elif indicateur_date == "deb":
    #         date_deb_saisie, date_deb_saisie_en = date_correct(request.POST['date_deb_saisie'])
    #         is_active = True
    #     elif indicateur_date == "fin":
    #         date_fin_saisie, date_fin_saisie_en = date_correct(request.POST['date_fin_saisie'])
    #         is_active = True
    #     elif indicateur_date == "bad":
    #         is_active = True
    # else:
    #     today = date.today()
    #     today = today.strftime("%d/%m/%Y")
    #     p, today = date_correct(today)

    #     date_deb_saisie = request.POST['date_deb_saisie']
    #     date_fin_saisie = request.POST['date_fin_saisie']
    #     date_deb_saisie, date_deb_saisie_en = date_correct(date_deb_saisie)
    #     date_fin_saisie, date_fin_saisie_en = date_correct(date_fin_saisie)
    #     is_active = set_divisiontemps_status(date_deb_saisie_en, date_fin_saisie_en,today)


    #     # is_active = True if 'is_active' in request.POST['is_active'] else False
    #     # if is_active == False:
    #     #     today = date.today()
    #     #     today = today.strftime("%d/%m/%Y")
    #     #     p, today = date_correct(today)
    #     #     is_active = set_divisiontemps_status(date_deb_saisie_en, date_fin_saisie_en,today)


    # # print(request.POST['dates_ok'])
    # # print(request.POST.getlist('evaluation'))
    # id_sousetab_selected = request.POST['id_sousetab_selected']
    # for evaluation_id in evaluations_id:
    #     print("evaluation_id: ", evaluation_id)
    #     LesDivisionTempsSousEtab.objects.filter(pk = int(evaluation_id)).update(date_deb_saisie= date_deb_saisie,
    #         date_fin_saisie= date_fin_saisie, date_deb_saisie_en= date_deb_saisie_en, 
    #         date_fin_saisie_en = date_fin_saisie_en, is_active=is_active)
    # request.session['id_sousetab'] = id_sousetab_selected
    return redirect('mainapp:periodes_jours_ouvrables')

    # return redirect('mainapp:liste_eleves')

def modification_boursier(request):
    # Fction à adapter
    id = int(request.POST['id_modif'])
    form = BoursierForm(request.POST)

    if form.is_valid():

        nom = form.cleaned_data['nom']
        Eleve.objects.filter(pk=id).update(bourse = 0, liste_bourses_afficher = "", liste_bourses = ""
        )

        return redirect('mainapp:liste_Bourses')

def modification_appellation_apprenant_formateur(request):

    id = int(request.POST['id_modif'])
    form = AppellationApprenantFormateurForm(request.POST)

    if form.is_valid():

        apprenant = form.cleaned_data['apprenant']
        formateur = form.cleaned_data['formateur']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        AppellationApprenantFormateur.objects.filter(pk=id).update(appellation_apprenant = apprenant, appellation_formateur= formateur, nom_sousetab=nom_sousetab)

        return redirect('mainapp:liste_appellation_apprenant_formateur')

def modification_type_apprenant(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = TypeApprenantForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        type_apprenant = form.cleaned_data['nom_type_apprenant']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        Matiere.objects.filter(pk=id).update(nom_type_apprenant = type_apprenant,nom_sousetab=nom_sousetab)

        return redirect('mainapp:liste_type_apprenants')

def modification_discipline(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = DisciplineForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():
        fait = form.cleaned_data['fait']
        description = form.cleaned_data['description']
        nb_heures_min = form.cleaned_data['nb_heures_min']
        nb_heures_max = form.cleaned_data['nb_heures_max']
        sanction = form.cleaned_data['sanction']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        Discipline.objects.filter(pk=id).update(fait = fait, description= description, nb_heures_min= nb_heures_min, nb_heures_max= nb_heures_max,sanction=sanction, nom_sousetab=nom_sousetab)

    return redirect('mainapp:liste_disciplines')

def modification_type_paiement_eleve(request):

    id = int(request.POST['id_modif'])
    form = TypePayementEleveForm(request.POST)
    print("******* ",form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        classe = form.cleaned_data['classe']

        TypePayementEleve.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_eleve')

def modification_type_paiement_pers_administratif(request):
    print("Yo")
    id = int(request.POST['id_modif'])
    form = TypePayementPersAdministratifForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        type_payement = form.cleaned_data['type_payement']
        person = form.cleaned_data['person']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,type_payement,person,entree_sortie_caisee)
        TypePayementAdminStaff.objects.filter(pk=id).update(libelle = libelle, type_payement= type_payement, person= person, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_pers_administratif')

def modification_type_paiement_pers_enseignant(request):

    id = int(request.POST['id_modif'])
    form = TypePayementPersAdministratifForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        type_payement = form.cleaned_data['type_payement']
        person = form.cleaned_data['person']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,type_payement,person,entree_sortie_caisee)
        TypePayementAdminStaff.objects.filter(pk=id).update(libelle = libelle, type_payement= type_payement, person= person, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_pers_enseignant')

def modification_type_paiement_pers_appui(request):

    id = int(request.POST['id_modif'])
    form = TypePayementPersAdministratifForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        type_payement = form.cleaned_data['type_payement']
        person = form.cleaned_data['person']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,type_payement,person,entree_sortie_caisee)
        TypePayementAdminStaff.objects.filter(pk=id).update(libelle = libelle, type_payement= type_payement, person= person, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_pers_appui')

def modification_type_paiement_divers(request):

    id = int(request.POST['id_modif'])
    form = TypePayementDiversForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,date_deb,entree_sortie_caisee)
        TypePayementDivers.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_divers')

def modification_type_paiement_cantine(request):

    id = int(request.POST['id_modif'])
    form = TypePayementDiversForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,date_deb,entree_sortie_caisee)
        TypePayementDivers.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_cantine')

def modification_type_paiement_transport(request):

    id = int(request.POST['id_modif'])
    form = TypePayementDiversForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,date_deb,entree_sortie_caisee)
        TypePayementDivers.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_transport')

def modification_type_paiement_dortoir(request):

    id = int(request.POST['id_modif'])
    form = TypePayementDiversForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,date_deb,entree_sortie_caisee)
        TypePayementDivers.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_dortoir')

def modification_type_paiement_facture(request):

    id = int(request.POST['id_modif'])
    form = TypePayementDiversForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        date_deb = form.cleaned_data['date_deb']
        date_fin = form.cleaned_data['date_fin']
        entree_sortie_caisee = form.cleaned_data['entree_sortie_caisee']
        montant = form.cleaned_data['montant']
        print("*******")
        print(libelle,date_deb,entree_sortie_caisee)
        TypePayementDivers.objects.filter(pk=id).update(libelle = libelle, date_deb= date_deb, date_fin= date_fin, entree_sortie_caisee= entree_sortie_caisee,montant=montant)

    return redirect('mainapp:liste_types_paiements_facture')

def modification_condition_renvoi(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = ConditionRenvoiForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():
        nb_heures_max = form.cleaned_data['nb_heures_max']
        age = form.cleaned_data['age']
        moyenne = form.cleaned_data['moyenne']
        nb_jours = form.cleaned_data['nb_jours']
        nom_niveau = form.cleaned_data['nom_niveau']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        ConditionRenvoi.objects.filter(pk=id).update(nb_heures_max = nb_heures_max, age= age, moyenne= moyenne, nb_jours= nb_jours,nom_niveau=nom_niveau, nom_sousetab=nom_sousetab)

    return redirect('mainapp:liste_condition_renvois')

def modification_condition_succes(request):

    id = int(request.POST['id_modif'])
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    # print("id =",id)
    form = ConditionSuccesForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():
        moyenne = form.cleaned_data['moyenne']
        nom_niveau = form.cleaned_data['nom_niveau']
        nom_sousetab = form.cleaned_data['nom_sousetab']

        ConditionSucces.objects.filter(pk=id).update(moyenne= moyenne, nom_niveau=nom_niveau, nom_sousetab=nom_sousetab)

    return redirect('mainapp:liste_condition_succes')

def modification_periodes_saisie_actives(request):
    print("Affiche même bonjour...")
    # id = int(request.POST['id_modif'])
    # print("Cote serveur ...")
    # print(request.POST['dates_ok'])
    # print(request.POST.getlist('evaluation'))
    # date_deb_saisie, date_deb_saisie_en = date_correct(request.POST['date_deb_saisie'])
    # date_fin_saisie, date_fin_saisie_en = date_correct(request.POST['date_fin_saisie'])
    # is_active = True if 'is_active' in request.POST['is_active'] else False
    # if is_active == False:
    #     today = date.today()
    #     today = today.strftime("%d/%m/%Y")
    #     p, today = date_correct(today)
    #     is_active = set_divisiontemps_status(date_deb_saisie_en, date_fin_saisie_en,today)

    # LesDivisionTempsSousEtab.objects.filter(pk=id).update(date_deb_saisie= date_deb_saisie,
    #     date_fin_saisie= date_fin_saisie, date_deb_saisie_en= date_deb_saisie_en, 
    #     date_fin_saisie_en = date_fin_saisie_en, is_active=is_active)

    # return redirect('mainapp:periodes_saisie_actives')
    return redirect('mainapp:liste_eleves')

def recherche_jours_ouvrables(request):
    print("salut")
    # sousetabs = []
    # id_sousetabs = []
    # periode_saisies = []
    # nom_evaluation = ""
    print("Saluté...")
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            # id_sousetab = int(donnees[4])
            
            # sousetabs = SousEtab.objects.values('nom_sousetab','id').filter(archived="0").order_by('id')
            # id_sousetabs = [s['id'] for s in sousetabs]
            # sousetabs = [s['nom_sousetab'] for s in sousetabs]
            # jours_ouvrables = SousEtab.objects.filter(archived = "0").order_by('libelle')
            # nom_evaluation = SousEtab.objects.values('nom_division_temps_saisisable').filter(id=id_sousetab)[0]['nom_division_temps_saisisable']
            
            jours_ouvrables = find_jours_ouvrables(donnees_recherche,trier_par)
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(jours_ouvrables)

            #form = EtudiantForm
            paginator = Paginator(jours_ouvrables, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "jours_ouvrables": jours_ouvrables,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

            return JSONResponse(data) 

# def recherche_periodes_saisie_actives(request):
def recherche_eleve3(request):
    print("salut")
    sousetabs = []
    id_sousetabs = []
    periode_saisies = []
    nom_evaluation = ""
    print("Saluté...")
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            id_sousetab = int(donnees[4])
            
            sousetabs = SousEtab.objects.values('nom_sousetab','id').filter(archived="0").order_by('id')
            id_sousetabs = [s['id'] for s in sousetabs]
            id_sousetab_selected = id_sousetab
            sousetabs = [s['nom_sousetab'] for s in sousetabs]
            periode_saisies = LesDivisionTempsSousEtab.objects.filter(archived = "0", id_sousetab = id_sousetab, mode = "saisi").order_by('libelle')
            nom_evaluation = SousEtab.objects.values('nom_division_temps_saisisable').filter(id=id_sousetab)[0]['nom_division_temps_saisisable']
            
            periode_saisies = find_periodes_saisie_actives(donnees_recherche,trier_par,id_sousetab)
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(periode_saisies)

            #form = EtudiantForm
            paginator = Paginator(periode_saisies, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "sousetabs": sousetabs,
                "id_sousetabs": id_sousetabs,
                "periode_saisies": periode_saisies,
                "nom_evaluation": nom_evaluation,
                "id_sousetab_selected": id_sousetab_selected,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

# def recherche_jours_ouvrables(request):
def recherche_eleve33(request):
    print("salut")
    # sousetabs = []
    # id_sousetabs = []
    # periode_saisies = []
    # nom_evaluation = ""
    print("Saluté...")
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            # id_sousetab = int(donnees[4])
            
            # sousetabs = SousEtab.objects.values('nom_sousetab','id').filter(archived="0").order_by('id')
            # id_sousetabs = [s['id'] for s in sousetabs]
            # sousetabs = [s['nom_sousetab'] for s in sousetabs]
            # jours_ouvrables = SousEtab.objects.filter(archived = "0").order_by('libelle')
            # nom_evaluation = SousEtab.objects.values('nom_division_temps_saisisable').filter(id=id_sousetab)[0]['nom_division_temps_saisisable']
            
            jours_ouvrables = find_jours_ouvrables(donnees_recherche,trier_par)
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(jours_ouvrables)

            #form = EtudiantForm
            paginator = Paginator(jours_ouvrables, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "jours_ouvrables": jours_ouvrables,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

            return JSONResponse(data) 

def find_jours_ouvrables(recherche, trier_par):
    print("**trier_par", trier_par)
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            jours_ouvrables =  SousEtab.objects.values('id','nom_sousetab','liste_jours_ouvrables',
                'duree_tranche_horaire','heure_deb_cours','liste_pauses','liste_pauses_afficher').filter(archived = "0").order_by('-id')
        else:
            jours_ouvrables = SousEtab.objects.values('id','nom_sousetab','liste_jours_ouvrables',
                'duree_tranche_horaire','heure_deb_cours','liste_pauses','liste_pauses_afficher').filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            jours_ouvrables = SousEtab.objects.values('id','nom_sousetab','liste_jours_ouvrables',
                'duree_tranche_horaire','heure_deb_cours','liste_pauses','liste_pauses_afficher').filter(Q(archived ="0") &
                (Q(liste_jours_ouvrables__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(duree_tranche_horaire__icontains=recherche) |
                Q(heure_deb_cours__icontains = recherche) |
                # Q(liste_pauses__icontains=recherche) |
                Q(liste_pauses_afficher__icontains=recherche)
                )
            ).distinct()

        else:
            jours_ouvrables = SousEtab.objects.values('id','nom_sousetab','liste_jours_ouvrables',
                'duree_tranche_horaire','heure_deb_cours','liste_pauses','liste_pauses_afficher').filter(Q(archived ="0") &
               (Q(liste_jours_ouvrables__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(duree_tranche_horaire__icontains=recherche) |
                Q(heure_deb_cours__icontains = recherche) |
                # Q(liste_pauses__icontains=recherche) |
                Q(liste_pauses_afficher__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            
    jours_ouvrables_serializers = SousEtabJoursOuvrablesSerializer(jours_ouvrables, many=True)

    return jours_ouvrables_serializers.data

def find_periodes_saisie_actives(recherche, trier_par, id_sousetab):
    print("**trier_par", trier_par)
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            periode_saisies = LesDivisionTempsSousEtab.objects.filter(archived = "0", mode = "saisi", id_sousetab = id_sousetab).order_by('-id')
        else:
            periode_saisies = LesDivisionTempsSousEtab.objects.filter(archived = "0", mode = "saisi", id_sousetab = id_sousetab).order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            periode_saisies = LesDivisionTempsSousEtab.objects.filter(Q(archived ="0") & Q(mode = "saisi") & Q(id_sousetab = id_sousetab) &
                (Q(nom_sousetab__icontains=recherche) |
                Q(libelle__icontains=recherche) |
                # Q(is_active = recherche) |
                Q(date_deb_saisie__icontains=recherche) |
                Q(date_fin_saisie__icontains=recherche)
                )
            ).distinct()

        else:
            periode_saisies = LesDivisionTempsSousEtab.objects.filter(Q(archived ="0") & Q(mode = "saisi") & Q(id_sousetab = id_sousetab) &
               (Q(nom_sousetab__icontains=recherche) |
                Q(libelle__icontains=recherche) |
                # Q(is_active = recherche) |
                Q(date_deb_saisie__icontains=recherche) |
                Q(date_fin_saisie__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            
    periode_saisies_serializers = LesDivisionTempsSousEtabSerializer(periode_saisies, many=True)

    return periode_saisies_serializers.data

def recherche_etudiant(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            etudiants = find_etudiant(donnees_recherche,trier_par)


            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(etudiants)

            form = EtudiantForm
            paginator = Paginator(etudiants, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "etudiants": etudiants,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
        
def find_etudiant(recherche, trier_par):
    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            etudiants = Etudiant.objects.order_by('-id')
        else:
            etudiants = Etudiant.objects.order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            etudiants = Etudiant.objects.filter(Q(archived ="0") &  
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(age__icontains=recherche))
            ).distinct()

        else:

            etudiants = Etudiant.objects.filter(Q(archived ="0") &  
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(age__icontains=recherche))
            ).distinct().order_by(trier_par)

    etudiants_serializers = EtudiantSerializer(etudiants, many=True)

    return etudiants_serializers.data

def recherche_etablissement(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            etablissements = find_etablissement(donnees_recherche,trier_par)


            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(etablissements)

            #form = EtudiantForm
            paginator = Paginator(etablissements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "etablissements": etablissements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def recherche_eleve(request):
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            # tailles_donnees = 5 si on veut voir les payements pour une classe
            tailles_donnees = len(donnees)

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            # if tailles_donnees == 4:
            #     eleves = find_eleve(donnees_recherche,trier_par,"1")
            # else:
            eleves, montant_a_payer = find_eleve(donnees_recherche,trier_par,donnees[4])

            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(eleves)

            #form = EtudiantForm
            paginator = Paginator(eleves, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "eleves": eleves,
                "montant_a_payer": montant_a_payer,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

            return JSONResponse(data) 

def find_eleve(recherche, trier_par, classe_recherchee):
    
    classe, id_classe = classe_recherchee.split("_")
    id_classe = int(id_classe)
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            eleves = Eleve.objects.filter(archived = "0", id_classe_actuelle = id_classe).order_by('matricule')
        else:
            eleves = Eleve.objects.filter(archived = "0", id_classe_actuelle = id_classe).order_by(trier_par)

    else:
        if (trier_par == "non defini"):
            # Q(archived ="0") &
            eleves = Eleve.objects.filter(Q(archived ="0") & Q(id_classe_actuelle = id_classe) &
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(sexe__icontains=recherche)|
                Q(redouble__icontains=recherche)|
                Q(date_naissance__icontains=recherche) |
                Q(lieu_naissance__icontains=recherche) |
                Q(date_entree__icontains=recherche) |
                Q(nom_pere__icontains=recherche)|
                Q(prenom_pere__icontains=recherche)|
                Q(nom_mere__icontains=recherche)|
                Q(prenom_mere__icontains=recherche)|
                Q(tel_pere__icontains=recherche)|
                Q(tel_mere__icontains=recherche)|
                Q(email_pere__icontains=recherche)|
                Q(classe_actuelle__icontains=recherche)|
                Q(email_mere__icontains=recherche))
            ).distinct()

        else:

            eleves = Eleve.objects.filter(Q(archived ="0") & Q(id_classe_actuelle = id_classe) &
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(sexe__icontains=recherche)|
                Q(redouble__icontains=recherche)|
                Q(date_naissance__icontains=recherche) |
                Q(lieu_naissance__icontains=recherche) |
                Q(date_entree__icontains=recherche) |
                Q(nom_pere__icontains=recherche)|
                Q(prenom_pere__icontains=recherche)|
                Q(nom_mere__icontains=recherche)|
                Q(prenom_mere__icontains=recherche)|
                Q(tel_pere__icontains=recherche)|
                Q(tel_mere__icontains=recherche)|
                Q(email_pere__icontains=recherche)|
                Q(classe_actuelle__icontains=recherche)|
                Q(email_mere__icontains=recherche))
            ).distinct().order_by(trier_par)
    montant_a_payer = 0
    classe_courante = str(id_classe)+"_"+classe+"_"
    tranches = TypePayementEleve.objects.values('id','libelle','montant','ordre_paiement').filter(liste_classes__icontains = classe_courante, entree_sortie_caisee = "e")
    tranches_paiements = ""
    for t in tranches:
        montant_a_payer += t['montant']
        tranches_paiements += str(t['id'])+"²²"+t['libelle']+"²²"+str(t['montant'])+"²²"+str(t['ordre_paiement'])+"*²*"


    eleves_serializers = EleveSerializer(eleves, many=True)

    return eleves_serializers.data, montant_a_payer

def recherche_boursier(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            tailles_donnees = len(donnees)

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            bourses = find_boursier(donnees_recherche,trier_par)

            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(eleves)

            #form = EtudiantForm
            paginator = Paginator(bourses, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "bourses": bourses,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_boursier(recherche, trier_par):
    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            bourses = Eleve.objects.filter(~Q(liste_bourses = ""), archived = "0").order_by('matricule')
        else:
            bourses = Eleve.objects.filter(~Q(liste_bourses = ""), archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):
            # Q(archived ="0") &
            bourses = Eleve.objects.filter(~Q(liste_bourses = "") & Q(archived ="0") &
                (Q(matricule__icontains = recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(sexe__icontains=recherche) |
                Q(classe_actuelle__icontains=recherche)|
                Q(liste_bourses_afficher__icontains=recherche))
            ).distinct()

        else:

            bourses = Eleve.objects.filter(~Q(liste_bourses = "") & Q(archived ="0") &
                (Q(matricule__icontains = recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(sexe__icontains=recherche) |
                Q(classe_actuelle__icontains=recherche)|
                Q(liste_bourses_afficher__icontains=recherche))
            ).distinct().order_by(trier_par)

    eleves_serializers = BoursierSerializer(bourses, many=True)

    return eleves_serializers.data

def find_etablissement(recherche, trier_par):
    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            etablissements = Etab.objects.order_by('-id')
        else:
            etablissements = Etab.objects.order_by(trier_par)

    else:
        if (trier_par == "non defini"):
            # Q(archived ="0") &
            etablissements = Etab.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(date_creation__icontains=recherche) |
                Q(nom_fondateur__icontains=recherche) |
                Q(localisation__icontains=recherche)|
                Q(bp__icontains=recherche) |
                Q(email__icontains=recherche) |
                Q(tel__icontains=recherche) |
                Q(devise__icontains=recherche)|
                Q(langue__icontains=recherche))
            ).distinct()

        else:

            etablissements = Etab.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(date_creation__icontains=recherche) |
                Q(nom_fondateur__icontains=recherche) |
                Q(localisation__icontains=recherche)|
                Q(bp__icontains=recherche) |
                Q(email__icontains=recherche) |
                Q(tel__icontains=recherche) |
                Q(devise__icontains=recherche)|
                Q(langue__icontains=recherche))
            ).distinct().order_by(trier_par)

    etablissements_serializers = EtabSerializer(etablissements, many=True)

    return etablissements_serializers.data

def recherche_sous_etablissement(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            s_etablissements = find_sous_etablissement(donnees_recherche,trier_par)


            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(s_etablissements)

            #form = EtudiantForm
            paginator = Paginator(s_etablissements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "s_etablissements": s_etablissements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
        
def find_sous_etablissement(recherche, trier_par):
    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            sous_etablissements = SousEtab.objects.order_by('-id')
        else:
            sous_etablissements = SousEtab.objects.order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            sous_etablissements = SousEtab.objects.filter(Q(archived ="0") &  
                (Q(nom_sousetab__icontains=recherche) |
                Q(date_creation__icontains=recherche) |
                Q(nom_fondateur__icontains=recherche) |
                Q(localisation__icontains=recherche))
            ).distinct()

        else:

            sous_etablissements = SousEtab.objects.filter(Q(archived ="0") &  
                (Q(nom_sousetab__icontains=recherche) |
                Q(date_creation__icontains=recherche) |
                Q(nom_fondateur__icontains=recherche) |
                Q(localisation__icontains=recherche))
            ).distinct().order_by(trier_par)

    sous_etablissements_serializers = SousEtabSerializer(sous_etablissements, many=True)

    return sous_etablissements_serializers.data

def recherche_cycle(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            cycles = find_cycle(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(cycles)

            #form = EtudiantForm
            paginator = Paginator(cycles, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "cycles": cycles,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_cycle(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            cycles = Cycle.objects.filter(archived = "0").order_by('-id')
        else:
            cycles = Cycle.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            cycles = Cycle.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche)
                )
            ).distinct()

        else:
            cycles = Cycle.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            
    cycles_serializers = CycleSerializer(cycles, many=True)

    return cycles_serializers.data

def recherche_niveau(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            niveaux = find_niveau(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(niveaux)

            #form = EtudiantForm
            paginator = Paginator(niveaux, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "niveaux": niveaux,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_niveau(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            niveaux = Niveau.objects.filter(archived = "0").order_by('-id')
        else:
            niveaux = Niveau.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            niveaux = Niveau.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) |
                Q(nom_niveau__icontains=recherche)
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            niveaux = Niveau.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) |
                Q(nom_niveau__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    niveaux_serializers = NiveauSerializer(niveaux, many=True)

    return niveaux_serializers.data

def recherche_classe(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            classes = find_classe(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(classes)

            #form = EtudiantForm
            paginator = Paginator(classes, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            #gestion de la description textuelle de la pagination
            nbre_item = len(classes)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

            if (nbre_item - first_item_page < nbre_element_par_page):
                last_item_page = first_item_page + (nbre_item - first_item_page)
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page


            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "classes": classes,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

           
            return JSONResponse(data) 

def find_classe(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            classes = Classe.objects.filter(archived = "0").order_by('-nom_classe')
        else:
            classes = Classe.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            classes = Classe.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(specialite__icontains=recherche) |
                Q(nom_classe__icontains=recherche)
                )
            ).distinct()

        else:
            
            classes = Classe.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(specialite__icontains=recherche) |
                Q(nom_classe__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    classes_serializers = ClasseSerializer(classes, many=True)

    return classes_serializers.data


def recherche_eleves_salle_de_classe(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            salle_de_classe_id = donnees[4]

            sousetab_id = donnees[5]

            annee_scolaire = donnees[6]

            
            eleves = find_eleves_salle_de_classe(donnees_recherche,trier_par,salle_de_classe_id,sousetab_id,annee_scolaire)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(classes)

            paginator = Paginator(eleves, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            #gestion de la description textuelle de la pagination
            nbre_item = len(eleves)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

            if (nbre_item - first_item_page < nbre_element_par_page):
                last_item_page = first_item_page + (nbre_item - first_item_page)
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page


            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "eleves": eleves,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

           
            return JSONResponse(data) 

def find_eleves_salle_de_classe(recherche, trier_par, salle_de_classe_id, sousetab_id, annee_scolaire):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            eleves = Cours.objects.filter(id_classe = salle_de_classe_id, id_sousetab=sousetab_id, annee_scolaire = annee_scolaire)[0].eleves.all().filter(Q(archived ="0")).order_by("nom")

        else:
            eleves = Cours.objects.filter(id_classe = salle_de_classe_id, id_sousetab=sousetab_id, annee_scolaire = annee_scolaire)[0].eleves.all().filter(Q(archived ="0")).order_by(trier_par)
            
    else:
        if (trier_par == "non defini"):

            eleves = Cours.objects.filter(id_classe = salle_de_classe_id, id_sousetab=sousetab_id, annee_scolaire = annee_scolaire)[0].eleves.all().filter(Q(archived ="0") &
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(adresse__icontains=recherche) |
                Q(sexe__icontains=recherche) |
                Q(date_naissance__icontains=recherche) |
                Q(lieu_naissance__icontains=recherche) |
                Q(date_entree__icontains=recherche) |
                Q(nom_pere__icontains=recherche) |
                Q(prenom_pere__icontains=recherche) |
                Q(nom_mere__icontains=recherche) |
                Q(prenom_mere__icontains=recherche) |
                Q(tel_pere__icontains=recherche) |
                Q(email_pere__icontains=recherche) |
                Q(tel_mere__icontains=recherche) |
                Q(email_mere__icontains=recherche) |
                Q(redouble__icontains=recherche)
                )
            ).distinct().order_by("nom")

        else:
           
            eleves = Cours.objects.filter(id_classe = salle_de_classe_id, id_sousetab=sousetab_id, annee_scolaire = annee_scolaire)[0].eleves.all().filter(Q(archived ="0") &
                (Q(matricule__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(adresse__icontains=recherche) |
                Q(sexe__icontains=recherche) |
                Q(date_naissance__icontains=recherche) |
                Q(lieu_naissance__icontains=recherche) |
                Q(date_entree__icontains=recherche) |
                Q(nom_pere__icontains=recherche) |
                Q(prenom_pere__icontains=recherche) |
                Q(nom_mere__icontains=recherche) |
                Q(prenom_mere__icontains=recherche) |
                Q(tel_pere__icontains=recherche) |
                Q(email_pere__icontains=recherche) |
                Q(tel_mere__icontains=recherche) |
                Q(email_mere__icontains=recherche) |
                Q(redouble__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    eleves_serializers = EleveSerializer(eleves, many=True)

    return eleves_serializers.data

def recherche_specialite(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            specialites = find_specialite(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(specialites)

            #form = EtudiantForm
            paginator = Paginator(specialites, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            #gestion de la description textuelle de la pagination
            nbre_item = len(specialites)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

            if (nbre_item - first_item_page < nbre_element_par_page):
                last_item_page = first_item_page + (nbre_item - first_item_page)
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page


            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "specialites": specialites,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

           
            return JSONResponse(data) 

def find_specialite(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            specialites = Specialite.objects.values('id','specialite','nom_etab','nom_sousetab').filter(archived = "0").order_by('-specialite').distinct()
        else:
            specialites = Specialite.objects.values('id','specialite','nom_etab','nom_sousetab').filter(archived = "0").order_by(trier_par).distinct()

    else:
        if (trier_par == "non defini"):

            specialites = Specialite.objects.values('id','specialite','nom_etab','nom_sousetab').filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(specialite__icontains=recherche)
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            specialites = Specialite.values('id','specialite','nom_etab','nom_sousetab').objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(specialite__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    specialites_serializers = SpecialiteSerializer(specialites, many=True)

    return specialites_serializers.data

def recherche_classe_specialite(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            print("DANS RECHERCHE DEBUT")

            
            classes = find_classe_specialite(donnees_recherche,trier_par)

            print("DANS RECHERCHE FIN")

            [print(classe) for classe in classes]
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(classes)

            #form = EtudiantForm
            paginator = Paginator(classes, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            #gestion de la description textuelle de la pagination
            nbre_item = len(classes)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

            if (nbre_item - first_item_page < nbre_element_par_page):
                last_item_page = first_item_page + (nbre_item - first_item_page)
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page


            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "classes": classes,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

            print("AVANT DE BACK AU JS")

           
            return JSONResponse(data) 

def find_classe_specialite(recherche, trier_par):
    classes = []
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            classes = Specialite.objects.\
            values('id_niveau','nom_etab','nom_sousetab','liste_classes_afficher','nom_niveau','specialite','liste_classes')\
            .filter(~Q(nom_niveau=""),archived = "0").distinct().order_by('-specialite')
        else:
            classes = Specialite.objects.\
            values('id_niveau','nom_etab','nom_sousetab','liste_classes_afficher','nom_niveau','specialite','liste_classes')\
            .filter(~Q(nom_niveau=""),archived = "0").distinct().order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            classes = Specialite.objects.\
            values('id_niveau','nom_etab','nom_sousetab','liste_classes_afficher','nom_niveau','specialite','liste_classes')\
            .filter(~Q(nom_niveau=""),Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(liste_classes_afficher__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(specialite__icontains=recherche)
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            classes = Specialite.objects.\
            values('id_niveau','nom_etab','nom_sousetab','liste_classes_afficher','nom_niveau','specialite','liste_classes')\
            .filter(~Q(nom_niveau=""),Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(liste_classes_afficher__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(specialite__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            
    print("ON VOIT UN PEUT:")
    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    classes_serializers = ClasseSpecialiteSerializer(classes, many=True)
    print("APRES LE SERIALIZER")

    return classes_serializers.data

def recherche_sousetab(request):

    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            sousetabs = find_sousetab(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(sousetabs)

            #form = EtudiantForm
            paginator = Paginator(sousetabs, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            #gestion de la description textuelle de la pagination

            nbre_item = len(sousetabs)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1
 
            if(int(page_active.number)-1 != 0):
                last_item_page = first_item_page + len(list(paginator.page_range)) -1
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page


            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {

                "sousetabs": sousetabs,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

            return JSONResponse(data) 

def find_sousetab(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            sousetabs = SousEtab.objects.filter(archived = "0").order_by('-nom_sousetab')
        else:
            sousetabs = SousEtab.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

                # cours = Cours.objects.filter(Q(archived ="0") &
                # (Q(code_matiere__icontains=recherche) |
                # Q(nom_matiere__icontains=recherche) |
                # Q(coef__icontains=recherche) |
                # Q(nom_classe__icontains=recherche) |
                # Q(volume_horaire_hebdo__icontains=recherche) |
                # Q(volume_horaire_annuel__icontains=recherche) |
                # Q(nom_etab__icontains=recherche) |
                # Q(nom_sousetab__icontains=recherche) |
                # Q(nom_cycle__icontains=recherche)

            sousetabs = SousEtab.objects.filter(Q(archived ="0") &
                (Q(nom_sousetab__icontains=recherche) |
                Q(format_matricule__icontains=recherche)
                )
            ).distinct()

        else:
        
            # cours = Cours.objects.filter(Q(archived ="0") &
            #     (Q(code_matiere__icontains=recherche) |
            #     Q(nom_matiere__icontains=recherche) |
            #     Q(coef__icontains=recherche) |
            #     Q(nom_classe__icontains=recherche) |
            #     Q(volume_horaire_hebdo__icontains=recherche) |
            #     Q(volume_horaire_annuel__icontains=recherche) |
            #     Q(nom_etab__icontains=recherche) |
            #     Q(nom_sousetab__icontains=recherche) |
            #     Q(nom_cycle__icontains=recherche) 

            print("*******recherche ",recherche)
            sousetabs = SousEtab.objects.filter(Q(archived ="0") &
                (Q(nom_sousetab__icontains=recherche) |
                Q(format_matricule__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)

    # cours_serializers = CoursSerializer(cours, many=True)

    # return classes_serializers.data

    sousetabs_serializers = SousEtabConfigSerializer(sousetabs, many=True)

    return sousetabs_serializers.data

def recherche_matiere(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            matieres = find_matiere(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(matieres)

            #form = EtudiantForm
            paginator = Paginator(matieres, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "matieres": matieres,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_matiere(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            matieres = Matiere.objects.filter(archived = "0").order_by('-id')
        else:
            matieres = Matiere.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            matieres = Matiere.objects.filter(Q(archived ="0") &
                (Q(code__icontains=recherche) |
                Q(nom_matiere__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            matieres = Matiere.objects.filter(Q(archived ="0") &
                (Q(code__icontains=recherche) |
                Q(nom_matiere__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    matieres_serializers = MatiereSerializer(matieres, many=True)

    return matieres_serializers.data

def recherche_cours(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            cours = find_cours(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(cours)

            #form = EtudiantForm
            paginator = Paginator(cours, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)


            #gestion de la description textuelle de la pagination
            nbre_item = len(cours)

            first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

            if (nbre_item - first_item_page < nbre_element_par_page):
                last_item_page = first_item_page + (nbre_item - first_item_page)
            else:
                last_item_page = int(page_active.number) * nbre_element_par_page

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "cours": cours,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
                "nbre_item" : nbre_item,
                "first_item_page" : first_item_page,
                "last_item_page" : last_item_page,
            }

           
            return JSONResponse(data) 

def find_cours(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            cours = Cours.objects.filter(archived = "0").order_by('code_matiere')
        else:
            cours = Cours.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            cours = Cours.objects.filter(Q(archived ="0") &
                (Q(code_matiere__icontains=recherche) |
                Q(nom_matiere__icontains=recherche) |
                Q(coef__icontains=recherche) |
                Q(volume_horaire_hebdo__icontains=recherche) |
                Q(volume_horaire_annuel__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_etab__icontains=recherche) |
                Q(nom_classe__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) 
                )
            ).distinct()

        else:
            
            cours = Cours.objects.filter(Q(archived ="0") &
                (Q(code_matiere__icontains=recherche) |
                Q(nom_matiere__icontains=recherche) |
                Q(coef__icontains=recherche) |
                Q(volume_horaire_hebdo__icontains=recherche) |
                Q(volume_horaire_annuel__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_etab__icontains=recherche) |
                Q(nom_classe__icontains=recherche) |
                Q(nom_cycle__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    cours_serializers = CoursSerializer(cours, many=True)

    return cours_serializers.data

def recherche_appellation_apprenant_formateur(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            appellations = find_appellation_apprenant_formateur(donnees_recherche,trier_par)
            # print("appellations: ", appellations.count())
            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(matieres)

            #form = EtudiantForm
            paginator = Paginator(appellations, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "appellations": appellations,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_appellation_apprenant_formateur(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            appellations = AppellationApprenantFormateur.objects.filter(archived = "0").order_by('-id')
        else:
            appellations = AppellationApprenantFormateur.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            appellations = AppellationApprenantFormateur.objects.filter(Q(archived ="0") &
                (Q(appellation_apprenant__icontains=recherche) |
                Q(appellation_formateur__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            appellations = AppellationApprenantFormateur.objects.filter(Q(archived ="0") &
                (Q(appellation_apprenant__icontains=recherche) |
                Q(appellation_formateur__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    appellations_serializers = AppellationApprenantFormateurSerializer(appellations, many=True)

    return appellations_serializers.data

def recherche_type_apprenant(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            type_apprenants = find_type_apprenant(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(type_apprenants)

            #form = EtudiantForm
            paginator = Paginator(type_apprenants, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "type_apprenants": type_apprenants,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_apprenant(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            type_apprenants = TypeApprenant.objects.filter(archived = "0").order_by('-id')
        else:
            type_apprenants = TypeApprenant.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            type_apprenants = TypeApprenant.objects.filter(Q(archived ="0") &
                (Q(nom_type_apprenant__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            type_apprenants = TypeApprenant.objects.filter(Q(archived ="0") &
                (Q(nom_type_apprenant__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    type_apprenants_serializers = TypeApprenantSerializer(type_apprenants, many=True)

    return type_apprenants_serializers.data

def recherche_discipline(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            disciplines = find_discipline(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(disciplines)

            #form = EtudiantForm
            paginator = Paginator(disciplines, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "disciplines": disciplines,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_discipline(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            disciplines = Discipline.objects.filter(archived = "0").order_by('-id')
        else:
            disciplines = Discipline.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            disciplines = Discipline.objects.filter(Q(archived ="0") &
                (Q(fait__icontains=recherche) |
                Q(description__icontains=recherche) |
                Q(nb_heures_min__icontains=recherche) |
                Q(nb_heures_max__icontains=recherche) |
                Q(sanction__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            disciplines = Discipline.objects.filter(Q(archived ="0") &
                (Q(fait__icontains=recherche) |
                Q(description__icontains=recherche) |
                Q(nb_heures_min__icontains=recherche) |
                Q(nb_heures_max__icontains=recherche) |
                Q(sanction__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    disciplines_serializers = DisciplineSerializer(disciplines, many=True)

    return disciplines_serializers.data

def recherche_type_paiement_eleve(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            # print("taille des données: ", len(donnees))
            # tailles_donnees = 5 si on veut voir les payements pour une classe
            tailles_donnees = len(donnees)

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            if tailles_donnees == 4:
                paiements = find_type_paiement_eleve(donnees_recherche,trier_par,"1")
            else:
                paiements = find_type_paiement_eleve(donnees_recherche,trier_par,donnees[4])


            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_eleve(recherche, trier_par, classe_recherchee):

    if classe_recherchee == "1":
        if recherche == "" or not recherche:
            if (trier_par == "non defini"):
                paiements = TypePayementEleve.objects.filter(archived = "0", entree_sortie_caisee = "e").order_by('-id')
            else:
                paiements = TypePayementEleve.objects.filter(archived = "0", entree_sortie_caisee = "e").order_by(trier_par)

        else:
            if (trier_par == "non defini"):

                paiements = TypePayementEleve.objects.filter(Q(archived ="0") &
                    (Q(entree_sortie_caisee="e") |
                    Q(libelle__icontains=recherche) |
                    Q(date_deb__icontains=recherche) |
                    Q(date_fin__icontains=recherche) |
                    Q(liste_classes_afficher__icontains=recherche) |
                    Q(entree_sortie_caisee__icontains=recherche) |
                    Q(montant__icontains=recherche) 
                    )
                ).distinct()

            else:
                print("*******recherche ",recherche)
                paiements = TypePayementEleve.objects.filter(Q(archived ="0") &
                    (Q(entree_sortie_caisee="e") |
                    Q(libelle__icontains=recherche) |
                    Q(date_deb__icontains=recherche) |
                    Q(date_fin__icontains=recherche) |
                    Q(liste_classes_afficher__icontains=recherche) |
                    Q(entree_sortie_caisee__icontains=recherche) |
                    Q(montant__icontains=recherche)
                    )
                ).distinct().order_by(trier_par)
    else:
        id_etab, id_sousetab, id_cycle, id_niveau = 0, 0, 0, 0
        info = classe_recherchee.split("_")
        print("classe_recherchee: ", classe_recherchee)
        if len(info) == 2:
            print("len == 2")
            if info[0] == "tous":
                paiements = TypePayementEleve.objects.values('ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(archived ="0", entree_sortie_caisee = "e")
            else:
                classe_recherchee = info[1]+"_"+info[0]+"_"
                # id = int(info[1])
                # print(Classe.objects.values('id_sousetab','id_cycle','id_niveau').filter(pk = id))
                # print(Cycle.objects.filter(pk = 1)[0].niveaux.filter()[0].classes.values('id_sousetab','id_cycle','id_niveau').filter()[0])
                paiements = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(Q(archived ="0") &
                        (Q(entree_sortie_caisee="e")&
                        Q(liste_classes__icontains=classe_recherchee)
                        )
                    ).order_by('ordre_paiement')
        else:
            paiements = []
            if info[0] == "etab":
                id_etab = int(info[2])
                paiements = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes', 'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee'
                    ).filter(archived = "0", id_etab = id_etab,
                    entree_sortie_caisee="e").order_by('ordre_paiement')
                for l in paiements:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
            elif info[0] == "sousetab":
                id_sousetab = int(info[2])
                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(Q(archived="0") & Q(id_sousetab = id_sousetab))
                for l in liste_classes:
                    print("for")
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                    #     else:
                    #         l['liste_classes_afficher'] = l['liste_classes_afficher']
                    # else:
                    #     l['liste_classes_afficher'] = l['liste_classes_afficher']
                    paiements.append(l)
                # if liste_classes.count()>0:
                #     id_etab = liste_classes[0]['id_etab']

                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(
                    ~Q(id_etab = 0) & Q(archived="0") & Q(id_sousetab = 0) & Q(id_cycle = 0) & Q(id_niveau = 0))
                for l in liste_classes:
                    paiements.append(l)

            elif info[0] == "cycle":
                id_cycle = int(info[2])
                data = Cycle.objects.filter(pk = id_cycle)[0].niveaux.filter()[0].classes.values('id_sousetab','id_etab').filter()[0]
                id_sousetab = data['id_sousetab']
                id_etab = data['id_etab']

                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(
                    Q(archived="0") & Q(id_cycle = id_cycle) & Q(id_niveau = 0))
                for l in liste_classes:
                    print("ici__")
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                        
                    paiements.append(l)
                
                liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                    'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter( 
                    ((Q(id_etab = id_etab) & Q(id_sousetab = 0) & Q(archived="0")  & Q(id_cycle = 0) & Q(id_niveau = 0))|
                     (Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(archived="0") & Q(id_cycle = 0) & Q(id_niveau = 0)))
                    )#.order_by('-id_sousetab')
                for l in liste_classes:
                    if l['indicateur_liste_classes']!= "classe":
                        if "_aucune_" in l['indicateur_liste_classes']:
                            l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                    paiements.append(l)
            else:
                if info[0] == "niveau":
                    id_niveau = int(info[2])
                    data = Niveau.objects.filter(pk = id_niveau)[0].classes.values('id_sousetab','id_etab','id_cycle').filter()[0]
                    id_sousetab = data['id_sousetab']
                    id_etab = data['id_etab']
                    id_cycle = data['id_cycle']
                    liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                        'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(Q(archived="0") & Q(id_niveau = id_niveau))
                    for l in liste_classes:
                        if l['indicateur_liste_classes']!= "classe":
                            if "_aucune_" in l['indicateur_liste_classes']:
                                l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                            
                        paiements.append(l)

                    liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                        'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(
                        ((Q(id_etab = id_etab) & Q(id_sousetab = 0) & Q(archived="0")  & Q(id_cycle = 0) & Q(id_niveau = 0))|
                         (Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(archived="0") & Q(id_cycle = 0) & Q(id_niveau = 0))|
                         (Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(archived="0") & Q(id_niveau = 0))
                         ))
                    for l in liste_classes:
                        ind_liste_cl = l['liste_classes_afficher']
                        paiements.append(l)

                elif info[0] == "specialite":
                    id_niveau = int(info[2])
                    data = Niveau.objects.filter(pk = id_niveau)[0].classes.values('id_sousetab','id_etab','id_cycle').filter()[0]
                    id_sousetab = data['id_sousetab']
                    id_etab = data['id_etab']
                    id_cycle = data['id_cycle']
                    liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                        'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(Q(archived="0") & Q(id_niveau = id_niveau) &
                        Q(indicateur_liste_classes= classe_recherchee))
                    for l in liste_classes:
                        if l['indicateur_liste_classes']!= "classe":
                            if "_aucune_" in l['indicateur_liste_classes']:
                                    l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                        paiements.append(l)
                    liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                        'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(
                        ((Q(id_etab = id_etab) & Q(id_sousetab = 0) & Q(archived="0")  & Q(id_cycle = 0) & Q(id_niveau = 0))|
                         (Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(archived="0") & Q(id_cycle = 0) & Q(id_niveau = 0))|
                         (Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(archived="0") & Q(id_niveau = 0)) |
                         (~Q(niveau = "") & Q(indicateur_liste_classes__icontains= "niveau") & Q(id_etab = id_etab) & Q(id_sousetab = id_sousetab) & Q(id_cycle = id_cycle) & Q(archived="0") & Q(id_niveau = id_niveau))
                         
                         ))
                    for l in liste_classes:
                        ind_liste_cl = l['liste_classes_afficher']
                        if l not in paiements:
                            paiements.append(l)

                    liste_classes = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                        'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(archived = "0", id_niveau = id_niveau, indicateur_liste_classes = classe_recherchee, entree_sortie_caisee ="e")
                    for lc in liste_classes:
                        current = lc['liste_classes'].split("_")
                        id_des_classes = current[0:][::2]
                        les_classes = current[1:][::2]

                        id_des_classes.pop(len(id_des_classes) - 1)
                        i = 0
                        # classes_selectionnees = []
                        for j in les_classes:
                            # classes_selectionnees.append(id_des_classes[i]+"_"+j+"_")
                            cl = id_des_classes[i]+"_"+j+"_"
                            ligne = TypePayementEleve.objects.values('niveau','ordre_paiement','liste_classes_afficher','liste_classes',
                            'libelle','date_deb','date_fin','montant','indicateur_liste_classes','entree_sortie_caisee').filter(Q(archived ="0") &
                                (Q(entree_sortie_caisee="e")&
                                Q(liste_classes__icontains=cl)
                                )
                            )

                            for l in ligne:
                                if l['indicateur_liste_classes']!= "classe":
                                    if "_aucune_" in l['indicateur_liste_classes']:
                                        l['liste_classes_afficher'] = l['niveau']+" "+"sans spécialité"
                                if l not in paiements:
                                    paiements.append(l)
                            i += 1


                  
            paiements = sorted(paiements, key=lambda k: k['ordre_paiement'])

    paiements_serializers = TypePayementEleveSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_pers_administratif(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_pers_administratif(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_pers_administratif(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Pers Administratif").order_by('-id')
        else:
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Pers Administratif").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Pers Administratif") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Pers Administratif") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    paiements_serializers = TypePayementPersAdministratifSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_pers_enseignant(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_pers_enseignant(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_pers_enseignant(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Enseignant").order_by('-id')
        else:
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Enseignant").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Enseignant") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Enseignant") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    paiements_serializers = TypePayementPersAdministratifSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_pers_appui(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_pers_appui(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_pers_appui(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Pers Appui").order_by('-id')
        else:
            paiements = TypePayementAdminStaff.objects.filter(archived = "0", type_payement ="Pers Appui").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Pers Appui") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementAdminStaff.objects.filter(Q(archived ="0") & Q(type_payement ="Pers Appui") &
                (Q(libelle__icontains=recherche) |
                Q(type_payement__icontains=recherche) |
                Q(person__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    paiements_serializers = TypePayementPersAdministratifSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_divers(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_divers(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_divers(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Divers").order_by('-id')
        else:
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Divers").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Divers") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Divers") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

    paiements_serializers = TypePayementDiversSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_cantine(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_cantine(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_cantine(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Cantine").order_by('-id')
        else:
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Cantine").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Cantine") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Cantine") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

    paiements_serializers = TypePayementDiversSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_transport(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_transport(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_transport(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Transport").order_by('-id')
        else:
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Transport").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Transport") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Transport") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

    paiements_serializers = TypePayementDiversSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_dortoir(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_dortoir(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_dortoir(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Dortoir").order_by('-id')
        else:
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Dortoir").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Dortoir") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Dortoir") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

    paiements_serializers = TypePayementDiversSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_type_paiement_facture(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            paiements = find_type_paiement_facture(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(paiements)

            #form = EtudiantForm
            paginator = Paginator(paiements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "paiements": paiements,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_type_paiement_facture(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Facture").order_by('-id')
        else:
            paiements = TypePayementDivers.objects.filter(archived = "0", type_payement ="Facture").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Facture") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            paiements = TypePayementDivers.objects.filter(Q(archived ="0") & Q(type_payement ="Facture") &
                (Q(libelle__icontains=recherche) |
                Q(date_deb__icontains=recherche) |
                Q(date_fin__icontains=recherche) |
                Q(entree_sortie_caisee__icontains=recherche) |
                Q(montant__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

    paiements_serializers = TypePayementDiversSerializer(paiements, many=True)

    return paiements_serializers.data

def recherche_condition_renvoi(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            c_renvois = find_condition_renvoi(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(c_renvois)

            #form = EtudiantForm
            paginator = Paginator(c_renvois, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "c_renvois": c_renvois,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_condition_renvoi(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            c_renvois = ConditionRenvoi.objects.filter(archived = "0").order_by('-id')
        else:
            c_renvois = ConditionRenvoi.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            c_renvois = ConditionRenvoi.objects.filter(Q(archived ="0") &
                (Q(nb_heures_max__icontains=recherche) |
                Q(age__icontains=recherche) |
                Q(moyenne__icontains=recherche) |
                Q(nb_jours__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            c_renvois = ConditionRenvoi.objects.filter(Q(archived ="0") &
                (Q(nb_heures_max__icontains=recherche) |
                Q(age__icontains=recherche) |
                Q(moyenne__icontains=recherche) |
                Q(nb_jours__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    c_renvois_serializers = ConditionRenvoiSerializer(c_renvois, many=True)

    return c_renvois_serializers.data

def recherche_condition_succes(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            
            c_success = find_condition_succes(donnees_recherche,trier_par)

            
            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(c_success)

            #form = EtudiantForm
            paginator = Paginator(c_success, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "c_success": c_success,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data) 

def find_condition_succes(recherche, trier_par):

    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            c_succes = ConditionSucces.objects.filter(archived = "0").order_by('-id')
        else:
            c_succes = ConditionSucces.objects.filter(archived = "0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            c_succes = ConditionSucces.objects.filter(Q(archived ="0") &
                (Q(moyenne__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            c_succes = ConditionSucces.objects.filter(Q(archived ="0") &
                (Q(moyenne__icontains=recherche) |
                Q(nom_niveau__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) 
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    c_succes_serializers = ConditionSuccesSerializer(c_succes, many=True)

    return c_succes_serializers.data

def recherche_profil(request):
    
    if (request.method == 'POST'):
        if(request.is_ajax()):


            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")

            donnees_recherche = donnees[0]
            page = donnees[1]

            nbre_element_par_page = int(donnees[2])

            trier_par = donnees[3]

            profils = find_profil(donnees_recherche,trier_par)


            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(profils)

            form = ProfilForm
            paginator = Paginator(profils, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

            try:
                # La définition de nos URL autorise comme argument « page » uniquement 
                # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
                page_active = paginator.page(page)
            except PageNotAnInteger:
                page_active = paginator.page(1)
            except EmptyPage:
                # Nous vérifions toutefois que nous ne dépassons pas la limite de page
                # Par convention, nous renvoyons la dernière page dans ce cas
                page_active = paginator.page(paginator.num_pages)

            liste_page = list(paginator.page_range)
            numero_page_active =  page_active.number

            page_prec = numero_page_active - 1
            page_suiv = numero_page_active + 1

            #recherche l'existence de la page precedente
            if (page_prec in liste_page):
                possede_page_precedente = True
                page_precedente = page_prec
            else:
                possede_page_precedente = False
                page_precedente = 0
            
            #recherche l'existence de la page suivante
            if (page_suiv in liste_page):
                possede_page_suivante = True
                page_suivante = page_suiv
            else:
                possede_page_suivante = False
                page_suivante = 0
            
            # necessaire a cause du fait que l'objet profil contient un objet user
            profils_serializers = ProfilSerializer(profils, many=True)
            profils = json.dumps(profils_serializers.data)


            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default


            data = {
                "profils": profils,
                "message_resultat":"",
                "numero_page_active" : int(numero_page_active),
                "liste_page" : liste_page,
                "possede_page_precedente" : possede_page_precedente,
                "page_precedente" : page_precedente,
                "possede_page_suivante" : possede_page_suivante,
                "page_suivante" : page_suivante,
                "nbre_element_par_page" : nbre_element_par_page,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,                
            }


            return JSONResponse(data)

def find_profil(recherche, trier_par):
    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            profils = Profil.objects.filter(archived="0").order_by('-id')
        else:
            profils = Profil.objects.filter(archived="0").order_by(trier_par)

    else:
        if (trier_par == "non defini"):

            profils = Profil.objects.filter(Q(archived ="0") &  
                (Q(user__last_name__icontains=recherche) |
                Q(user__first_name__icontains=recherche) |
                Q(user__username__icontains=recherche) |
                Q(user__is_active__icontains=recherche) |
                
                Q(telephone__icontains=recherche) |
                Q(ville__icontains=recherche) |
                Q(quartier__icontains=recherche))
            ).distinct()

        else:

            profils = Profil.objects.filter(Q(archived ="0") & 
                (Q(user__last_name__icontains=recherche) |
                Q(user__first_name__icontains=recherche) |
                Q(user__username__icontains=recherche) |
                Q(user__is_active__icontains=recherche) |
                
                Q(telephone__icontains=recherche) |
                Q(ville__icontains=recherche) |
                Q(quartier__icontains=recherche))
            ).distinct().order_by(trier_par)

    profils_serializers = ProfilSerializer(profils, many=True)

    return profils_serializers.data

def login_user(request):

    if request.POST:
        status = False
        user = None
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        errors = ""
        if user == None:
            print ("user is : ")
            print (user)
            errors = " pseudo ou Mot de passe incorrect !"
        else:
            login(request, user)
            print (user.password)
            status = True
            request.session['verrou']= 0
            #return status, user
            #return render(request, "mainapp/pages/liste-etudiants.html")
            return redirect('mainapp:accueil')

    return render(request, "mainapp/pages/login.html" , locals())

def deverrouiller(request):

    #from django.contrib.auth.models import User
    
    request.session['verrou'] = 0

    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    profil = Profil.objects.filter(user=request.user)
    photo_url = profil[0].photo_url

    errors = ""
    user = User.objects.get(username=username)
    if user.check_password(password):
        request.session['verrou'] = 1
        return redirect('mainapp:accueil')

    else:
        errors = " Mot de passe incorrect !"
    #user = User.objects.create_user('Gerard', 'gerardsigne@gmail.com', 'Gerard000')
    # user = User.objects.get(id=1)
    # print(user.id)
    # #print(user.first_name)
    # user.first_name, user.last_name = "Maxime", "Lorant"
    # user.is_staff = True
    # user.save()
    # print(user.first_name + " "+ user.last_name)
    
    # user = User.objects.get(username="Maxime")
    # user.set_password("coucou")    # Nous changeons le mot de passe
    # print("ancien mot de passe :" + user.password)
    # print(user.check_password("salut"))
    # print("nouveau mot de passe :" + user.password)
    
    return render(request,"mainapp/pages/deverrouiller.html" , locals())

def verrouiller(request):

    username = request.user
    #print(request.user.username)
    #gerer le cas de la connexion en tant que super user
    #parce que le super user n'a pas de profil enregistré dans la table des profils
    if request.user.is_authenticated:
        
        profil = Profil.objects.get(user=request.user)

        photo_url = profil.photo_url
        request.session['verrou'] = 1
        #print("+++++++++++")
        #print(profil.ville)

    #logout(request)

    return render(request, "mainapp/pages/deverrouiller.html", locals())

def liste_groupes(request):
    # A upgrade
    perms = ['view','change','add']
    # Just to test append
    perms.append('add')

    user = User.objects.all()

    group_list = Group.objects.all().order_by('-id')
    info_grp = []
    for grp in group_list:
        info_grp.append(groupe_permission_modification(request, grp.id, 0))
    id_max = group_list.count()


    #print('All user group: {}'.format(user.groups.all()))

    #print("___List of this group's Permissions___")
    # for p in perms:
    #     print('__ {} '.format(p.name))

    form = GroupForm(request.POST or None)
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        name = form.cleaned_data['name']
        new_group = Group()
        new_group.name=name
        # new_group.id= id_max+1
        new_group.save()
        #Group.objects.create(name=name)
        print(name)
    # Quoiqu'il arrive, on affiche la page du formulaire.
    group_list = Group.objects.all().order_by('-id')
    return render(request,'mainapp/pages/liste-groupes.html',locals())


def group_users_list(group):
    ''' Cette fonction permet de renvoyer tous les users d'un group
        Elle renvoie donc une liste
     '''
    return group.user_set.all()

# avec gestion du parametre render
def groupe_permission_modification(request, id, render = 1):

    if render == 1:
        id = request.POST["id"]
    group = Group.objects.get(id=id)
    current_grp_name = (group.name).lower()

    data = []
    ch = ''
    after_post = False
    if request.POST:
        #remove_all_perms_group(group)
        after_post = True
        for r in request.POST:
            ch = r.replace('1','')
            

            operation = ''
            if 'view' in ch:
                operation = 'view'
            elif 'change' in ch:
                operation = 'change'
            elif 'add' in ch:
                operation = 'add'
            elif 'delete' in ch:
                operation = 'delete'

            if operation != '':
                mod = ch.replace(operation,'')
                print('mod: {}'.format(mod))
                permss.append(operation)
                data.append(operation+'_'+mod)

                add_perms_group(mod,permss,group)
            permss = []

        # new_grp_name = (request.POST[group.name]).lower()
        # if current_grp_name != new_grp_name:
        #     group.name = new_grp_name
        #     group.save()

    nb = 0
    print(nb)
    # for d in data:
    #     print('data: {}'.format(d))
    if after_post:
        permsg = group_perms_list(group.name)
        # print('perms list:{}   {}'.format(len(permsg),len(data)))
        for pg in permsg:
            if pg.codename not in data:
                print('a enlever: {}'.format(pg.codename))
                #suppression permission dans le groupe
                group.permissions.remove(pg)
    permss = []
    permssall = []
    operation = ""
    incr = 0

    # creer liste de taille perms init a 0 puis 1 si trouve
    app_models = apps.get_app_config('mainapp').get_models()
    mods = []
    models = []

    # print(group.name)
    for model in app_models:
        m = str(model)
        m = m.split('models.')[1]
        mod = str(m[:len(m)-2]).lower()
        print(mod)
        # mod = str(m[23:len(m)-2]).lower()
        mods.append(mod)
    models = sorted(mods)
    # print(models)
    nb = len(models)*4
    perms = group_perms_list(group.name)
    pms = [0] *nb
    pms_values = [''] *nb
    models_list = ['']*nb
    # print('les perms')
    for p in perms:
        print(p)
    i=0
    for m in models:
        model = m.replace(' ','')
        models_list[i] = model
        models_list[i+1] = model
        models_list[i+2] = model
        models_list[i+3] = model
        pms_values[i] = 'view'
        pms_values[i+1] = 'change'
        pms_values[i+2] = 'add'
        pms_values[i+3] = 'delete'
        i+=4

    permss = ['view','change','add','delete']
    cn = ''
    j = 0
    ind = 0
    taille = len(models) -1
    for m in models:

        ind = models.index(m)

        nb_permission_par_model = 4

        for p in perms:
            print('{} : {} -- {}'.format( models.index(m),incr,m==p.codename) )
            if 'view'+'_'+m in p.codename:
                pms[ind*nb_permission_par_model + 0] = 1
            if 'change'+'_'+m in p.codename:
                pms[ind*nb_permission_par_model + 1] = 1
            if 'add'+'_'+m in p.codename:
                pms[ind*nb_permission_par_model + 2] = 1
            if 'delete'+'_'+m in p.codename:
                pms[ind*nb_permission_par_model + 3] = 1

    gpm_data = zip(pms, pms_values,models_list)

    if (render ==0):
        return gpm_data
    else:
        return redirect('mainapp:liste_groupes')

def add_perms_group(model, permss, group, app='mainapp'):
    '''Ajout de permissions à un groupe d'users sur un model donné
       permss est une liste de perms ex: ['view', 'change', 'add', 'delete']
    '''
    status = False
    content_type = ContentType.objects.get(app_label=app, model=model)

    gp = group.permissions.values_list('codename', flat=True).filter(content_type=content_type)

    lst = [x for x in gp]

    while len(permss):
        status = False
        perm_name = permss.pop()

        pn = perm_name+'_'+model
        pn2 = 'can'+'_'+perm_name+'_'+model
        if pn in lst:
            continue
        else:
            p = Permission.objects.filter(content_type=content_type).filter(codename=pn)
            # Il faudra essayer plutot la ligne suivante en commentaire
            # p = Permission.objects.filter(content_type=content_type, codename=pn )
            for pr in p:
                print('p: {}'.format(p))
                group.permissions.add(pr)

    return status

def group_perms_list(group_name, app='mainapp'):
    ''' Permet d'avoir la liste des permissions d'un groupe sur un modèle donné 
    '''
    perms = []
    group_id = Group.objects.filter(name=group_name).values_list('id', flat=True)
    perms = Permission.objects.filter(group__id__in=group_id).order_by('-content_type_id')
    #print(perms)
    for p in perms:
        print(p.name)
    return perms

def add_user_group(user,group_name):
    ''' Permet d'ajouter un user à un group
    '''
    group = Group.objects.get(name=group_name)
    status = False
    if user not  in group.user_set.all():
        group.user_set.add(user)
        status = True
    return status

def del_user_group(user,group_name):
    ''' Permet de supprimer un user d'un group
    '''
    group = Group.objects.get(name=group_name)
    status = False
    if user in group.user_set.all():
        group.user_set.remove(user)
        status = True
    return status

def logout_user(request):
    logout(request)
    return redirect('mainapp:login')

def mlab(request):

    models = permissions_of_a_user(request.user)
    #print(models)

    # group_id = Group.objects.filter(name=group.name).values_list('id', flat=True)
    # perms = Permission.objects.filter(group__id__in=group_id).order_by('-content_type_id')

    # permissions_code_numerique = [0]* (len(models)*4)

    # user = request.user
    # groups_user = user.groups.all()
    # permission_list_group = group_perms_list_with_model(groups_user,models)

    # print(permission_list_group)


    return redirect('mainapp:login')

def permissions_of_a_user(user):

    # print("test user")

    if user.id != None:
        # print("fin test user")
        # if user == "AnonymousUser"
        groups_user = user.groups.all()
        models = []
        
        i = 0
        codenames = []
        for group in groups_user:
            group_id = Group.objects.filter(name=group.name).values_list('id', flat=True)
            perms = Permission.objects.filter(group__id__in=group_id).order_by('-content_type_id')

            model = [ perm.codename.split("_")[-1:] for perm in perms ]
            codename = [ perm.codename for perm in perms ]
            codenames.append(codename)
        

            model = [ m[0] for m in model]
            model = list(set(model))

            for m in model:
                if m not in models:
                    models.append(m)

        models = sorted(models)
        permissions = ['0']* (len(models)*5)

        
        #print(codenames[0])
        for elts in codenames:
            for elt in elts:
                model = elt.split("_")[1]
                #print(model)
                if(model not in permissions):
                    permissions[i] = model
                    
                    if (("view"+"_"+model) in elt):
                        permissions[i+1] = "1"
                    if (("change"+"_"+model) in elt):
                        permissions[i+2] = "1"
                    if (("add"+"_"+model) in elt):
                        permissions[i+3] = "1"

                    if (("delete"+"_"+model) in elt):
                        permissions[i+4] = "1"
                    
                    i += 5
                else:
                    j = permissions.index(model)
                                  
                    if (("view"+"_"+model) in elt):
                        permissions[j+1] = "1"
                    if (("change"+"_"+model) in elt):
                        permissions[j+2] = "1"
                    if (("add"+"_"+model) in elt):
                        permissions[j+3] = "1"

                    if (("delete"+"_"+model) in elt):
                        permissions[j+4] = "1"
    else:

        permissions = []               

    return permissions

def emploi_de_temps(request):
    
    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

    width = int(10*100/7);
    return render(request, 'mainapp/pages/emploi-de-temps.html', locals())

@csrf_exempt
def modifier_theme(request):

    if request.method == 'POST':

        if(request.is_ajax()):

            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            data_color = donnees[0]
            sidebar_class = donnees[1]
            theme_class = donnees[2]
            
            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser != True):
                    prof = Profil.objects.get(user=request.user)
                    prof.data_color = data_color
                    prof.sidebar_class = sidebar_class
                    prof.theme_class = theme_class
                    prof.save()
                    print("-----------------------"+ prof.user.username + " ** " +  data_color + sidebar_class + theme_class)

            data = {
            "data_color" : data_color,
            "sidebar_class" : sidebar_class,
            "theme_class" : theme_class,                
            }

        return JSONResponse(data)

def classe(request,id, page=1,nbre_element_par_page=pagination_nbre_element_par_page):
    
    classe = Classe.objects.filter(id=id)[0]
    eleves = Cours.objects.filter(id_classe = id)[0].eleves.all().order_by('nom')
    
    garcons = Cours.objects.filter(id_classe = id)[0].eleves.all().filter(sexe="masculin")
    filles = Cours.objects.filter(id_classe = id)[0].eleves.all().filter(sexe="feminin")

    nbre_eleves_en_sante = len(Cours.objects.filter(id_classe = id)[0].eleves.all().filter(etat_sante="0"))
    nbre_eleves_sante_fragile = len(Cours.objects.filter(id_classe = id)[0].eleves.all().filter(etat_sante="1"))
    nbre_eleves_malade = len(Cours.objects.filter(id_classe = id)[0].eleves.all().filter(etat_sante="2"))
    
    nbre_eleves = len(eleves)
    nbre_garcons = len(garcons)
    nbre_filles = len(filles)

    cours = Cours.objects.filter(id_classe = id);

    first_cours = Cours.objects.filter(id_classe = id)[0];

    classesAll = Classe.objects.filter(archived = "0").order_by('-nom_classe')

    sous_etab = SousEtab.objects.filter(archived = "0").all()[0]
    sous_etabs = SousEtab.objects.filter(archived = "0").all()

    paginator = Paginator(eleves, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        page_active = paginator.page(page)
    except PageNotAnInteger:
        page_active = paginator.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        page_active = paginator.page(paginator.num_pages)

    #gestion de la description textuelle de la pagination
    nbre_item = len(eleves)

    first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

    if (nbre_item - first_item_page < nbre_element_par_page):
        last_item_page = first_item_page + (nbre_item - first_item_page)
    else:
        last_item_page = int(page_active.number) * nbre_element_par_page


    liste_page = list(paginator.page_range)
    numero_page_active =  page_active.number

    page_prec = numero_page_active - 1
    page_suiv = numero_page_active + 1

    #recherche l'existence de la page precedente
    if (page_prec in liste_page):
        possede_page_precedente = True
        page_precedente = page_prec
    else:
        possede_page_precedente = False
        page_precedente = 0
    
    #recherche l'existence de la page suivante
    if (page_suiv in liste_page):
        possede_page_suivante = True
        page_suivante = page_suiv
    else:
        possede_page_suivante = False
        page_suivante = 0

    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default

    return render(request, 'mainapp/pages/classe.html', locals())

@csrf_exempt
def initialisation_fin(request,page=1, nbre_element_par_page=pagination_nbre_element_par_page):
    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        prof = Profil.objects.get(user=request.user)
        data_color = prof.data_color
        sidebar_class = prof.sidebar_class
        theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default
    # [print(x) for x in Classe.objects.only('nom_classe')]
    # all_classes = Classe.objects.only('nom_classe')
    # classes = Classe.objects.filter(nom_classe="6eA",annee_scolaire="2019-2020")[0]\
    #             .annees.filter(annee="2019-2020")[0]
    # list_eleves = classes.eleves.all()
    # annee = "2019-2020"

    # ASSOCIATION DES ELEVES AUX COURS

    # for clss in all_classes:
    #     classes = Classe.objects.filter(nom_classe=clss,annee_scolaire=annee)[0]\
    #             .annees.filter(annee=annee)[0]
    #     list_eleves = classes.eleves.all()
    #     grps = classes.groupes.filter()

    #     for gr in grps:
    #         grp = classes.groupes.filter(libelle=gr)[0].cours
    #         list_cours = list(grp.all())
    #         list_eleves = list(list_eleves)
    #         for lc in list_cours:
    #             print("cours: ",lc)
    #             grp.filter(nom_cours=lc)[0].eleves.add(*list_eleves)

    # TEST UPDATE NOTES POUR UN ELEVE DANS UNE MATIERE

        # rep = classes.groupes.filter(libelle="G1")[0].cours.filter(nom_cours="Maths")[0].eleves.filter(id=1)[0]#.values('matricule','nom')
        # pr = rep.divisions_temps.all()
        # [print (p.notes.all()[0])  for p in pr]
        # nt = Note()
        # nt.score = 16.5
        # nt.save()

        # dt = DivisionTemps()
        # dt.libelle = "Eval1"
        # dt.niveau_division_temps = 1
        # dt.notes.add(nt)
        # dt.save()

        # rep.divisions_temps.add(dt)
        
        # rep = classes.groupes.filter(libelle="G1")[0].cours.filter(nom_cours="Maths")[0].eleves.filter(id=1)[0]#.values('matricule','nom')

        # print(rep.divisions_temps.all()[0].notes.all())


    
    # configure = 0
    # if request.method == 'POST':  
    #     config = InitialisationForm(request.POST, request.FILES)
    #     #print(request.FILES['file'])
    #     if config.is_valid():  
    #         handle_uploaded_file(request.FILES['file'])
    #         #print(request.FILES['file'].name)
    #     configure = 1  
    #         # return HttpResponse("File uploaded successfuly")

    # else:  
    #     form = InitialisationForm()
    #     isConfig =0
    #     if(Etab.objects.count() > 0):
    #         isConfig = 1
          
    #     # return render(request,"index.html",{'form':config})  
    #     return render(request,"mainapp/pages/initialisation.html", locals())  

    # configure = 1
    isNbMatformatOk = "ok"
    if request.method == 'GET':

        sousetabs = SousEtab.objects.filter(archived = "0").order_by('-nom_sousetab')

        for se in sousetabs:
            if not se.format_matricule:
                isNbMatformatOk = "no"
                break


        nbreItem = len(sousetabs)


        #form = ClasseForm  
        paginator = Paginator(sousetabs, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

        try:
            # La définition de nos URL autorise comme argument « page » uniquement 
            # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
            page_active = paginator.page(page)
        except PageNotAnInteger:
            page_active = paginator.page(1)
        except EmptyPage:
            # Nous vérifions toutefois que nous ne dépassons pas la limite de page
            # Par convention, nous renvoyons la dernière page dans ce cas
            page_active = paginator.page(paginator.num_pages)

        #gestion de la description textuelle de la pagination
        nbre_item = len(sousetabs)

        first_item_page = (int(page_active.number)-1) * nbre_element_par_page + 1

        if(int(page_active.number)-1 != 0):
            last_item_page = first_item_page + len(list(paginator.page_range)) -1
        else:
            last_item_page = int(page_active.number) * nbre_element_par_page


        #gerer les preferences utilisateur en terme de theme et couleur
        if (request.user.id != None):
            if(request.user.is_superuser == True):
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default
            else:          
                #print(request.user.is_superuser)
                prof = Profil.objects.get(user=request.user)
                data_color = prof.data_color
                sidebar_class = prof.sidebar_class
                theme_class = prof.theme_class
        else:
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default

      
        return render(request, 'mainapp/pages/initialisation-fin.html', locals())



    else:

        school = Etab.objects.count()
        print("LEN = ",school)
        # location = request.FILES['file']
        location = request.session.get('location', None)
        print("location: ", location)
        print("Le debut ...")
        xl = pd.ExcelFile(location)
        nb_sheet = len(xl.sheet_names)
        print(nb_sheet)
        # print(xl.sheet_names[2])
        cpt_sheet = 0
        cpt_sheet2 = 0
        
        df = pd.read_excel(location, sheet_name="Start")
        df2 = pd.read_excel(location, sheet_name="Start")
        # print(df.columns)
        nom_etab = df[df.columns[1]].values[0]
        # etab = Etab()
        # etab.nom_etab=nom_etab
        # etab.save()
        etab = Etab.objects.filter(nom_etab=nom_etab)[0]
        print(nom_etab)
        
        ANNEE_SCOLAIRE = "2019-2020"
        

        while cpt_sheet < nb_sheet:
            cpt_sheet2 = 0
            appellation_formateur = ""
            list_cycle = []
            list_cycle_classe = []
            list_niveau = []
            list_classe = []
            liste_admin_staff = []
            current_sousetab = ""
            has_groupe_matiere =""
            max_niveau_classe = 0
            selected_sheet = xl.sheet_names[cpt_sheet]
            liste_last_group_matiere = []
            group_matiere_classe = ""
            if "Sous_Etab" in selected_sheet or "Sub_School" in selected_sheet:
                print(selected_sheet)
                df = pd.read_excel(location, sheet_name=selected_sheet)
                # print (df.loc[0, 'B'])
                # print("Column headings:")
                print(df.columns)
                # print(len(list_classe))
                # break
                if len(df.columns) > 10:
                    # pd.isnull(df.columns[51])== False
                    if pd.isnull(df[df.columns[4]].values[1])== False:
                        if df[df.columns[4]].values[1] == "Oui":
                            has_groupe_matiere = "Oui"
                        else:
                            has_groupe_matiere = ""
                    else:
                        has_groupe_matiere = ""
                    
                    print("has_groupe_matiere: ",has_groupe_matiere)
                    max_niveau_classe = int(df[df.columns[5]].values[1])
                    print("max_niveau_classe:  ", max_niveau_classe)
                    print("NOTATION SUR ", df[df.columns[1]].values[5])
                    langue = df[df.columns[1]].values[3]
                    nom_sous_etab = df.columns[1]
                    current_sousetab = nom_sous_etab
                    # sousEtab = SousEtab()
                    # sousEtab.nom_sousetab =nom_sous_etab
                    # sousEtab.annee_scolaire = ANNEE_SCOLAIRE
                    # sousEtab.langue = langue
                    # sousEtab.bulletin_base_sur = df[df.columns[1]].values[4]
                    # sousEtab.notation_sur = float(df[df.columns[1]].values[5])
                    # sousEtab.appellation_coef = df[df.columns[1]].values[6]
                    # sousEtab.format_bulletin = df[df.columns[1]].values[10]
                    # sousEtab.has_group_matiere = True if has_groupe_matiere == "Oui" else False
                    # sousEtab.profondeur_division_temps = 0
                    # sousEtab.format_matricule = matformat
                    # sousEtab.mat_fixedindex = mat_fixedindex
                    # sousEtab.mat_yearindex = mat_yearindex
                    # sousEtab.mat_varyindex = mat_varyindex

                    # sousEtab.nom_etab = etab.nom_etab
                    # sousEtab.id_etab = etab.id

                    # sousEtab.save()
                    # etab.sous_etabs.add(sousEtab)
                    # etab.save()
                    sousEtab = SousEtab.objects.filter(nom_sousetab=current_sousetab)[0]

                    # matformat = "HT190000"
                    matformat = sousEtab.format_matricule
                    mat_fixedindex = int(sousEtab.mat_fixedindex)
                    mat_yearindex = int(sousEtab.mat_yearindex)
                    mat_varyindex = int(sousEtab.mat_varyindex)
                    first_matricule = sousEtab.first_matricule

                    # position = [x for x in range(mat_varyindex)]
                    position2 = sousEtab.position

                    position3 = list(position2)
                    position = [0]*mat_varyindex
                    idf = 0
                    for item in position3:
                        if item in '0123456789':
                            position[idf] = int(item)
                            idf += 1
                    print("position : ", position)

                    amc = AppellationModuleChapitreLecon()
                    amc.appellation_module = df[df.columns[1]].values[7]
                    amc.appellation_chapitre = df[df.columns[1]].values[8]
                    amc.appellation_lecon = df[df.columns[1]].values[9]
                    amc.save()

                    # sous_etab = df.columns[1]
                    nb_cycle = df[df.columns[1]].values[0]
                    appellation_apprenant = df[df.columns[1]].values[1]

                    aaf = AppellationApprenantFormateur ()
                    aaf.appellation_apprenant = appellation_apprenant
                    aaf.appellation_formateur = df[df.columns[1]].values[2]
                    appellation_formateur = df[df.columns[1]].values[2]
                    liste_admin_staff.append(df[df.columns[1]].values[2])
                    aaf.save()

                    print(nb_cycle, appellation_apprenant)

                    i = 12
                    nb_niveaux = 0
                    nb_cycle = 1
                    continu = True

                    # print("Cycle: ",df['Unnamed: 3'].values[11])
                    nom_cycle = "Cycle 1" if pd.isnull(df['Unnamed: 3'].values[11]) else df['Unnamed: 3'].values[11]
                    
                    cycle = Cycle()
                    cycle.nom_cycle = nom_cycle

                    cycle.nom_etab = etab.nom_etab
                    cycle.id_etab = etab.id
                    cycle.id_sousetab = sousEtab.id
                    cycle.nom_sousetab = sousEtab.nom_sousetab

                    cycle.save()
                    list_cycle.append(nom_cycle)
                    sousEtab.cycles.add(cycle)
                    # sousEtab.save()

                    print(nom_cycle)

                    passed = False

                    while continu == True and pd.isnull(df['Unnamed: 3'].values[i] ) == False:
                        if passed == True:
                            nb_cycle += 1
                            nom_cycle = "Cycle " + str(nb_cycle)
                            cycle = Cycle()
                            cycle.nom_cycle = nom_cycle

                            cycle.nom_etab = etab.nom_etab
                            cycle.id_etab = etab.id
                            cycle.id_sousetab = sousEtab.id
                            cycle.nom_sousetab = sousEtab.nom_sousetab

                            cycle.save()
                            list_cycle.append(nom_cycle)
                            sousEtab.cycles.add(cycle)
                            # sousEtab.save()

                            print("* ",nom_cycle)
                            passed = False

                        if "Niveau" in df['Unnamed: 3'].values[i] or "Level" in df['Unnamed: 3'].values[i]:
                            print("Niveau: ",df['Unnamed: 4'].values[i])
                            nb_niveaux += 1

                            niv = Niveau()
                            niv.nom_niveau = df['Unnamed: 4'].values[i]

                            niv.nom_etab = etab.nom_etab
                            niv.id_etab = etab.id
                            niv.id_sousetab = sousEtab.id
                            niv.nom_sousetab = sousEtab.nom_sousetab
                            niv.id_cycle = cycle.id
                            niv.nom_cycle = cycle.nom_cycle

                            niv.save()
                            list_niveau.append(df['Unnamed: 4'].values[i])
                            # if nb_cycle == 1:
                            cycle.niveaux.add(niv)
                            cycle.save()
                            # else:
                            #     cycle2.niveaux.add(niv)
                            #     cycle2.save()

                        else:
                            if "_" not in df['Unnamed: 3'].values[i]:
                                nb_cycle += 1
                                # nom_cycle = "Cycle 1" if pd.isnull(df['Unnamed: 3'].values[11]) else df['Unnamed: 3'].values[11]

                                cycle = Cycle()
                                cycle.nom_cycle = df['Unnamed: 3'].values[i]

                                cycle.nom_etab = etab.nom_etab
                                cycle.id_etab = etab.id
                                cycle.id_sousetab = sousEtab.id
                                cycle.nom_sousetab = sousEtab.nom_sousetab

                                cycle.save()
                                list_cycle.append(df['Unnamed: 3'].values[i])
                                sousEtab.cycles.add(cycle)
                                # sousEtab.save()

                                print("Cycle ",nb_cycle," :",df['Unnamed: 3'].values[i])
                            else:

                                annee_scolaire = AnneeScolaire()
                                annee_scolaire.annee = ANNEE_SCOLAIRE
                                annee_scolaire.save()

                                classe = Classe()
                                classe.nom_classe = df['Unnamed: 4'].values[i]
                                classe.annee_scolaire = ANNEE_SCOLAIRE
                                # classe.annees.add(annee_scolaire)
                                list_cycle_classe.append(cycle.nom_cycle)

                                classe.nom_etab = etab.nom_etab
                                classe.id_etab = etab.id
                                classe.id_sousetab = sousEtab.id
                                classe.nom_sousetab = sousEtab.nom_sousetab
                                classe.id_cycle = cycle.id
                                classe.nom_cycle = cycle.nom_cycle
                                classe.id_niveau = niv.id
                                classe.nom_niveau = niv.nom_niveau
                                classe.annees.add(annee_scolaire)
                                classe.save()
                                list_classe.append(df['Unnamed: 4'].values[i])
                                niv.classes.add(classe)
                                niv.save()

                                if has_groupe_matiere == "Oui":
                                    ind_grp = 8
                                    if pd.isnull(df['Unnamed: 8'].values[i]) == False:
                                        if df['Unnamed: 8'].values[i] == "_":
                                            for grp_mat in liste_last_group_matiere:
                                                groupe = Groupe()
                                                groupe.libelle = grp_mat
                                                groupe.classe = classe.nom_classe
                                                groupe.nom_sousetab = sousEtab.nom_sousetab
                                                groupe.id_sousetab = sousEtab.id
                                                groupe.save()
                                                annee_scolaire.groupes.add(groupe)
                                                print("_Groupe add: ",groupe.libelle, groupe.classe )
                                        else:
                                            liste_last_group_matiere = []
                                            group_matiere_classe = df['Unnamed: 4'].values[i]
                                            while pd.isnull(df['Unnamed: '+str(ind_grp)].values[i]) == False:
                                                liste_last_group_matiere.append(df['Unnamed: '+str(ind_grp)].values[i])
                                                groupe = Groupe()
                                                groupe.libelle = df['Unnamed: '+str(ind_grp)].values[i]
                                                groupe.classe = classe.nom_classe
                                                groupe.nom_sousetab = sousEtab.nom_sousetab
                                                groupe.id_sousetab = sousEtab.id
                                                groupe.save()
                                                annee_scolaire.groupes.add(groupe)
                                                print("Groupe add: ",groupe.libelle, groupe.classe )
                                                ind_grp += 1


                                

                                print("CLASS -- CYCLE",classe.nom_classe, cycle.nom_cycle)
                        
                        if pd.isnull(df['Unnamed: 3'].values[i+1])== True:
                            if pd.isnull(df['Unnamed: 3'].values[i+2])== False:
                                print("µµµµµµµµ", df['Unnamed: 3'].values[i+2])
                                if (df['Unnamed: 3'].values[i+2] != "Oui") and (df['Unnamed: 3'].values[i+2] != "Non") and (df['Unnamed: 3'].values[i+2]!="Yes") and (df['Unnamed: 3'].values[i+2]!="No"):
                                    passed = True

                                    print("µµµµµµµµ ici")
                                    continu = True
                                    i += 2
                                else:
                                    continu = False
                                    print("µµµµµµµµ labas")

                                    # i += 1
                            else:
                                continu = False
                                # i += 1
                        else:
                            continu = True
                            i += 1
                        # print("__*__",df['Unnamed: 2'].values[i+1])
                    print(i)
                    i += 1
                    print("Nb niveaux: {}".format(nb_niveaux))
                    # print(df['Unnamed: 4'].values[i-1])

                    # has_dortoir = df['Unnamed: 3'].values[i+1] == "Oui"
                    has_dortoir = df['Unnamed: 3'].values[i+1] == "Oui" or df['Unnamed: 3'].values[i+1] == "Yes" if pd.isnull(df['Unnamed: 3'].values[i+1]) ==False else False            
                    has_bus = df['Unnamed: 3'].values[i+2] == "Oui" or df['Unnamed: 3'].values[i+2] == "Yes" if pd.isnull(df['Unnamed: 3'].values[i+2]) ==False else False            
                    # has_bus = df['Unnamed: 3'].values[i+2] == "Oui"
                    print("LANGUE ", langue)
                    if has_dortoir == True:
                        dortoir = Dortoir()
                        dortoir.libelle = "Dortoir" if ("ran" in langue) or ("renc" in langue) else "Dormitory"
                        dortoir.is_active = True
                        dortoir.save()

                    if has_bus == True:
                        bus = Bus()
                        bus.libelle = "Bus"
                        bus.is_active = True
                        bus.save()

                    print(df['Unnamed: 3'].values[i+1], df['Unnamed: 3'].values[i+2])
                    print("\n---Dortoir: {}".format(has_dortoir))
                    print("\n---Bus: {}".format(has_bus))

                    index_hierachie = i + 3
                    index_pers_appui = i + 3
                    index_operation = i + 3
                    index_matiere = i + 3
                    index_type_enseignant = i + 3
                    index_division_temps = i + 3
                    index_reunion = i + 3
                    nb_matiere = 0


                    print("\n---Les Reunions: ", index_reunion)

                    while pd.isnull(df['Unnamed: 20'].values[index_reunion] ) == False:
                        print("Reunion1: ", df['Unnamed: 20'].values[index_reunion])
                        tr = TypeReunion()
                        tr.annee_scolaire = ANNEE_SCOLAIRE
                        tr.libelle = df['Unnamed: 20'].values[index_reunion]
                        colnn = 22
                        nb_participants = int(df['Unnamed: 21'].values[index_reunion])
                        dcpt = 0
                        while dcpt < nb_participants:
                        # while pd.isnull(df['Unnamed: '+str(colnn)].values[index_reunion] ) == False:
                            if pd.isnull(df['Unnamed: '+str(colnn)].values[index_reunion] ) == False:
                                tr.participants += "+"+df['Unnamed: '+str(colnn)].values[index_reunion]
                            colnn += 1
                            dcpt +=1
                            print("participant list:", tr.participants)
                            
                        tr.save()
                        # print("participant list:", tr.participants)

                        index_reunion += 1
                        # break


                    print("\n---Les Pers Administratif: ")

                    priorite_admin_staff = 0
                    while pd.isnull(df['Unnamed: 7'].values[index_hierachie] ) == False:
                        
                        tas = TypeAdminStaff()
                        tas.libelle = df['Unnamed: 7'].values[index_hierachie]
                        tas.priorite = priorite_admin_staff
                        tas.type_admin_staff = "Pers Administratif"
                        tas.save()

                        liste_admin_staff.append(df['Unnamed: 7'].values[index_hierachie])

                        priorite_admin_staff += 1

                        print("   {}".format(df['Unnamed: 7'].values[index_hierachie]))

                        index_hierachie += 1
                    print("\n---Les Pers d'Appui: ")

                    priorite_admin_staff = 0
                    while pd.isnull(df['Unnamed: 8'].values[index_pers_appui] ) == False:
                        
                        tas = TypeAdminStaff()
                        tas.libelle = df['Unnamed: 8'].values[index_pers_appui]
                        tas.priorite = priorite_admin_staff
                        tas.type_admin_staff = "Pers Appui"
                        tas.save()

                        liste_admin_staff.append(df['Unnamed: 8'].values[index_pers_appui])

                        priorite_admin_staff += 1

                        print("   {}".format(df['Unnamed: 8'].values[index_pers_appui]))

                        index_pers_appui += 1
                    
                        print("\n---Les Type Enseignant: ")  
                    while pd.isnull(df['Unnamed: 15'].values[index_type_enseignant] ) == False:

                        te = TypeEnseignant()
                        te.libelle = df['Unnamed: 15'].values[index_type_enseignant]
                        te.save()

                        liste_admin_staff.append(df['Unnamed: 15'].values[index_type_enseignant])

                        print("   {}".format(df['Unnamed: 15'].values[index_type_enseignant]))

                        index_type_enseignant += 1

                    print("\n---Les Operations  --   E/S?: ")
                    while pd.isnull(df['Unnamed: 9'].values[index_operation] ) == False:
                        print("   {} -- {} -- {}".format(df['Unnamed: 9'].values[index_operation],df['Unnamed: 10'].values[index_operation],df['Unnamed: 11'].values[index_operation]))
                        if pd.isnull(df['Unnamed: 9'].values[index_operation]) == False:
                            if df['Unnamed: 9'].values[index_operation] != "_":
                                if pd.isnull(df['Unnamed: 10'].values[index_operation]) == False:
                                    if pd.isnull(df['Unnamed: 11'].values[index_operation]) == False:
                                        if df['Unnamed: 11'].values[index_operation] == appellation_apprenant:
                                            tpe = TypePayementEleve()
                                            tpe.libelle = df['Unnamed: 9'].values[index_operation]
                                            tpe.entree_sortie_caisee = "e" if ("Entrée de Caisse" == df['Unnamed: 10'].values[index_operation]) or ("Cash in" == df['Unnamed: 10'].values[index_operation]) else "s"
                                            if pd.isnull(df['Unnamed: 12'].values[index_operation]) == False:
                                                tpe.montant = df['Unnamed: 12'].values[index_operation]
                                            tpe.save()
                                        else:
                                            if (df['Unnamed: 11'].values[index_operation] == "Other") or (df['Unnamed: 11'].values[index_operation] == "Autre"):
                                                tpd = TypePayementDivers()
                                                tpd.libelle = df['Unnamed: 9'].values[index_operation]
                                                tpd.entree_sortie_caisee = "e" if ("Entrée de Caisse" == df['Unnamed: 10'].values[index_operation]) or ("Cash in" == df['Unnamed: 10'].values[index_operation]) else "s"
                                                if pd.isnull(df['Unnamed: 12'].values[index_operation]) == False:
                                                    tpd.montant = df['Unnamed: 12'].values[index_operation]
                                                tpd.save()
                                            else:
                                                type_payement = ""
                                                if df['Unnamed: 11'].values[index_operation] == appellation_formateur:
                                                    type_payement = "Enseignant"
                                                else:
                                                    type_payement = "Pers Administratif"
                                                tpas = TypePayementAdminStaff()
                                                tpas.libelle = df['Unnamed: 9'].values[index_operation]
                                                tpas.entree_sortie_caisee = "e" if ("Entrée de Caisse" == df['Unnamed: 10'].values[index_operation]) or ("Cash in" == df['Unnamed: 10'].values[index_operation]) else "s"
                                                tpas.type_payement = type_payement
                                                tpas.person = df['Unnamed: 11'].values[index_operation]
                                                if pd.isnull(df['Unnamed: 12'].values[index_operation]) == False:
                                                    tpas.montant = df['Unnamed: 12'].values[index_operation]
                                                tpas.save()

                        index_operation += 1
                    print("\n---Les Matières: ") 

                    while pd.isnull(df['Unnamed: 13'].values[index_matiere] ) == False:

                        matiere = Matiere()
                        matiere.nom_matiere = df['Unnamed: 13'].values[index_matiere]
                        matiere.code = df['Unnamed: 14'].values[index_matiere]
                        matiere.id_sousetab = sousEtab.id
                        matiere.nom_sousetab = sousEtab.nom_sousetab
                        matiere.save()

                        print("   {}".format(df['Unnamed: 13'].values[index_matiere]))
                        index_matiere += 1
                        nb_matiere += 1

                    for op in liste_admin_staff:
                        print(op)
                    

                    print("\n---Les Divisions du temps: ")  
                    profondeur_division_temps = 1
                    while pd.isnull(df['Unnamed: 16'].values[index_division_temps] ) == False:
                        
                        dt = LesDivisionTemps()
                        dt.libelle = df['Unnamed: 16'].values[index_division_temps]
                        dt.niveau_division_temps = profondeur_division_temps
                        dt.save()
                        sousEtab.divisions_temps.add(dt)
                        sousEtab.profondeur_division_temps = profondeur_division_temps
                        # sousEtab.objects.update(profondeur_division_temps=F('profondeur_division_temps') + 1)
                        # sousEtab.save()

                        print("   {} - {}".format(df['Unnamed: 16'].values[index_division_temps],df['Unnamed: 17'].values[index_division_temps]))
                        index_division_temps += 1
                        profondeur_division_temps += 1

                    i = 0
                    j = 1
                    index_niveau = 148

                    print(current_sousetab)

                    
                    while i < nb_niveaux:
                        j = 1
                        id = index_niveau + 1
                        current_niveau = list_niveau[0]
                        list_niveau.pop(0)
                        list_niveau.append(current_niveau)

                        while j <= nb_matiere:
                            col = 3
                            coef = 0
                            global_coef = False        
                            
                            if df['Unnamed: 2'].values[id] != "_" :
                                coef = df['Unnamed: 2'].values[id]
                                global_coef = True
                                # print(global_coef)
                            nom_matiere = df[nom_sous_etab].values[index_niveau + j]
                            print(" \nMatiere :   {}".format(df[nom_sous_etab].values[index_niveau + j]))
                            cpte = 0


                            while pd.isnull(df['Unnamed: '+str(col)].values[id] ) == False :
                                if pd.isnull(df['Unnamed: '+str(col)].values[index_niveau])==True:
                                    break

                                clss = df['Unnamed: '+str(col)].values[index_niveau]
                                print(" \nClasse :",clss)
                                index_classe = list_classe.index(clss)
                                # print(list_cycle_classe[index_classe])
                                current_cycle = list_cycle_classe[index_classe]

                                insert = False
                                eff_coef = "_"
                                current_classe = df['Unnamed: '+str(col)].values[index_niveau]
                                # current_groupe = df['Unnamed: '+str(col+max_niveau_classe+1)].values[index_niveau]

                                if global_coef == True:
                                    print("classe - coef: {} : {}".format(df['Unnamed: '+str(col)].values[index_niveau],coef) )
                                    insert = True
                                    eff_coef = coef
                                else:
                                    print("classe - coef: {} : {}".format(df['Unnamed: '+str(col)].values[index_niveau],df['Unnamed: '+str(col)].values[index_niveau+j]) )
                                    if df['Unnamed: '+str(col)].values[index_niveau+j] != "_":
                                        insert = True
                                        eff_coef = df['Unnamed: '+str(col)].values[index_niveau+j]
                                
                                current_groupe = df['Unnamed: '+str(col+max_niveau_classe+1)].values[index_niveau+j]
                                
                                if eff_coef != "_":
                                    matiere = Matiere.objects.filter(nom_matiere=nom_matiere)[0]
                                    cours = Cours()
                                    cours.nom_matiere = nom_matiere
                                    cours.id_matiere = matiere.id
                                    cours.code_matiere = matiere.code
                                    
                                    # id_clss = Classe.objects.filter(nom_classe=current_classe).values_list('id', flat=True)
                                    clss = Classe.objects.filter(nom_classe=current_classe)[0]
                                    
                                    cours.nom_classe = current_classe
                                    cours.nom_cycle = clss.nom_cycle
                                    cours.nom_sousetab = clss.nom_sousetab
                                    cours.nom_etab = clss.nom_etab
                                    cours.id_cycle = clss.id_cycle
                                    cours.id_classe = clss.id
                                    cours.id_sousetab = clss.id_sousetab
                                    cours.id_etab = clss.id_etab

                                    cours.annee_scolaire = ANNEE_SCOLAIRE

                                    cours.matiere.add(matiere)
                                    cours.coef = eff_coef
                                    cours.save()

                                    print("C N CL M ",current_cycle, current_niveau, current_classe, nom_matiere)
                                    if has_groupe_matiere == "Oui":
                                        print("******",current_groupe, current_classe )
                                        data = Etab.objects.filter(nom_etab=nom_etab)[0]\
                                                .sous_etabs.filter(nom_sousetab=current_sousetab)[0]\
                                                .cycles.filter(nom_cycle=current_cycle)[0]\
                                                .niveaux.filter(nom_niveau=current_niveau)[0]\
                                                .classes.filter(nom_classe=current_classe)[0]\
                                                .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                                .groupes.filter(libelle=current_groupe, classe=current_classe)[0]\
                                                .cours.add(cours)
                                    else:
                                        data = Etab.objects.filter(nom_etab=nom_etab)[0]\
                                                .sous_etabs.filter(nom_sousetab=current_sousetab)[0]\
                                                .cycles.filter(nom_cycle=current_cycle)[0]\
                                                .niveaux.filter(nom_niveau=current_niveau)[0]\
                                                .classes.filter(nom_classe=current_classe)[0]\
                                                .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                                .cours.add(cours)
                                cpte += 1
                                col +=1

                            j += 1
                            id += 1
                        index_niveau += nb_matiere + 1
                        i += 1
                        # i = 7
                    nb_clss = len(list_classe)
                    if "ran" in langue:
                        indice = selected_sheet.split("Sous_Etab")[1]
                    else:
                        indice = selected_sheet.split("Sub_School")[1]

                    app_formateur = indice+"_"+appellation_formateur
                    print(nb_clss, selected_sheet, app_formateur)
                    nc =0
                    idf = 0
                    # matlast = ""
                    while cpt_sheet2 < nb_sheet:
                        nc =0
                        if xl.sheet_names[cpt_sheet2] == app_formateur:
                            print("Fichier des formateurs: ",app_formateur," en cours d'analyse ...")
                            df2 = pd.read_excel(location, sheet_name=xl.sheet_names[cpt_sheet2])
                            # print(df2.columns)
                            cross = 0
                            nb_lign = len(df2[df2.columns[0]])
                            # enseignant = Enseignant()
                            indc = 0
                            while nb_lign > 0 :
                                if pd.isnull(df2[df2.columns[0]].values[indc])== False:
                                    print(df2[df2.columns[0]].values[indc])
                                    cross = 1
                                    enseignant = Enseignant()
                                    enseignant.nom = df2[df2.columns[0]].values[indc]
                                    if pd.isnull(df2[df2.columns[1]].values[indc])== False:
                                        enseignant.prenom = df2[df2.columns[1]].values[indc]
                                    if pd.isnull(df2[df2.columns[2]].values[indc])== False:
                                        enseignant.sexe = df2[df2.columns[2]].values[indc]
                                    if pd.isnull(df2[df2.columns[3]].values[indc])== False:
                                        enseignant.date_entree = df2[df2.columns[3]].values[indc]
                                    if pd.isnull(df2[df2.columns[4]].values[indc])== False:
                                        enseignant.tel1 = df2[df2.columns[4]].values[indc]
                                    if pd.isnull(df2[df2.columns[5]].values[indc])== False:
                                        enseignant.email = df2[df2.columns[5]].values[indc]
                                    if pd.isnull(df2[df2.columns[6]].values[indc])== False:
                                        enseignant.mapiere_specialisation1 = df2[df2.columns[6]].values[indc]
                                    if pd.isnull(df2[df2.columns[7]].values[indc])== False:
                                        enseignant.mapiere_specialisation2 = df2[df2.columns[7]].values[indc]
                                    if pd.isnull(df2[df2.columns[8]].values[indc])== False:
                                        enseignant.mapiere_specialisation3 = df2[df2.columns[8]].values[indc]
                                nb_lign -= 1
                                indc += 1
                                if cross == 1:
                                    enseignant.is_active = True
                                    enseignant.save()
                                    print('Saving:', enseignant.nom, enseignant.prenom)
                                    data = SousEtab.objects.filter(nom_sousetab=current_sousetab,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                            .enseignants.add(enseignant)
                        else:
                            # matlast = ""
                            # idf = 0
                            while nc < nb_clss:
                                # print(xl.sheet_names[cpt_sheet2],list_classe[nc])
                                if xl.sheet_names[cpt_sheet2] == indice+"_"+list_classe[nc]:
                                    print("Classe: ", list_classe[nc], " en cours d'analyse ...")
                                    df2 = pd.read_excel(location, sheet_name=xl.sheet_names[cpt_sheet2])
                                    id_classe_actuelle = Classe.objects.values('id').filter(nom_classe__iexact = list_classe[nc])[0]['id']
                                    nb_lign = len(df2[df2.columns[0]])
                                    indc = 0
                                    cross = 0
                                    eleves = []
                                    # idf = 0
                                    while nb_lign > 0 :
                                        if pd.isnull(df2[df2.columns[0]].values[indc])== False:
                                            # Le nom de l'eleve
                                            print(df2[df2.columns[0]].values[indc])
                                            cross = 1
                                            eleve = Eleve()
                                            eleve.classe_actuelle = list_classe[nc]
                                            eleve.id_classe_actuelle = id_classe_actuelle
                                            eleve.nom = df2[df2.columns[0]].values[indc]
                                            if pd.isnull(df2[df2.columns[1]].values[indc])== False:
                                                eleve.prenom = df2[df2.columns[1]].values[indc]
                                            if pd.isnull(df2[df2.columns[2]].values[indc])== False:
                                                eleve.sexe = df2[df2.columns[2]].values[indc]
                                            if pd.isnull(df2[df2.columns[3]].values[indc])== False:
                                                eleve.date_naissance = str(Timestamp(df2[df2.columns[3]].values[indc])).split(" ")[0]
                                            if pd.isnull(df2[df2.columns[4]].values[indc])== False:
                                                eleve.lieu_naissance = df2[df2.columns[4]].values[indc]
                                            if pd.isnull(df2[df2.columns[5]].values[indc])== False:
                                                eleve.date_entree = df2[df2.columns[5]].values[indc]
                                            if pd.isnull(df2[df2.columns[6]].values[indc])== False:
                                                eleve.redouble = df2[df2.columns[6]].values[indc]
                                            if pd.isnull(df2[df2.columns[7]].values[indc])== False:
                                                eleve.nom_pere = df2[df2.columns[7]].values[indc]
                                            if pd.isnull(df2[df2.columns[8]].values[indc])== False:
                                                eleve.email_pere = df2[df2.columns[8]].values[indc]
                                            if pd.isnull(df2[df2.columns[9]].values[indc])== False:
                                                eleve.tel_pere = df2[df2.columns[9]].values[indc]
                                            if pd.isnull(df2[df2.columns[10]].values[indc])== False:
                                                eleve.nom_mere = df2[df2.columns[10]].values[indc]
                                            if pd.isnull(df2[df2.columns[11]].values[indc])== False:
                                                eleve.email_mere = df2[df2.columns[11]].values[indc]
                                            if pd.isnull(df2[df2.columns[12]].values[indc])== False:
                                                eleve.tel_mere = df2[df2.columns[12]].values[indc]
                                            
                                            # if(indc % 2 ==0):
                                            #     eleve.sexe = "masculin"
                                            # else:
                                            #     eleve.sexe = "feminin"

                                            if(indc % 3 ==0):
                                                eleve.etat_sante = "0"
                                            elif(indc % 3 ==1):
                                                eleve.etat_sante = "1"
                                            else:
                                                eleve.etat_sante = "2"

                                        nb_lign -= 1
                                        indc += 1
                                        if cross == 1:
                                            # print("ici", eleve.nom, eleve.prenom)
                                            # exists = Eleve.objects.exists()
                                            if  idf == 0: #and exists == False:
                                                idf += 1
                                                # matformat = matformat.split('*')
                                                # matlast = matformat
                                                matlast = first_matricule
                                                # print("***PREMIER ELEVE: ", matlast)
                                                # position = [x for x in range(mat_varyindex)]
                                                eleve.matricule = ''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))
                                                matlast = eleve.matricule
                                            else:
                                                # print("***AUTRE ELEVE: ", matlast)
                                                # last_eleve = Eleve.objects.filter().order_by('-id')[0]
                                                # matlast = last_eleve.matricule
                                                eleve.matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))
                                                matlast = eleve.matricule
                                                # print("***MAT  ", matlast)

                                            eleve.save()
                                            # data = Classe.objects.filter(nom_classe=list_classe[nc],annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                            #         .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                            #         .eleves.add(eleve)

                                            Cours.objects.filter(nom_classe=list_classe[nc],annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                                    .eleves.add(eleve)

                                    break
                                nc += 1
                        cpt_sheet2 += 1


            cpt_sheet += 1
        # ASSOCIATION DES ELEVES AUX COURS
        annee = ANNEE_SCOLAIRE
        all_classes = Classe.objects.values('id')
        [print(c) for c in all_classes]
        for clss in all_classes:
            classes = Classe.objects.filter(pk=clss['id'],annee_scolaire=annee)[0]\
                    .annees.filter(annee=annee)[0]
            list_eleves = classes.eleves.all()
            grps = classes.groupes.values('id')
            # grps = classes.groupes.only('id')
            print("CLASSE: ", clss['id'] )
            for gr in grps:
                grp = classes.groupes.filter(pk=gr['id'])[0].cours
                # list_cours = list(grp.all())
                list_cours = list(grp.values('id'))
                list_eleves = list(list_eleves)
                for lc in list_cours:
                    print("cours: ",lc['id'])
                    grp.filter(pk=lc['id'])[0].eleves.add(*list_eleves)
        # return render(request, 'mainapp/pages/config-terminere.html', locals())
        return redirect('mainapp:dashboard')

@csrf_exempt
def initialisation_charger_fichier(request):
    #gerer les preferences utilisateur en terme de theme et couleur
    # last_eleve_mat = Eleve.objects.filter().order_by('-id').values('matricule')
    # print("LAST MAT: ", last_eleve_mat[0]['matricule'])
   
    if (request.user.id != None):
        prof = Profil.objects.get(user=request.user)
        data_color = prof.data_color
        sidebar_class = prof.sidebar_class
        theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default
   
    configure = 0
    if request.method == 'POST':  
        config = InitialisationForm(request.POST, request.FILES)
        #print(request.FILES['file'])
        if config.is_valid():  
            handle_uploaded_file(request.FILES['file'])
            #print(request.FILES['file'].name)
        configure = 1  
            # return HttpResponse("File uploaded successfuly")

    else:  
        form = InitialisationForm()
        isConfig =0
        if(Etab.objects.count() > 0):
            isConfig = 1
          
        # return render(request,"index.html",{'form':config})  
        return render(request,"mainapp/pages/initialisation-charger-fichier.html", locals())  

    if configure == 1:
        school = Etab.objects.count()
        # if school > 0:
            # Profil.objects.all().delete()
            # Etudiant.objects.all().delete()
            # AppellationModuleChapitreLecon.objects.all().delete()
            # AppellationApprenantFormateur.objects.all().delete()
            # TypeApprenant.objects.all().delete()
            # Document.objects.all().delete()
            # Chambre.objects.all().delete()
            # Bus.objects.all().delete()
            # Chauffeur.objects.all().delete()
            # Dortoir.objects.all().delete()
            # AppreciationNote.objects.all().delete()
            # CorrepondanceNoteLettre.objects.all().delete()
            # TypeReunion.objects.all().delete()
            # Reunion.objects.all().delete()
            # Periode.objects.all().delete()
            # Absence.objects.all().delete()
            # TypeEnseignant.objects.all().delete()
            # Enseignant.objects.all().delete()
            # TypeAdminStaff.objects.all().delete()
            # Pause.objects.all().delete()
            # Jour.objects.all().delete()
            # ConfigAnnee.objects.all().delete()
            # Discipline.objects.all().delete()
            # ConditionRenvoi.objects.all().delete()
            # ConditionSucces.objects.all().delete()
            # Note.objects.all().delete()
            # ResultatEleve.objects.all().delete()
            # GroupeInfosRecap.objects.all().delete()
            # CoursInfosRecap.objects.all().delete()
            # LesDivisionTemps.objects.all().delete()
            # ObservationsEleve.objects.all().delete()
            # DivisionTemps.objects.all().delete()
            # Message.objects.all().delete()
            # Matiere.objects.all().delete()
            # Transport.objects.all().delete()
            # Cantine.objects.all().delete()
            # PayementChambre.objects.all().delete()
            # Eleve.objects.all().delete()
            # CahierDeTexte.objects.all().delete()
            # Cours.objects.all().delete()
            # Groupe.objects.all().delete()
            # AnneeScolaire.objects.all().delete()
            # Classe.objects.all().delete()
            # AdminStaff.objects.all().delete()
            # Niveau.objects.all().delete()
            # Cycle.objects.all().delete()
            # TypePayementAdminStaff.objects.all().delete()
            # TypePayementDivers.objects.all().delete()
            # PayementAdminStaff.objects.all().delete()
            # PayementFacture.objects.all().delete()
            # TypePayementEleve.objects.all().delete()
            # PayementEleve.objects.all().delete()
            # SousEtab.objects.all().delete()
            # Etab.objects.all().delete()
        print("LEN = ",school)
        print("Location: ",request.FILES['file'])
        location = chemin_fichier_excel + request.FILES['file'].name
        request.session['location'] = location

        print("Le debut ...")
        xl = pd.ExcelFile(location)
        nb_sheet = len(xl.sheet_names)
        print(nb_sheet)
        # print(xl.sheet_names[2])
        cpt_sheet = 0
        cpt_sheet2 = 0
        
        df = pd.read_excel(location, sheet_name="Start")
        df2 = pd.read_excel(location, sheet_name="Start")
        # print(df.columns)
        nom_etab = df[df.columns[1]].values[0]
        etab = Etab()
        etab.nom_etab=nom_etab
        etab.save()
        print(nom_etab)
        
        ANNEE_SCOLAIRE = "2019-2020"
        

        while cpt_sheet < nb_sheet:
            cpt_sheet2 = 0
            appellation_formateur = ""
            list_cycle = []
            list_cycle_classe = []
            list_niveau = []
            list_classe = []
            liste_admin_staff = []
            current_sousetab = ""
            has_groupe_matiere =""
            max_niveau_classe = 0
            selected_sheet = xl.sheet_names[cpt_sheet]
            liste_last_group_matiere = []
            group_matiere_classe = ""
            if "Sous_Etab" in selected_sheet or "Sub_School" in selected_sheet:
                print(selected_sheet)
                df = pd.read_excel(location, sheet_name=selected_sheet)
                # print (df.loc[0, 'B'])
                # print("Column headings:")
                print(df.columns)
                # print(len(list_classe))
                # break
                if len(df.columns) > 10:
                    # pd.isnull(df.columns[51])== False
                    if pd.isnull(df[df.columns[4]].values[1])== False:
                        if df[df.columns[4]].values[1] == "Oui":
                            has_groupe_matiere = "Oui"
                        else:
                            has_groupe_matiere = ""
                    else:
                        has_groupe_matiere = ""
                    
                    # matformat = "H*T*1*9*0*0*0*0"
                    mat_fixedindex = 2
                    mat_yearindex = 4
                    mat_varyindex = 8
                    position = [x for x in range(mat_varyindex)]
                    print("has_groupe_matiere: ",has_groupe_matiere)
                    max_niveau_classe = int(df[df.columns[5]].values[1])
                    print("max_niveau_classe:  ", max_niveau_classe)
                    print("NOTATION SUR ", df[df.columns[1]].values[5])
                    langue = df[df.columns[1]].values[3]
                    nom_sous_etab = df.columns[1]
                    current_sousetab = nom_sous_etab
                    sousEtab = SousEtab()
                    sousEtab.nom_sousetab =nom_sous_etab
                    sousEtab.annee_scolaire = ANNEE_SCOLAIRE
                    sousEtab.langue = langue
                    sousEtab.bulletin_base_sur = df[df.columns[1]].values[4]
                    sousEtab.notation_sur = float(df[df.columns[1]].values[5])
                    sousEtab.appellation_coef = df[df.columns[1]].values[6]
                    sousEtab.format_bulletin = df[df.columns[1]].values[10]
                    sousEtab.has_group_matiere = True if has_groupe_matiere == "Oui" else False
                    sousEtab.profondeur_division_temps = 0
                    # sousEtab.format_matricule = matformat
                    sousEtab.mat_fixedindex = mat_fixedindex
                    sousEtab.mat_yearindex = mat_yearindex
                    sousEtab.mat_varyindex = mat_varyindex

                    sousEtab.nom_etab = etab.nom_etab
                    sousEtab.id_etab = etab.id

                    sousEtab.save()
                    etab.sous_etabs.add(sousEtab)
                    etab.save()


            cpt_sheet += 1
    # return render(request, 'mainapp/pages/initialisation-fin.html', locals())
    return redirect('mainapp:initialisation_fin')

def handle_uploaded_file(f):
    with open("mainapp/templates/mainapp/static/upload/" + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def matriculeformat(request):
    # print("POSPOS ",int(SousEtab.objects.filter(pk=1)[0].position))

    #gerer les preferences utilisateur en terme de theme et couleur
    if (request.user.id != None):
        if(request.user.is_superuser == True):
            data_color = data_color_default
            sidebar_class = sidebar_class_default
            theme_class = theme_class_default
        else:          
            #print(request.user.is_superuser)
            prof = Profil.objects.get(user=request.user)
            data_color = prof.data_color
            sidebar_class = prof.sidebar_class
            theme_class = prof.theme_class
    else:
        data_color = data_color_default
        sidebar_class = sidebar_class_default
        theme_class = theme_class_default


    matvalue = ''
    i = 0
    j = 0
    k = 0
    digitnbre = 0
    lenmat2 = False
    varying = []
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    if request.POST:
        if 'Vali' in request.POST['submit'] :
            matvalue = request.POST['matricule']
            matlen = len(matvalue)
            print(matlen)
            print("*** id_modif",request.POST['id_modif'])
            request.session['id_modif'] = request.POST['id_modif']
            return render(request,'mainapp/pages/matformat.html',locals())
        else:
            matlen = 0
            matvalue = request.POST['matricule']
            matanalysed = ['']*(len(matvalue)+1)
            position = [-1]*(len(matvalue))

            #print('fixed: {}'.format(matvalue+'1'))
            #print(request.POST.getlist(matvalue+'1'))
            for fixed in request.POST.getlist(matvalue+'1'):
                matanalysed[int(fixed)] = 'f'
                print('***fixed***: {}'.format(fixed))
                position[i] = int(fixed) - 1
                i += 1
                print('{} f'.format(matvalue[int(fixed)-1]))

            for year in request.POST.getlist(matvalue+'2'):
                if (int(year) -1) not in position:
                    matanalysed[int(year)] = 'y'
                    position[i+j] = int(year) - 1
                    j += 1
                print('{} y'.format(matvalue[int(year)-1]))
            for vary in request.POST.getlist(matvalue+'3'):
                if (int(vary) -1) not in position:
                    matanalysed[int(vary)] = 'v'
                    position[i+j+k] = int(vary) - 1
                    k += 1
                    print('{} v'.format(matvalue[int(vary)-1]))
                    try:
                        v = int(matvalue[int(vary)-1])
                        varying.append(v)
                        digitnbre += 1
                    except:
                        varying.append(matvalue[int(vary)-1])
            print('---Position: ---: {}'.format(position))
            print(matanalysed)
            print('varying:{} digitnbre {}'.format(varying,digitnbre))
            print('i={}; j={}; k={}'.format(i,j,k))
            possibilities = k
            finish = 1
            print(request.POST['submit'])
            id = 0

            if 'Voir' in request.POST['submit'] or 'See' in request.POST['submit']:
                finish = 2
                print(matvalue)
                lenmat2 = True
                nbrematperyear = 1
                matricule, matricule2 = ['']*(len(matvalue)), ['']*(len(matvalue))
                while id < i:
                    matricule[position[id]] = matvalue[position[id]].upper()
                    matricule2[position[id]] = matvalue[position[id]].upper()
                    id += 1
                # Translators: format année
                annee = _('A')
                u = i+j
                while id < u:
                    matricule[position[id]] = annee
                    matricule2[position[id]] = annee
                    id += 1
                h = i+j+k
                while id < h:
                    if matvalue[position[id]] in '0123456789':
                        nbrematperyear *= 10
                        matricule[position[id]] = 'x'
                        matricule2[position[id]] = '0'
                    else:
                        matricule[position[id]] = 'c'
                        print("µµµµµµµµ: ", (position[id]+1))
                        val1 = ord(request.POST['c'+str((position[id]+1))])
                        val2 = ord(request.POST[str((position[id]+1))+'c'])
                        if val1 > val2:
                            matricule2[position[id]] = request.POST[str((position[id]+1))+'c']+''+request.POST['c'+str((position[id]+1))]
                            nbre =  val1 -val2 + 1
                        else:
                            matricule2[position[id]] = request.POST['c'+str((position[id]+1))]+''+request.POST[str((position[id]+1))+'c']
                            nbre =  val2 -val1 + 1
                        nbrematperyear *= nbre
                        if nbrematperyear < 0 :
                            nbrematperyear *=-1
                        print(nbre)
                        print(request.POST[str((position[id]+1))+'c'])
                        print(request.POST['c'+str((position[id]+1))])
                    id += 1
                print(matricule)

                print(" matricule2 : ",matricule2)
                ANNEE_SCOLAIRE = "2019-2020"
                ann= list(ANNEE_SCOLAIRE.split("-")[0])
                # cpx = 0
                cpy = 3
                nbr = len(matricule2) - 1
                nbr2 = nbr
                while nbr >= 0: 
                    if matricule2[nbr] == "A" or matricule2[nbr] == "Y":
                        matricule2[nbr] = ann[cpy]
                        cpy -= 1
                    nbr -= 1

                print(" Apres le for matricule2 : ",matricule2)
                mat = '*'.join(matricule2)
                print('mat ',mat)
                mat = mat.split('*')
                print('mat ',mat)
                matok = [''] * (nbr2 + 1)
                pst = 0

                while pst <= nbr2:
                    print("INSIDE ")
                    if len(matricule2[pst]) > 1:
                        matok[pst] = matricule2[pst][0]
                    else:
                        matok[pst] = matricule2[pst]
                    pst += 1
                print("MATOK: ", matok)
                
                # print("posss ", posss)
                print('position ',position)
                position2 = position
                request.session['matformat'] = ''.join(matricule2)
                request.session['first_matricule'] = ''.join(matok)
                request.session['fixedindex'] = i
                request.session['yearindex'] = u
                request.session['varyindex'] = h
                request.session['position'] = position
                request.session['deborde'] = 0
                print(i,u,h)
                print('nbre mat par annee: {}'.format(nbrematperyear))
                print(ord('b')-ord('a'))
                matricule = ''.join(matricule)
                data = SousEtab.objects.all()
                for dt in data:
                    print(dt)
                # Décommenter la ligne suivante pour tester la génération des matricules
                # getNextMat(request)
                matformat = request.session['matformat']

                # id = int(request.POST['id_modif'])
                

                # format_matricule =  ""
                # mat_fixedindex = ""
                # mat_yearindex = ""
                # mat_varyindex = ""

                request.session["format_matricule"] = matformat
                request.session["mat_fixedindex"] = i
                request.session["mat_yearindex"] = u
                request.session["mat_varyindex"] = h
                request.session['matricule2'] = matricule2

                # print("Mat genere: ",getNextMatt(matformat,position,i,u,h,matricule2))
                return render(request,'mainapp/pages/matformat.html',locals())
            else:
                if 'Enreg' in request.POST['submit'] or 'Save' in request.POST['submit']:
                    id = int (request.session.get('id_modif', None))
                    matformat = request.session.get('matformat', None)
                    matricule2 = request.session.get('first_matricule', None)
                    i = int(request.session.get('mat_fixedindex', None))
                    u = int(request.session.get('mat_yearindex', None))
                    h = int(request.session.get('mat_varyindex', None))
                    print("********* POSITION", position)
                    # position = [x for x in range(h)]
                    position2 = ""
                    for item in position:
                        print("ITEM ",item)
                        position2 += str(item)+"_"
                    print("FINAL ", position2)
                    print("Mat genere: ",getNextMatt(matformat,position,i,u,h,matricule2))
                    matricule2 = ''.join(matricule2)

                    print("*** id modif ***: ", id)

                    # position3 = list(position2)
                    # position4 = [0]*h
                    # idf = 0
                    # for item in position3:
                    #     if item in '0123456789':
                    #         position4[idf] = int(item)
                    #         idf += 1
                    # print("position4 : ", position4)

                    # print("=== Position: ", position, "Position str: ", str(position)," tab: ", ''.join(str(position)))
                    SousEtab.objects.filter(pk=id).update(position = position2, format_matricule=matformat,mat_fixedindex=i,mat_yearindex=u,mat_varyindex=h,first_matricule = matricule2)
                    # return render(request,'mainapp/pages/initialisation-fin.html',locals())
                    # print("POSPOS ",SousEtab.objects.filter(pk=id).position)
                    return redirect('mainapp:initialisation_fin')

                else:
                    return render(request,'mainapp/pages/matformat.html',locals())

    # return render(request,'mainapp/pages/matformat.html',locals())
    # return redirect('mainapp:initialisation_fin')
# Fonction pour tester la génération du prochain matricule
def getNextMat(request):
    position = request.session.get('position', None)
    matformat = request.session.get('matformat', None)
    # Ici on suppose que matlast est le dernier matricule dans la bd et on veut générer le prochain
    # Mais attention matlast doit avoir le format que tu es entrain de tester dans la vue sinon ça
    # va générer une erreur; c'est ce que ça nous faisait. C'est pourquoi tu vois plusieurs matalast
    # en commentaire ici en bas
    # Pour voir le matricule qui sera généré après matlast tu regarde à l'invite de commandes
    matlast = 'HT1999a9'
    #matlast = '0199rH5T'
    #matlast = 'abcdefg'
    #matlast = '1234567'
    i = request.session.get('fixedindex', None)
    j = request.session.get('yearindex', None)
    h = request.session.get('varyindex', None)
    print('i= {} j={} h={}'.format(i,j,h))
    #deborde = request.session.get('deborde', 0)
    deborde = 0
    newmat, mat2 = ['']*(h+deborde), ['']*(h+deborde)
    print('deborde: {}'.format(deborde))
    print(matformat)
    print(position)
    newmat, mat2 = list(matlast), list(matlast)
    print(newmat)
    fini = False
    fini2 = False
    #passed = 0
    id = h - 1
    if deborde > 0:
        it = deborde + h - 1
        while it >= h and not fini:
            print('it= {}'.format(newmat[it]))
            if newmat[it] != '9':
                fini2 = True
            it -=1
            #passed += 1
    while id >= j and not fini:
        val = newmat[position[id]]
        print('val = {}'.format(val))
        if val in '0123456789':
            if val == '9':
                newmat[position[id]] = '0'
            else:
                newmat[position[id]] = str(int(val)+1)
                fini = True
                print('on y est: {}'.format(newmat[position[id]]))
        else:
            print('toto {}'.format(matformat[position[id]]))
            c1, c2 = matformat[position[id]][0],matformat[position[id]][1]
            if val == c2:
                newmat[position[id]] = c1
            else:
                newmat[position[id]] = chr(ord(val)+1)
                fini = True
            #print('debut: {} et fin: {} test {} {}'.format(c1,c2,val<c2,chr(ord(val)+1)))
        id -= 1

    print('fini= {} fini2= {}'.format(fini,fini2))
    if fini and not fini2:
        id = h
        while id < h+deborde:
            newmat[id] = mat2[id]
            id += 1
    elif not fini and fini2:
        p =deborde+h-1
        stop = False
        print('lili')
        while p >= h and not stop:
            
            if newmat[p] != '9':
                newmat[p] = str(int(newmat[p])+1)
                stop = True
            p -= 1

    elif not fini or (not fini2 and not fini):
        print('yeah')
        if not fini2 and not fini:
            deborde +=1
            newmat = ['']*(h+deborde)
            p =deborde+h-1
            while p > h :
                newmat[p] = '0'
                p -= 1
            newmat[p] = '1'
        #print('long: {}'.format(h+deborde))
        id = 0
        #print('ici nm: {}'.format(newmat))
        while id < h:
            if len(matformat[id]) == 1:
                newmat[id] = matformat[id]
            else:
                newmat[id] = matformat[id][0]
            id +=1
        id = i
        while id < j:
            print('mat2: {}'.format(mat2[id]))
            newmat[id] = mat2[id]
            id += 1
        #newmat[h+deborde] = '1'
        print(deborde)
        print('ça a pris feu')
    del request.session['deborde']
    request.session['deborde'] = deborde

    print(newmat)

    #getlast matricule (1)
    #extract digits and increment
    #extract chars
    #if digits maxvalue limit eg: 9999 incr chars in range specified
    #try insert if not go to (1) with this matricule as last
    print( request.session.get('position', None))

def getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast):

    matformat = list(matformat)
    i = mat_fixedindex
    j = mat_yearindex
    h = mat_varyindex
    ANNEE_SCOLAIRE = "2019-2020"

    deborde = 0
    newmat, mat2 = ['']*(h+deborde), ['']*(h+deborde)

    newmat = list(matlast)
    mat2 = newmat
    # print(newmat)
    fini = False
    fini2 = False
    #passed = 0
    id = h - 1
    if deborde > 0:
        it = deborde + h - 1
        while it >= h and not fini:
            # print('it= {}'.format(newmat[it]))
            if newmat[it] != '9':
                fini2 = True
            it -=1
            #passed += 1
    while id >= j and not fini:
        val = newmat[position[id]]
        # print('val = {}'.format(val))
        if val in '0123456789':
            if val == '9':
                newmat[position[id]] = '0'
            else:
                newmat[position[id]] = str(int(val)+1)
                fini = True
                # print('on y est: {}'.format(newmat[position[id]]))
        else:
            # print('toto {}'.format(matformat[position[id]]))
            # print("---- Ici matformat=", matformat, "id = ", id, " position[id] ", position[id], " newmat = ", newmat)
            # c1 = matformat[position[id]][0]
            # c2 = matformat[position[id]][1]
            c1 = matformat[position[id]]
            c2 = matformat[position[id]+1]
            # print("---- LA c1 = ", c1, " c2 = ", c2)
            if val == c2:
                newmat[position[id]] = c1
            else:
                newmat[position[id]] = chr(ord(val)+1)
                fini = True
            #print('debut: {} et fin: {} test {} {}'.format(c1,c2,val<c2,chr(ord(val)+1)))
        id -= 1

    # print('fini= {} fini2= {}'.format(fini,fini2))
    if fini and not fini2:
        id = h
        while id < h+deborde:
            newmat[id] = mat2[id]
            id += 1
    elif not fini and fini2:
        p =deborde+h-1
        stop = False
        # print('lili')
        while p >= h and not stop:
            
            if newmat[p] != '9':
                newmat[p] = str(int(newmat[p])+1)
                stop = True
            p -= 1

    elif not fini or (not fini2 and not fini):
        # print('yeah')
        if not fini2 and not fini:
            deborde +=1
            newmat = ['']*(h+deborde)
            p =deborde+h-1
            while p > h :
                newmat[p] = '0'
                p -= 1
            newmat[p] = '1'
        #print('long: {}'.format(h+deborde))
        id = 0
        #print('ici nm: {}'.format(newmat))
        while id < h:
            if len(matformat[id]) == 1:
                newmat[id] = matformat[id]
            else:
                newmat[id] = matformat[id][0]
            id +=1
        id = i
        while id < j:
            newmat[id] = mat2[id]
            id += 1
    
    return newmat

def createSuperUser(request):
    import os
    os.system("C:/Users/scg/Desktop/createsuperuseur.bat ")

    return render(request, 'mainapp/pages/liste-etablissements.html', locals())

def load_specialites_ajax(request):
    sousetabs = []
    niveaux = []
    classes = []
    specialites = []
    choix =""
    if (request.method == 'POST'):
        if(request.is_ajax()):
            donnees = request.POST['form_data']
            donnees = donnees.split("²²~~")
            # donnees = position + "²²~~" + id_etab + "²²~~" + etab;
            position = donnees[0]
            param2 = int(donnees[1])
            param3 = donnees[2]
            print("PYTHON: ",position,param2, param3)
            # cycles = _load_specialites_ajax(donnees_recherche,trier_par)

            # L'etab a changé on cherche les sousetabs associés
            if position == "1":
                param2 = 1
                choix = "etab"
                # sousetabs = SousEtab.objects.values_list('id','nom_sousetab').filter(id_etab = param2)
                sousetabs = SousEtab.objects.values('id','nom_sousetab').filter(id_etab = param2)
                id_sousetab0 = sousetabs[0]['id']
                niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_sousetab = id_sousetab0)
                id_niveau0 = niveaux[0]['id']
                classes = Classe.objects.values('id', 'nom_classe','code').filter(id_niveau = id_niveau0)
                # print("VALUES_LIST", sousetabs[0][1])
                # print("VALUES", sousetabs2[0]['nom_sousetab'])
            # Le sousetab a changé on cherche les niveaux et spécialités associés
            if position == "2":
                choix = "sousetab"            
                niveaux = Niveau.objects.values('id', 'nom_niveau').filter(id_sousetab = param2)
                id_niveau0 = niveaux[0]['id']
                classes = Classe.objects.values('id', 'nom_classe','code').filter(id_niveau = id_niveau0)
                specialites = Specialite.objects.values('specialite').filter(archived = "0", id_sousetab = param2).order_by('specialite').distinct()
            if position == "3":
                print("PARAM2: ",param2)
                choix = "niveau"            
                classes = Classe.objects.values('id', 'nom_classe', 'code').filter(id_niveau = param2)
                [print(cl) for cl in classes]
            #gerer les preferences utilisateur en terme de theme et couleur
            if (request.user.id != None):
                if(request.user.is_superuser == True):
                    data_color = data_color_default
                    sidebar_class = sidebar_class_default
                    theme_class = theme_class_default
                else:          
                    #print(request.user.is_superuser)
                    prof = Profil.objects.get(user=request.user)
                    data_color = prof.data_color
                    sidebar_class = prof.sidebar_class
                    theme_class = prof.theme_class
            else:
                data_color = data_color_default
                sidebar_class = sidebar_class_default
                theme_class = theme_class_default

            data = {
                "choix":choix,
                "sousetabs": sousetabs,
                "niveaux": niveaux,
                "classes": classes,
                "specialites": specialites,
                "permissions" : permissions_of_a_user(request.user),
                "data_color" : data_color,
                "sidebar_class" : sidebar_class,
                "theme_class" : theme_class,
            }

           
            return JSONResponse(data)
        else:
            liste_classes = ""
            liste_classes_afficher = ""
            print('ON VEUT CREER UNE CLASSE')
            etab = request.POST['choix_etab']
            sousetab = request.POST['choix_sousetab']
            niveau = request.POST['choix_niveau']
            specialite = request.POST['choix_specialite']
            print("RES:", etab, sousetab,niveau, specialite)
            
            liste_cls, liste_cls2, liste_id = [], [], []
            for r in request.POST:
                if "*" in r:
                    data = r.split('_')
                    print("data: ", data[0],data[1])
                    liste_classes += data[1]+"_"+data[0]+"_"
                    liste_classes_afficher += data[0]+", "
                    liste_cls.append(data[0])
                    liste_cls2.append(data[0])
                    liste_id.append(int(data[1]))
            
            specialite = specialite.strip()
            if specialite == "":
                print("Specialite vide")
            else:
                print("specialite est:", specialite)
                # On cherche s'il n ya pas deja la spécialité et le niveau en bd
                same_spe_niv = Specialite.objects.filter(Q(specialite__iexact=specialite),\
                    Q(nom_niveau__iexact=niveau.split('_')[0]))
                nbre_spe_niv = same_spe_niv.count()

                # spécialité et le niveau existe déja en bd
                if nbre_spe_niv != 0:
                    id_spe_niv = same_spe_niv[0].id
                    # On retire les classes cochées des éventuelles autres spécialités en bd
                    for c in liste_id:
                        d = liste_cls[0]
                        liste_cls.pop(0)
                        print(" ID",c," CLS", d)
                        clss = str(c)+"_"+d+"_"
                        spes = Specialite.objects.filter(Q(liste_classes__icontains=clss),~Q(id=id_spe_niv))
                        print("NBRE",spes.count())
                        for p in spes:
                            print("YO***",p.liste_classes)
                            liste = p.liste_classes.replace(clss,"")
                            liste_afficher = p.liste_classes_afficher.replace(d+", ","")
                            print("After",liste)
                            p.liste_classes = liste
                            p.liste_classes_afficher = liste_afficher
                            print("NIVEAU: ", p.nom_niveau)
                            if liste == "":
                                p.nom_niveau = ""
                            p.save()
                        Classe.objects.filter(id=c, id_etab = etab.split('_')[1],\
                            id_sousetab = sousetab.split('_')[1], id_niveau = niveau.split('_')[1]).\
                        update(specialite = specialite)

                    s = same_spe_niv[0]
                    s.nom_etab = etab.split('_')[0]
                    s.id_etab = etab.split('_')[1]
                    s.nom_sousetab = sousetab.split('_')[0]
                    s.id_sousetab = sousetab.split('_')[1]
                    s.nom_niveau = niveau.split('_')[0]
                    s.id_niveau = niveau.split('_')[1]
                    s.specialite = specialite
                    print("L2", liste_cls2)
                    for id in liste_id:
                        d = liste_cls2[0]
                        liste_cls2.pop(0)
                        cl = str(id)+"_"+d+"_"
                        if cl not in s.liste_classes:
                            s.liste_classes += cl
                            s.liste_classes_afficher += d+", "
                            print("ESSAI: ", cl)
                    s.save()
                else:
                    spe = Specialite.objects.filter(Q(specialite__iexact=specialite))
                    test = False

                    for s in spe:
                        # C'est une spécialité qui existait déjà mais sans classes associées
                        if s.nom_niveau == "":
                            print("existe deja")
                            s.nom_etab = etab.split('_')[0]
                            s.id_etab = etab.split('_')[1]
                            s.nom_sousetab = sousetab.split('_')[0]
                            s.id_sousetab = sousetab.split('_')[1]
                            s.nom_niveau = niveau.split('_')[0]
                            s.id_niveau = niveau.split('_')[1]
                            s.specialite = specialite
                            s.liste_classes = liste_classes
                            s.liste_classes_afficher = liste_classes_afficher
                            s.save()
                            test = True
                            print(liste_classes)
                            break

                    # C'est une nouvelle specialité on l'ajoute avec la liste des classes cochée
                    # if test = False:
                    #     s = Specialite()
                    #     s.nom_etab = etab.split('_')[0]
                    #     s.id_etab = etab.split('_')[1]
                    #     s.nom_sousetab = sousetab.split('_')[0]
                    #     s.id_sousetab = sousetab.split('_')[1]
                    #     s.nom_niveau = niveau.split('_')[0]
                    #     s.id_niveau = niveau.split('_')[1]
                    #     s.specialite = specialite
                    #     s.liste_classes = liste_classes
                    #     s.save()
                    # On retire les classes cochées des éventuelles autres spécialités en bd
                    for c in liste_id:
                        d = liste_cls[0]
                        liste_cls.pop(0)
                        print(" ID",c," CLS", d)
                        clss = str(c)+"_"+d+"_"
                        spes = Specialite.objects.filter(Q(liste_classes__icontains=clss))
                        print("NBRE",spes.count())
                        for p in spes:
                            # On s'assure que la spécialité ne contient pas déjà la classe courante
                            if p.specialite != specialite:
                                print("YO***",p.liste_classes)
                                liste = p.liste_classes.replace(clss,"")
                                liste_afficher = p.liste_classes_afficher.replace(d+", ","")
                                print("After",liste)
                                p.liste_classes = liste
                                p.liste_classes_afficher = liste_afficher
                                print("NIVEAU: ", p.nom_niveau)
                                if liste == "":
                                    p.nom_niveau = ""
                                p.save()
                        Classe.objects.filter(id=c, id_etab = etab.split('_')[1],\
                            id_sousetab = sousetab.split('_')[1], id_niveau = niveau.split('_')[1]).\
                        update(specialite = specialite)

                    if test == False:
                        sp = Specialite()
                        sp.nom_etab = etab.split('_')[0]
                        sp.id_etab = etab.split('_')[1]
                        sp.nom_sousetab = sousetab.split('_')[0]
                        sp.id_sousetab = sousetab.split('_')[1]
                        sp.nom_niveau = niveau.split('_')[0]
                        sp.id_niveau = niveau.split('_')[1]
                        sp.specialite = specialite
                        sp.liste_classes = liste_classes
                        sp.liste_classes_afficher = liste_classes_afficher
                        sp.save()
                        print("ICI")
                Specialite.objects.filter(specialite__iexact = specialite, nom_niveau = "").delete()
                
            return redirect('mainapp:liste_classe_specialites')

