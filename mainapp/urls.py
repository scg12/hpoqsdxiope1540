from django.conf.urls import url
from mainapp import views

app_name = 'mainapp'

urlpatterns = [


url('dashboard/', views.dashboard, name="dashboard"),
url(r'^groupe-permission-modification/(?P<id>\d+)$', views.groupe_permission_modification, name='groupe_permission_modification'),
url(r'^login/$', views.login_user, name='login'),
url(r'^logout/$', views.logout_user, name='logout_user'),
url(r'^verrouiller/$', views.verrouiller, name='verrouiller'),
url(r'^deverrouiller/$', views.deverrouiller, name='deverrouiller'),

url(r'mlab/$', views.mlab, name="mlab"),
url('initialisation/', views.initialisation, name="initialisation"),
url('emploi-de-temps/', views.emploi_de_temps, name="emploi_de_temps"),


url(r'liste-profils/(?P<page>\d+)$', views.liste_profils, name="liste_profils"),
url(r'liste-profils/$', views.liste_profils, name="liste_profils"),
url(r'^liste-etudiants/(?P<page>\d+)$', views.liste_etudiants, name='liste_etudiants'),
url('liste-etudiants/', views.liste_etudiants, name="liste_etudiants"),
url('liste-groupes/', views.liste_groupes, name="liste_groupes"),

url('liste-etablissements/', views.liste_etablissements, name="liste_etablissements"),
url('liste-sous-etablissements/', views.liste_sous_etablissements, name="liste_sous_etablissements"),
url('liste-cycles/', views.liste_cycles, name="liste_cycles"),
url('liste-cours/', views.liste_cours, name="liste_cours"),
url('liste-progressions/', views.liste_progressions, name="liste_progressions"),
url('liste-reunions/', views.liste_reunions, name="liste_reunions"),

url('parametres-progression/', views.parametres_progression, name="parametres_progression"),
url('parametres-cours/', views.parametres_cours, name="parametres_cours"),
url('parametres-reunion/', views.parametres_reunion, name="parametres_reunion"),

url(r'^recherche-etablissement/$', views.recherche_etablissement, name='recherche_etablissement'),
url(r'^recherche-etudiant/$', views.recherche_etudiant, name='recherche_etudiant'),
url(r'^recherche-profil/$', views.recherche_profil, name='recherche_profil'),
url(r'^recherche-cycle/$', views.recherche_cycle, name='recherche_cycle'),
url(r'^recherche-sous-etablissement/$', views.recherche_sous_etablissement, name='recherche_sous_etablissement'),

url('creation-etablissement/', views.creation_etablissement, name="creation_etablissement"),
url('creation-sous-etablissement/', views.creation_sous_etablissement, name="creation_sous_etablissement"),
url('creation-etudiant/', views.creation_etudiant, name="creation_etudiant"),
url('creation-profil/', views.creation_profil, name="creation_profil"),
url('creation-cycle/', views.creation_cycle, name="creation_cycle"),

url(r'^suppression-etablissement/$', views.suppression_etablissement, name='suppression_etablissement'),
url(r'^suppression-sous-etablissement/$', views.suppression_sous_etablissement, name='suppression_sous_etablissement'),
url(r'^suppression-etudiant/$', views.suppression_etudiant, name='suppression_etudiant'),
url(r'^suppression-profil/$', views.suppression_profil, name='suppression_profil'),
url(r'^suppression-cycle/$', views.suppression_cycle, name='suppression_cycle'),

url(r'^modification-sous-etablissement/$', views.modification_sous_etablissement, name='modification_sous_etablissement'),
url(r'^modification-etablissement/$', views.modification_etablissement, name='modification_etablissement'),
url(r'^modification-etudiant/$', views.modification_etudiant, name='modification_etudiant'),
url(r'^modification-cycle/$', views.modification_cycle, name='modification_cycle'),
url('modifier-theme/', views.modifier_theme, name="modifier_theme"),

url('', views.accueil, name="accueil"),

]
