#from django.shortcuts import render
from django.shortcuts import render,redirect
from mainapp.forms import EtudiantForm, ProfilForm, GroupForm, EtablissementForm, SousEtablissementForm, CycleForm
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

from mainapp.models import Profil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import *

from mainapp.serializers import *

from pymongo import MongoClient

from django.db.models import Q
from mainapp.models import Etudiant
from django.apps import apps
from django.db import transaction

from .forms import InitialisationForm 
from django.contrib.staticfiles.storage import staticfiles_storage

import pandas as pd

#pour la webcam
from base64 import b64decode
from django.core.files.base import ContentFile
#from django.core.files.images.ImageFile 

# definition des constantes
pagination_nbre_element_par_page = 10
photo_repertoire = "/photos/"

# definition des preferences utilisateurs par defaut (couleur, theme, ...) pour ceux qui ne sont pas connectés
data_color_default = "blue"
sidebar_class_default = "sidebar-bleu"
theme_class_default = "bleu"

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def dashboard(request):

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

def creation_etudiant(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-etudiant.html',{'form':EtudiantForm})
    elif request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():

            matricule = form.cleaned_data['matricule']
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

def creation_sous_etablissement(request):

    if request.method == 'GET':

        return render(request, 'mainapp/pages/creation-sous-etablissement.html',{'form':SousEtablissementForm})
    elif request.method == 'POST':
        form = SousEtablissementForm(request.POST)
        if form.is_valid():

            nom_etab = form.cleaned_data['nom_etab']
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

            etab = Etab()
            etab.nom_etab = nom_etab
            etab.date_creation = date_creation
            etab.nom_fondateur = nom_fondateur
            etab.localisation = localisation
            # etab.bp = bp
            # etab.email = email
            # etab.tel = tel
            # etab.devise = devise
            # etab.langue = langue
            # etab.annee_scolaire = annee_scolaire
            # etab.site_web = site_web

            etab.save()

        return redirect('mainapp:liste_sous_etablissements')

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



    etudiants = Etudiant.objects.all().order_by('-id')

    
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

def liste_etablissements(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
    etablissement = Etab.objects.all().order_by('-id')

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

    
    sous_etablissement = SousEtab.objects.all().order_by('-id')

    
    #form = EtudiantForm  
    paginator = Paginator(sous_etablissement, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

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

    
    cycle = Cycle.objects.get(id=1)
    print("Cycle id n°---" , cycle.id)
    print("sous etablissement du cycle : ", cycle.sous_etablissement())
    print("etablissement du cycle : ", cycle.etablissement())

    data =[]

    # etabs = Etab.objects.all().order_by('-id')
    cycles = Cycle.objects.all().order_by('-id')
    # for e in etabs:
    #     for s in e.sous_etabs_id:
    #         se = SousEtab.objects.filter(pk=s)
    #         for p in se:
    #             for c in p.cycles_id:
    #                 cy = Cycle.objects.filter(pk=c)
    #                 cycle = dict(
    #                         nom_etab = e.nom_etab,
    #                         nom_sousetab = p.nom_sousetab,
    #                         nom_cycle = cy[0].nom_cycle,
    #                         cycle_id = cy[0].id
    #                 )
    #                 data.append(cycle)
    # for d in data:
    #     print(d['nom_etab'],"_",d['nom_sousetab'],"_",d['nom_cycle'],"_",d['cycle_id'])


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

def suppression_profil(request):

    id = int(request.POST['id_supp'])

    profil = Profil.objects.get(pk=id)
    profil.archived = "1"
    profil.save()

    return redirect('mainapp:liste_profils')

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

def liste_cours(request, page=1, nbre_element_par_page=pagination_nbre_element_par_page):

    
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

  
    return render(request, 'mainapp/pages/liste-cours.html', locals())

def accueil(request):
    verrou = "Verrouiller"
    return render(request, 'mainapp/pages/accueil.html', locals())

def suppression_etudiant(request):

    id = request.POST['id_supp']

    try:
        services.suppression_etudiant(id)

    except ConnectionError:
        message_title = "Service de gestion des étudiants indisponible !!!"
        message_body = "Ce service est indisponible pour l'instant, veuillez reéssayer plus tard ou contacter l'administrateur"
        message_phone1 = "(+237) 676 06 94 52"
        message_phone2 = "(+237) 674 90 58 41"
        message_email1 = "ulrichguebayi@gmail.com"
        message_email2 = "agathe.signe@gmail.com"

        return render(request, 'mainapp/pages/erreur-service-indisponible.html', locals())

    return redirect('mainapp:liste_etudiants')

def suppression_etablissement(request):

    id = request.POST['id_supp']
    # Etab.objects.get(pk=id).delete()
    
    Etab.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_etablissements')

def suppression_sous_etablissement(request):

    id = request.POST['id_supp']
    # SousEtab.objects.get(pk=id).delete()
    SousEtab.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_sous_etablissements')

def suppression_cycle(request):

    id = request.POST['id_supp']    
    Cycle.objects.filter(pk=id).update(archived="1")

    return redirect('mainapp:liste_cycles')

def modification_etudiant(request):

    id = request.POST['id_modif']

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

    id = request.POST['id_modif']
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

            Etab.objects.filter(pk=id).update(nom_etab=nom_etab,date_creation=date_creation,nom_fondateur=nom_fondateur,\
                localisation=localisation,bp=bp,email=email,tel=tel,devise=devise,langue=langue,\
                annee_scolaire=annee_scolaire,site_web=site_web)


        return redirect('mainapp:liste_etablissements')

def modification_sous_etablissement(request):

    id = request.POST['id_modif']

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


        with transaction.atomic():

            if(SousEtab.objects.filter(pk=id)[0].nom_sousetab.lower() != nom_sousetab.lower()):
                Cycle.objects.filter(id_sousetab = id).update(nom_sousetab = nom_etab)
                Niveau.objects.filter(id_sousetab = id).update(nom_sousetab = nom_etab)
                Classe.objects.filter(id_sousetab = id).update(nom_sousetab = nom_etab)


            SousEtab.objects.filter(pk=id).update(nom_etab=nom_etab,date_creation=date_creation,nom_fondateur=nom_fondateur,\
                localisation=localisation)

        return redirect('mainapp:liste_sous_etablissements')

def modification_cycle(request):

    id = request.POST['id_modif']
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')

    form = CycleForm(request.POST)
    # form.fields['nom_sousetab'].disabled = True 
    # form.fields['nom_etab'].disabled = True 

    if form.is_valid():

        nom_cycle = form.cleaned_data['nom_cycle']
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

        with transaction.atomic():

            if(Cycle.objects.filter(pk=id)[0].nom_cycle.lower() != nom_cycle.lower()):
                Niveau.objects.filter(id_cycle = id).update(nom_cycle = nom_cycle)
                Classe.objects.filter(id_cycle = id).update(nom_cycle = nom_cycle)

            Cycle.objects.filter(pk=id).update(nom_cycle=nom_cycle)

        return redirect('mainapp:liste_cycles')

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

            
            sous_etablissements = find_sous_etablissement(donnees_recherche,trier_par)


            if (nbre_element_par_page == -1):
                nbre_element_par_page = len(sous_etablissements)

            #form = EtudiantForm
            paginator = Paginator(sous_etablissements, nbre_element_par_page)  # 20 liens par page, avec un minimum de 5 liens sur la dernière

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
                "sous_etablissements": sous_etablissements,
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

    # data =[]

    # etabs = Etab.objects.all()
    # for e in etabs:
    #     for s in e.sous_etabs_id:
    #         se = SousEtab.objects.filter(pk=s)
    #         for p in se:
    #             for c in p.cycles_id:
    #                 cy = Cycle.objects.filter(pk=c)
    #                 cycle = dict(
    #                         nom_etab = e.nom_etab,
    #                         nom_sousetab = p.nom_sousetab,
    #                         nom_cycle = cy[0].nom_cycle,
    #                         cycle_id = cy[0].id
    #                 )
    #                 data.append(cycle)

    # infos = []
    
    # if recherche == "" or not recherche:
    #     cycles = data
    # else:
    #     if (trier_par == "non defini"):
    #         for dictn in data:
    #             if recherche in dictn['nom_etab'] or recherche in dictn['nom_sousetab'] or recherche in dictn['nom_cycle']:
    #                 infos.append(dictn)
    #         cycles = infos
    #     else:

    
    if recherche == "" or not recherche:
        if (trier_par == "non defini"):
            cycles = Cycle.objects.order_by('-id')
        else:
            cycles = Cycle.objects.order_by(trier_par)

    else:
        if (trier_par == "non defini"):
            # Q(archived ="0") &
            # print("*******recherche ",recherche)

            cycles = Cycle.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche)
                # Q(localisation__icontains=recherche)|
                # Q(bp__icontains=recherche) |
                # Q(email__icontains=recherche) |
                # Q(tel__icontains=recherche) |
                # Q(devise__icontains=recherche)|
                # Q(langue__icontains=recherche)
                )
            ).distinct()

        else:
            print("*******recherche ",recherche)
            cycles = Etab.objects.filter(Q(archived ="0") &
                (Q(nom_etab__icontains=recherche) |
                Q(nom_sousetab__icontains=recherche) |
                Q(nom_cycle__icontains=recherche)
                # Q(localisation__icontains=recherche)|
                # Q(bp__icontains=recherche) |
                # Q(email__icontains=recherche) |
                # Q(tel__icontains=recherche) |
                # Q(devise__icontains=recherche)|
                # Q(langue__icontains=recherche)
                )
            ).distinct().order_by(trier_par)

            

    # cycles_serializers = EtabCyclesSerializer(cycles, many=True)
    cycles_serializers = CycleSerializer(cycles, many=True)

    return cycles_serializers.data

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
        new_group.id= id_max+1
        new_group.save()
        #Group.objects.create(name=name)
        print(name)
    # Quoiqu'il arrive, on affiche la page du formulaire.

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

    print("test user")

    if user.id != None:
        print("fin test user")
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

