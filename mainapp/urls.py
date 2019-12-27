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
url('liste-niveaux/', views.liste_niveaux, name="liste_niveaux"),
url('liste-classes/', views.liste_classes, name="liste_classes"),
url('liste-matieres/', views.liste_matieres, name="liste_matieres"),
url('liste-appellation-apprenant-formateur/', views.liste_appellation_apprenant_formateur, name="liste_appellation_apprenant_formateur"),
url('liste-type-apprenants/', views.liste_type_apprenants, name="liste_type_apprenants"),
url('liste-disciplines/', views.liste_disciplines, name="liste_disciplines"),
url('liste-condition-renvois/', views.liste_condition_renvois, name="liste_condition_renvois"),
url('liste-condition-succes/', views.liste_condition_succes, name="liste_condition_succes"),



url('liste-types-paiements-eleve/', views.liste_types_paiements_eleve, name="liste_types_paiements_eleve"),
url('liste-types-paiements-pers-enseignant/', views.liste_types_paiements_pers_enseignant, name="liste_types_paiements_pers_enseignant"),
url('liste-types-paiements-pers-administratif/', views.liste_types_paiements_pers_administratif, name="liste_types_paiements_pers_administratif"),
url('liste-types-paiements-pers-appui/', views.liste_types_paiements_pers_appui, name="liste_types_paiements_pers_appui"),



url('parametres-progression/', views.parametres_progression, name="parametres_progression"),
url('parametres-cours/', views.parametres_cours, name="parametres_cours"),
url('parametres-reunion/', views.parametres_reunion, name="parametres_reunion"),

url(r'^recherche-etablissement/$', views.recherche_etablissement, name='recherche_etablissement'),
url(r'^recherche-etudiant/$', views.recherche_etudiant, name='recherche_etudiant'),
url(r'^recherche-profil/$', views.recherche_profil, name='recherche_profil'),
url(r'^recherche-cycle/$', views.recherche_cycle, name='recherche_cycle'),
url(r'^recherche-sous-etablissement/$', views.recherche_sous_etablissement, name='recherche_sous_etablissement'),
url(r'^recherche-niveau/$', views.recherche_niveau, name='recherche_niveau'),
url(r'^recherche-classe/$', views.recherche_classe, name='recherche_classe'),
url(r'^recherche-matiere/$', views.recherche_matiere, name='recherche_matiere'),
url(r'^recherche-appellation-apprenant-formateur/$', views.recherche_appellation_apprenant_formateur, name='recherche_appellation_apprenant_formateur'),
url(r'^recherche-type-apprenant/$', views.recherche_type_apprenant, name='recherche_type_apprenant'),
url(r'^recherche-discipline/$', views.recherche_discipline, name='recherche_discipline'),
url(r'^recherche-condition-renvoi/$', views.recherche_condition_renvoi, name='recherche_condition_renvoi'),
url(r'^recherche-condition-succes/$', views.recherche_condition_succes, name='recherche_condition_succes'),

url('creation-etablissement/', views.creation_etablissement, name="creation_etablissement"),
url('creation-sous-etablissement/', views.creation_sous_etablissement, name="creation_sous_etablissement"),
url('creation-etudiant/', views.creation_etudiant, name="creation_etudiant"),
url('creation-profil/', views.creation_profil, name="creation_profil"),
url('creation-cycle/', views.creation_cycle, name="creation_cycle"),
url('creation-niveau/', views.creation_niveau, name="creation_niveau"),
url('creation-classe/', views.creation_classe, name="creation_classe"),
url('creation-matiere/', views.creation_matiere, name="creation_matiere"),
url('creation-appellation-apprenant-formateur/', views.creation_appellation_apprenant_formateur, name="creation_appellation_apprenant_formateur"),
url('creation-type-apprenant/', views.creation_type_apprenant, name="creation_type_apprenant"),
url('creation-discipline/', views.creation_discipline, name="creation_discipline"),
url('creation-condition-renvoi/', views.creation_condition_renvoi, name="creation_condition_renvoi"),
url('creation-condition-succes/', views.creation_condition_succes, name="creation_condition_succes"),

url(r'^suppression-etablissement/$', views.suppression_etablissement, name='suppression_etablissement'),
url(r'^suppression-sous-etablissement/$', views.suppression_sous_etablissement, name='suppression_sous_etablissement'),
url(r'^suppression-etudiant/$', views.suppression_etudiant, name='suppression_etudiant'),
url(r'^suppression-profil/$', views.suppression_profil, name='suppression_profil'),
url(r'^suppression-cycle/$', views.suppression_cycle, name='suppression_cycle'),
url(r'^suppression-niveau/$', views.suppression_niveau, name='suppression_niveau'),
url(r'^suppression-classe/$', views.suppression_classe, name='suppression_classe'),
url(r'^suppression-matiere/$', views.suppression_matiere, name='suppression_matiere'),
url(r'^suppression-appellation-apprenant-formateur/$', views.suppression_appellation_apprenant_formateur, name='suppression_appellation_apprenant_formateur'),
url(r'^suppression-type-apprenant/$', views.suppression_type_apprenant, name='suppression_type_apprenant'),
url(r'^suppression-discipline/$', views.suppression_discipline, name='suppression_discipline'),
url(r'^suppression-condition-renvoi/$', views.suppression_condition_renvoi, name='suppression_condition_renvoi'),
url(r'^suppression-condition-succes/$', views.suppression_condition_succes, name='suppression_condition_succes'),

url(r'^modification-sous-etablissement/$', views.modification_sous_etablissement, name='modification_sous_etablissement'),
url(r'^modification-etablissement/$', views.modification_etablissement, name='modification_etablissement'),
url(r'^modification-etudiant/$', views.modification_etudiant, name='modification_etudiant'),
url(r'^modification-cycle/$', views.modification_cycle, name='modification_cycle'),
url(r'^modification-niveau/$', views.modification_niveau, name='modification_niveau'),
url(r'^modification-classe/$', views.modification_classe, name='modification_classe'),
url(r'^modification-classe/$', views.modification_classe, name='modification_classe'),
url(r'^modification-matiere/$', views.modification_matiere, name='modification_matiere'),
url(r'^modification-appellation-apprenant-formateur/$', views.modification_appellation_apprenant_formateur, name='modification_appellation_apprenant_formateur'),
url(r'^modification-type_apprenant/$', views.modification_type_apprenant, name='modification_type_apprenant'),
url(r'^modification-discipline/$', views.modification_discipline, name='modification_discipline'),
url(r'^modification-condition-renvoi/$', views.modification_condition_renvoi, name='modification_condition_renvoi'),
url(r'^modification-condition-succes/$', views.modification_condition_succes, name='modification_condition_succes'),

url('modifier-theme/', views.modifier_theme, name="modifier_theme"),

url('', views.accueil, name="accueil"),

]