@csrf_exempt
def initialisation(request):
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
        return render(request,"mainapp/pages/initialisation.html", locals())  

    if configure == 1:
        school = Etab.objects.count()
        print("LEN = ",school)
        print("Location: ",request.FILES['file'])
        location = request.FILES['file']
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
                    
                    matformat = "H*T*1*9*0*0*0*0"
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
                    sousEtab.format_matricule = matformat
                    sousEtab.mat_fixedindex = mat_fixedindex
                    sousEtab.mat_yearindex = mat_yearindex
                    sousEtab.mat_varyindex = mat_varyindex

                    sousEtab.nom_etab = etab.nom_etab
                    sousEtab.id_etab = etab.id

                    sousEtab.save()
                    etab.sous_etabs.add(sousEtab)
                    etab.save()

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
                    sousEtab.save()

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
                            sousEtab.save()

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
                                sousEtab.save()

                                print("Cycle ",nb_cycle," :",df['Unnamed: 3'].values[i])
                            else:

                                annee_scolaire = AnneeScolaire()
                                annee_scolaire.annee = ANNEE_SCOLAIRE
                                annee_scolaire.save()

                                classe = Classe()
                                classe.nom_classe = df['Unnamed: 4'].values[i]
                                classe.annee_scolaire = ANNEE_SCOLAIRE
                                classe.annees.add(annee_scolaire)
                                list_cycle_classe.append(cycle.nom_cycle)

                                classe.nom_etab = etab.nom_etab
                                classe.id_etab = etab.id
                                classe.id_sousetab = sousEtab.id
                                classe.nom_sousetab = sousEtab.nom_sousetab
                                classe.id_cycle = cycle.id
                                classe.nom_cycle = cycle.nom_cycle
                                classe.id_niveau = niv.id
                                classe.nom_niveau = niv.nom_niveau

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
                        print("participant list:", tr.participants)

                        index_reunion += 1
                        # break


                    print("\n---Les Hierachies: ")

                    priorite_admin_staff = 0
                    while pd.isnull(df['Unnamed: 7'].values[index_hierachie] ) == False:
                        
                        tas = TypeAdminStaff()
                        tas.libelle = df['Unnamed: 7'].values[index_hierachie]
                        tas.priorite = priorite_admin_staff
                        tas.save()

                        liste_admin_staff.append(df['Unnamed: 7'].values[index_hierachie])

                        priorite_admin_staff += 1

                        print("   {}".format(df['Unnamed: 7'].values[index_hierachie]))

                        index_hierachie += 1
                    
                        print("\n---Les Type Enseignant: ")  
                    while pd.isnull(df['Unnamed: 14'].values[index_type_enseignant] ) == False:

                        te = TypeEnseignant()
                        te.libelle = df['Unnamed: 14'].values[index_type_enseignant]
                        te.save()

                        liste_admin_staff.append(df['Unnamed: 14'].values[index_type_enseignant])

                        print("   {}".format(df['Unnamed: 14'].values[index_type_enseignant]))

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
                                                tpas = TypePayementAdminStaff()
                                                tpas.libelle = df['Unnamed: 9'].values[index_operation]
                                                tpas.entree_sortie_caisee = "e" if ("Entrée de Caisse" == df['Unnamed: 10'].values[index_operation]) or ("Cash in" == df['Unnamed: 10'].values[index_operation]) else "s"
                                                tpas.person = df['Unnamed: 11'].values[index_operation]
                                                if pd.isnull(df['Unnamed: 12'].values[index_operation]) == False:
                                                    tpas.montant = df['Unnamed: 12'].values[index_operation]
                                                tpas.save()

                        index_operation += 1
                    print("\n---Les Matières: ") 

                    while pd.isnull(df['Unnamed: 13'].values[index_matiere] ) == False:

                        matiere = Matiere()
                        matiere.titre = df['Unnamed: 13'].values[index_matiere]
                        matiere.save()

                        print("   {}".format(df['Unnamed: 13'].values[index_matiere]))
                        index_matiere += 1
                        nb_matiere += 1

                    for op in liste_admin_staff:
                        print(op)
                    

                    print("\n---Les Divisions du temps: ")  
                    profondeur_division_temps = 1
                    while pd.isnull(df['Unnamed: 15'].values[index_division_temps] ) == False:
                        
                        dt = LesDivisionTemps()
                        dt.libelle = df['Unnamed: 15'].values[index_division_temps]
                        dt.niveau_division_temps = profondeur_division_temps
                        dt.save()
                        sousEtab.divisions_temps.add(dt)
                        sousEtab.profondeur_division_temps = profondeur_division_temps
                        # sousEtab.objects.update(profondeur_division_temps=F('profondeur_division_temps') + 1)
                        sousEtab.save()

                        print("   {} - {}".format(df['Unnamed: 15'].values[index_division_temps],df['Unnamed: 16'].values[index_division_temps]))
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
                                    matiere = Matiere.objects.filter(titre=nom_matiere)[0]
                                    cours = Cours()
                                    cours.nom_cours = nom_matiere
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
                                        enseignant.date_entree = df2[df2.columns[2]].values[indc]
                                    if pd.isnull(df2[df2.columns[3]].values[indc])== False:
                                        enseignant.tel1 = df2[df2.columns[3]].values[indc]
                                    if pd.isnull(df2[df2.columns[4]].values[indc])== False:
                                        enseignant.email = df2[df2.columns[4]].values[indc]
                                    if pd.isnull(df2[df2.columns[5]].values[indc])== False:
                                        enseignant.mapiere_specialisation1 = df2[df2.columns[5]].values[indc]
                                    if pd.isnull(df2[df2.columns[6]].values[indc])== False:
                                        enseignant.mapiere_specialisation2 = df2[df2.columns[6]].values[indc]
                                    if pd.isnull(df2[df2.columns[7]].values[indc])== False:
                                        enseignant.mapiere_specialisation3 = df2[df2.columns[7]].values[indc]
                                nb_lign -= 1
                                indc += 1
                                if cross == 1:
                                    enseignant.is_active = True
                                    enseignant.save()
                                    print('Saving:', enseignant.nom, enseignant.prenom)
                                    data = SousEtab.objects.filter(nom_sousetab=current_sousetab,annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                            .enseignants.add(enseignant)
                        else:
                            matlast = ""
                            while nc < nb_clss:
                                # print(xl.sheet_names[cpt_sheet2],list_classe[nc])
                                if xl.sheet_names[cpt_sheet2] == indice+"_"+list_classe[nc]:
                                    print("Classe: ", list_classe[nc], " en cours d'analyse ...")
                                    df2 = pd.read_excel(location, sheet_name=xl.sheet_names[cpt_sheet2])
                                    # print(df2.columns)
                                    nb_lign = len(df2[df2.columns[0]])
                                    indc = 0
                                    cross = 0
                                    eleves = []
                                    idf = 0
                                    while nb_lign > 0 :
                                        if pd.isnull(df2[df2.columns[0]].values[indc])== False:
                                            print(df2[df2.columns[0]].values[indc])
                                            cross = 1
                                            eleve = Eleve()
                                            eleve.nom = df2[df2.columns[0]].values[indc]
                                            if pd.isnull(df2[df2.columns[1]].values[indc])== False:
                                                eleve.prenom = df2[df2.columns[1]].values[indc]
                                            if pd.isnull(df2[df2.columns[2]].values[indc])== False:
                                                eleve.date_naissance = df2[df2.columns[2]].values[indc]
                                            if pd.isnull(df2[df2.columns[3]].values[indc])== False:
                                                eleve.lieu_naissance = df2[df2.columns[3]].values[indc]
                                            if pd.isnull(df2[df2.columns[4]].values[indc])== False:
                                                eleve.date_entree = df2[df2.columns[4]].values[indc]
                                            if pd.isnull(df2[df2.columns[5]].values[indc])== False:
                                                eleve.redouble = df2[df2.columns[5]].values[indc]
                                            if pd.isnull(df2[df2.columns[6]].values[indc])== False:
                                                eleve.nom_pere = df2[df2.columns[6]].values[indc]
                                            if pd.isnull(df2[df2.columns[7]].values[indc])== False:
                                                eleve.email_pere = df2[df2.columns[7]].values[indc]
                                            if pd.isnull(df2[df2.columns[8]].values[indc])== False:
                                                eleve.tel_pere = df2[df2.columns[8]].values[indc]
                                            if pd.isnull(df2[df2.columns[9]].values[indc])== False:
                                                eleve.nom_mere = df2[df2.columns[9]].values[indc]
                                            if pd.isnull(df2[df2.columns[10]].values[indc])== False:
                                                eleve.email_mere = df2[df2.columns[10]].values[indc]
                                            if pd.isnull(df2[df2.columns[11]].values[indc])== False:
                                                eleve.tel_mere = df2[df2.columns[11]].values[indc]
                                                                                        
                                        nb_lign -= 1
                                        indc += 1
                                        if cross == 1:
                                            # print("ici", eleve.nom, eleve.prenom)
                                            # exists = Eleve.objects.exists()
                                            if  idf == 0: #and exists == False:
                                                idf += 1
                                                matformat = matformat.split('*')
                                                matlast = matformat
                                                print("***PREMIER ELEVE: ", matformat)
                                                # position = [x for x in range(mat_varyindex)]
                                                eleve.matricule = ''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))
                                                matlast = eleve.matricule
                                            else:
                                                # last_eleve = Eleve.objects.filter().order_by('-id')[0]
                                                # matlast = last_eleve.matricule
                                                eleve.matricule =''.join(getNextMatt(matformat,position,mat_fixedindex,mat_yearindex,mat_varyindex,matlast))
                                                matlast = eleve.matricule

                                            eleve.save()
                                            data = Classe.objects.filter(nom_classe=list_classe[nc],annee_scolaire=ANNEE_SCOLAIRE)[0]\
                                                    .annees.filter(annee=ANNEE_SCOLAIRE)[0]\
                                                    .eleves.add(eleve)
                                    break
                                nc += 1
                        cpt_sheet2 += 1


            cpt_sheet += 1
    return render(request, 'mainapp/pages/liste-etablissements.html', locals())

def handle_uploaded_file(f):
    with open("mainapp/templates/mainapp/static/upload/" + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def matriculeformat(request):
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
            if 'Enreg' in request.POST['submit'] or 'Save' in request.POST['submit']:
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
                print(matricule2)
                mat = '*'.join(matricule2)
                print('mat ',mat)
                mat = mat.split('*')
                print('mat ',mat)
                
                # print("posss ", posss)
                print('position ',position)
                request.session['matformat'] = matricule2
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

                print("Mat genere: ",getNextMatt(matformat,position,i,u,h,matricule2))
    return render(request,'matformat.html',locals())

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

    i = mat_fixedindex
    j = mat_yearindex
    h = mat_varyindex

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
            c1, c2 = matformat[position[id]][0],matformat[position[id]][1]
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