#from django.db import models
from djongo import models

from django.contrib.auth.models import User

def renommage_photo(instance, filename):
	name, ext = filename.split('.')
	photo_repertoire = "photos/"
	
	name_file = photo_repertoire + str(instance.user.id)+ '_' + instance.user.last_name + '.' + ext
	return name_file

def renommage_photo_eleve(instance, filename):
    name, ext = filename.split('.')
    photo_repertoire = "photos/"
    
    name_file = photo_repertoire + str(instance.matricule)+ '_' + instance.nom + '_' + instance.prenom + '.' + ext
    return name_file

class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	telephone = models.TextField(blank=True)
	ville = models.TextField(blank=True)
	quartier = models.TextField(blank=True)
	photo = models.ImageField(upload_to=renommage_photo, default='photos/profil.jpg')
	photo_url = models.TextField(blank=True)

	# pour gerer la suppression utilisateur
	# quand l'utilisateur supprime on archive et on ne lui affiche plus l'element en question
	# on se reserve le droit de supprimer definitivement toutes
	archived = models.CharField(max_length=2,default="0")

	# pour gerer les preferences utilsateurs en terme de thème et couleur
	data_color = models.TextField(default='blue')
	sidebar_class = models.TextField(default='sidebar-bleu')
	theme_class = models.TextField(default='bleu')


    # site_web = models.URLField(blank=True)
	#avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
	# signature = models.TextField(blank=True)
	# inscrit_newsletter = models.BooleanField(default=False)

	def __str__(self):
		return "Profil de {0}".format(self.user.username)

	def groupes(self):
		return self.user.groups.all()

class Etudiant(models.Model):
    matricule = models.CharField(max_length=200, unique=True)
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    age = models.IntegerField()
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
        return self.nom

# def content_file_name(instance, filename):
#     name, ext = filename.split('.')
#     file_path = '{account_id}/photos/user_{user_id}.{ext}'.format(
#          account_id=instance.account_id, user_id=instance.id, ext=ext) 
#     return file_path

from djongo import models


class AppellationModuleChapitreLecon(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    appellation_module = models.CharField(max_length=200)
    appellation_chapitre = models.CharField(max_length=200)
    appellation_lecon = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
   
    def __str__(self):
            return self.appellation_module+" "+appellation_chapitre+" "+appellation_lecon

class AppellationApprenantFormateur(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    appellation_apprenant = models.CharField(max_length=200)
    appellation_formateur = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    def __str__(self):
            return self.appellation_apprenant+" "+self.appellation_formateur

class TypeApprenant(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    nom_type_apprenant = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    def __str__(self):
            return self.nom_type_apprenant

class Document(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    chemin_fichier = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Chambre(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Bus(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Chauffeur(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    date_entree = models.CharField(max_length=10)
    date_sortie = models.CharField(max_length=10)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")

    bus = models.ArrayReferenceField(
        to=Bus,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.nom+" "+self.prenom

class Dortoir(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    chambres = models.ArrayReferenceField(
        to=Chambre,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class AppreciationNote(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    borne_inf = models.FloatField()
    borne_sup = models.FloatField()
    appreciation = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.appreciation+" "+self.borne_inf+" "+self.borne_sup

class CorrepondanceNoteLettre(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    borne_inf = models.FloatField()
    borne_sup = models.FloatField()
    lettre = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.lettre+" "+self.borne_inf+" "+self.borne_sup

class TypeReunion(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    # Ici on met les types de participants séparés par * par ex: les participants possible sont:
    # Eleve, Enseignant, adminStaff d'une priorite donnée, Parent
    participants = models.TextField()
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Reunion(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    date = models.CharField(max_length=30)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # eventuelle liste de classes parsées
    # Une réunion est lancée par l'adminstaff ou le teacher de priorité la plus élevée
    classes = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")

    type_reunion = models.ArrayReferenceField(
        to=TypeReunion,
        #on_delete=models.CASCADE,
    )
    documents = models.ArrayReferenceField(
        to=Document,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

# A supprimer
# Fondu dans absence
class Periode(models.Model):
    jour = models.CharField(max_length=100) # Lundi, Mardi, ...    
    date = models.CharField(max_length=100) # 2019-12-02    
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.jour

class AbsenceEleve(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")

    jour = models.CharField(max_length=100) # Lundi, Mardi, ...    
    date = models.CharField(max_length=100) # 2019-12-02    
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # periodes = models.ArrayReferenceField(
    #     to=Periode,
    # )
    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class AbsenceAdminStaff(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")

    jour = models.CharField(max_length=100) # Lundi, Mardi, ...    
    date = models.CharField(max_length=100) # 2019-12-02    
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # periodes = models.ArrayReferenceField(
    #     to=Periode,
    # )
    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class TypeEnseignant(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    priorite = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Enseignant(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=20, default='masculin')
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    matiere_specialisation1 = models.CharField(max_length=100)
    matiere_specialisation2= models.CharField(max_length=100)
    matiere_specialisation3= models.CharField(max_length=100)
    date_entree = models.CharField(max_length=10)
    date_sortie = models.CharField(max_length=10)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")

    # A gérer convenablement plus tard
    id_user = models.IntegerField(default=1)


    quota_horaire = models.FloatField(default=0.0)

    documents = models.ArrayReferenceField(
        to=Document,
        #on_delete=models.CASCADE,
    )
    type_enseignant = models.ArrayReferenceField(
        to=TypeEnseignant,
        #on_delete=models.CASCADE,
    )
    absences = models.ArrayReferenceField(
        to=AbsenceAdminStaff,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.nom+" "+self.prenom

class TypeAdminStaff(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
     # type peut etre: Pers Administratif, Pers Appui
    type_admin_staff = models.CharField(max_length=100)
    priorite = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Pause(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    duree = models.IntegerField(default=20)
    id_sousetab = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class TrancheHoraire(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # Pour ordnonner les tranches du matin au soir
    numero_tranche = models.IntegerField(default=0)
    numero_tranche_only = models.IntegerField(default=0)
    # indicateur_tranche_suivante peut être tranche|pause
    # indicateur_tranche_suivante = models.CharField(default="tranche")

    # Permet de savoir si c'est une tranche (ie 0) ou une pause au quel cas il contient l'id de la pause
    type_tranche = models.IntegerField(default=0)
    # Contient éventuellement le nom de la pause, il faudra update atomiqmen type_tranche et nom_pause
    nom_pause = models.CharField(max_length=100, default="")
    id_pause = models.IntegerField(default=1)
    # nb_jours qui use la tranche
    nb_jours = models.IntegerField(default=0)
    nom_sousetab = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class Jour(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    heure_deb_cours = models.CharField(max_length=10)
    heure_fin_cours = models.CharField(max_length=10)
    nom_sousetab = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    numero_jour = models.IntegerField(default=1)

    archived = models.CharField(max_length=2,default="0")
    # pauses = models.ArrayReferenceField(
    #     to=Pause,
    # )
    tranche_horaires = models.ArrayReferenceField(
        to=TrancheHoraire, default=[]
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class ConfigAnnee(models.Model):
    date_deb = models.CharField(max_length=100)
    date_fin = models.CharField(max_length=100)
    duree_periode = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    jours = models.ArrayReferenceField(
        to=Jour,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.date_deb

class Discipline(models.Model):
    fait = models.TextField()
    description = models.TextField()
    nb_heures_min = models.FloatField(default=0)
    nb_heures_max = models.FloatField(default=0)
    id_sousetab = models.IntegerField(default=1)
    sanction = models.TextField(default="")
    nom_sousetab = models.CharField(max_length=100,default="")
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return self.fait

class ConditionRenvoi(models.Model):
    nb_heures_max = models.FloatField(default=0)
    age = models.FloatField(default=0)
    moyenne = models.FloatField(default=0)
    nb_jours = models.FloatField(default=0)
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    id_niveau = models.IntegerField(default=1)
    nom_niveau = models.CharField(max_length=100,default="")

    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return self.nb_heures_max

class ConditionSucces(models.Model):
    moyenne = models.FloatField(default=0)
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    id_niveau = models.IntegerField(default=1)
    nom_niveau = models.CharField(max_length=100,default="")
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return self.moyenne

class Note(models.Model):
    libelle = models.CharField(max_length=100)
    score = models.FloatField(default=-111)
    numero = models.IntegerField(default=2)
    archived = models.CharField(max_length=2,default="0")

    objects = models.DjongoManager()
    def __str__(self):
            return str(self.score)

# class DivisionTemps2(models.Model):
#     libelle = models.CharField(max_length=200)
#     date_deb = models.CharField(max_length=10)
#     date_fin = models.CharField(max_length=10)
#     annee_scolaire = models.CharField(max_length=20)

#     notes = models.ArrayReferenceField(
#         to=Note,
#         #on_delete=models.CASCADE,
#     )
#     absences = models.ArrayReferenceField(
#         to=Absence,
#         #on_delete=models.CASCADE,
#     )
#     disciplines = models.ArrayReferenceField(
#         to=Discipline,
#         #on_delete=models.CASCADE,
#     )

#     objects = models.DjongoManager()
#     def __str__(self):
#             return self.libelle
class ResultatEleve(models.Model):
    total_points = models.FloatField()
    total_coefs = models.FloatField()
    moyenne_eleve = models.FloatField()
    moyenne_classe = models.FloatField()
    taux_reussite_classe = models.FloatField()
    moyenne_premier_classe = models.FloatField()
    moyenne_dernier_classe = models.FloatField()
    nxc = models.FloatField()
    rang = models.IntegerField()
    appreciation = models.CharField(max_length=200)
    observations = models.TextField(default="")
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "

class GroupeInfosRecap(models.Model):
    # cours_note_min = models.FloatField()
    # cours_note_max = models.FloatField()
    # total_Coef = models.FloatField()
    moy = models.FloatField()
    nxc = models.FloatField()
    rang = models.IntegerField()
    appreciation = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "
# A supprimer
class CoursInfosRecap(models.Model):
    # cours_note_min = models.FloatField()
    # cours_note_max = models.FloatField()
    moy = models.FloatField(default=0.0)
    nxc = models.FloatField(default=0.0)
    rang = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "

class DivisionTempsCours(models.Model):

    note_min = models.FloatField(default=0.0)
    note_max = models.FloatField(default=0.0)
    nb_eleves_consideres = models.IntegerField(default=0)
    nb_sous_notes = models.IntegerField(default=0)
    niveau_division_temps = models.IntegerField(default=0)
    id_cours = models.IntegerField(default=1)
    id_groupe = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")
    nom_sousetab = models.CharField(max_length=100, default="")
    # mode_saisie_notes peut être points ou pourcentage
    mode_saisie_notes = models.CharField(max_length=100, default="points")
    # liste_ponderations_notes est de la forme "70%²²30%²²" ou "13²²7"
    liste_ponderations_notes = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    comptetence_visee = models.TextField(default="")
    id_divtemps_se = models.IntegerField(default=7)
    # Chaine sur la forme option²²numero²²quota²²numero²²quota
    # option peut être pourcentage, decimal, fraction, pondération, normal
    quota_notes = models.TextField(default="")

    
    objects = models.DjongoManager()
    def __str__(self):
            return self.comptetence_visee

class DivisionTempsGroupe(models.Model):
    moy = models.FloatField(default=0.0)
    nxc = models.FloatField(default=0.0)
    nb_eleves_consideres = models.IntegerField(default=0)
    total_coef_groupe = models.FloatField(default=0.0)
    note_min = models.FloatField(default=0.0)
    note_max = models.FloatField(default=0.0)
    niveau_division_temps = models.IntegerField(default=0)
    id_groupe = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")
    nom_sousetab = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    comptetence_visee = models.TextField(default="")
    id_divtemps_se = models.IntegerField(default=1)

    
    objects = models.DjongoManager()
    def __str__(self):
            return str(self.moy)

class LesDivisionTempsSousEtab(models.Model):
    libelle = models.CharField(max_length=200)
    date_deb = models.CharField(max_length=10)
    date_fin = models.CharField(max_length=10)
    date_deb_en = models.CharField(max_length=10, default="")
    date_fin_en = models.CharField(max_length=10, default="")

    date_deb_saisie = models.CharField(max_length=10, default="")
    date_fin_saisie = models.CharField(max_length=10, default="")
    date_deb_saisie_en = models.CharField(max_length=10, default="")
    date_fin_saisie_en = models.CharField(max_length=10, default="")

    # Mode peut etre saisi ou calculé
    mode = models.CharField(max_length=100, default= "")
    niveau_division_temps = models.IntegerField(default=0)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    nom_sous_hierarchie = models.CharField(max_length=200,default="")
    nom_sousetab = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    nb_sous_hierarchie = models.IntegerField(default=0)
    # sous_divisionstemps = models.ArrayReferenceField(
    #     to=LesDivisionTemps,
    #     #on_delete=models.CASCADE,
    # )
    sous_divisionstemps = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle + " " + str(self.niveau_division_temps)
# A supprimer
# fondu dans resultat_final
class ObservationsEleve(models.Model):
    observations = models.TextField()
    objects = models.DjongoManager()
    def __str__(self):
            return self.observations

class DivisionTempsEleve(models.Model):
    rang = models.IntegerField(default=1)
    moy = models.FloatField()
    nxc = models.FloatField()
    note_finale = models.FloatField(default=0.0)
    appreciation = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    nom_sousetab = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    niveau_division_temps = models.IntegerField(default=1)
    id_cours = models.IntegerField(default=1)
    id_groupe = models.IntegerField(default=1)
    id_eleve = models.IntegerField(default=1)
    id_divtemps_se = models.IntegerField(default=7)


    notes = models.ArrayReferenceField(
        to=Note,
    )
    absences = models.ArrayReferenceField(
        to=AbsenceEleve,
    ) 
    disciplines = models.ArrayReferenceField(
        to=Discipline,
    )
    groupe_infos_recap = models.ArrayReferenceField(
        to=GroupeInfosRecap,
    )
    resultat_final = models.ArrayReferenceField(
        to=ResultatEleve,
    )

    # cours_info_recap = models.ArrayReferenceField(
    #     to=CoursInfosRecap,
    # )
    # observation_final = models.ArrayReferenceField(
    #     to=ObservationsEleve,
    # )

    objects = models.DjongoManager()
    def __str__(self):
            return self.appreciation

class Message(models.Model):
    infos = models.TextField()
    annee_scolaire = models.CharField(max_length=100)
    date = models.CharField(max_length=30)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return self.infos

class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    objects = models.DjongoManager()
    def __str__(self):
            return self.titre + " " + self.nom_sousetab

class Transport(models.Model):
    montant = models.FloatField()
    cumul_montant = models.FloatField(default=0.0)
    date_deb_valide = models.CharField(max_length=20,default="")
    date_fin_valide = models.CharField(max_length=20,default="")
    id_eleve = models.IntegerField()
    id_type_payement_transport = models.IntegerField()
    is_more_recent = models.BooleanField(default=True)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.date_deb_valide

class Cantine(models.Model):
    montant = models.FloatField()
    cumul_montant = models.FloatField(default=0.0)
    date_deb_valide = models.CharField(max_length=20,default="")
    date_fin_valide = models.CharField(max_length=20,default="")
    id_eleve = models.IntegerField()
    id_type_payement_cantine = models.IntegerField()
    is_more_recent = models.BooleanField(default=True)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.date_deb_valide

class PayementChambre(models.Model):
    montant = models.FloatField()
    cumul_montant = models.FloatField(default=0.0)
    date_deb_valide = models.CharField(max_length=20,default="")
    date_fin_valide = models.CharField(max_length=20,default="")
    id_eleve = models.IntegerField()
    id_chambre = models.IntegerField()
    id_dortoir = models.IntegerField()
    id_type_payement_dortoir = models.IntegerField()
    is_more_recent = models.BooleanField(default=True)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.date_deb_valide

class Eleve(models.Model):
    matricule = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, default="")
    prenom = models.CharField(max_length=150)
    sexe = models.CharField(max_length=20, default='masculin')
    date_naissance = models.CharField(max_length=100)
    lieu_naissance = models.CharField(max_length=100)
    date_entree = models.CharField(max_length=50)
    nom_pere = models.CharField(max_length=100)
    prenom_pere = models.CharField(max_length=100)
    nom_mere = models.CharField(max_length=100)
    prenom_mere = models.CharField(max_length=100)
    tel_pere = models.CharField(max_length=100)
    tel_mere = models.CharField(max_length=100)
    email_pere = models.CharField(max_length=100)
    email_mere = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=300)
    photo = models.ImageField(upload_to=renommage_photo_eleve, default='photos/profil.jpg')
    annee_scolaire = models.CharField(max_length=100)
    redouble = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    archived = models.CharField(max_length=2,default="0")
    etat_sante = models.CharField(max_length=2,default="0")
    classe_actuelle = models.CharField(max_length=100)
    liste_classes_changees = models.CharField(max_length=150,default="")
    id_classe_actuelle = models.IntegerField()
    bourse = models.FloatField(default=0)
    # excedent : ce qui est en plus lorsque l'eleve a tout payé
    excedent = models.FloatField(default=0)
    compte = models.FloatField(default=0)
    # Pr savoir si l'élève a payé la pension pr l'année en cours
    est_en_regle = models.CharField(max_length=1, default="0")
    liste_bourses = models.TextField(default="")
    liste_bourses_afficher = models.TextField(default="")

    divisions_temps = models.ArrayReferenceField(
        to=DivisionTempsEleve,
    )
    messages = models.ArrayReferenceField(
        to=Message,
    )
    chambres = models.ArrayReferenceField(
        to=Chambre,
    )
    payements_transport = models.ArrayReferenceField(
        to=Transport,
    )
    payements_cantine = models.ArrayReferenceField(
        to=Cantine,
    )
    payements_dortoir = models.ArrayReferenceField(
        to=PayementChambre,
    )
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom+" _ "+self.prenom

class CahierDeTexte(models.Model):
    date = models.CharField(max_length=100)
    jour = models.CharField(max_length=100)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    module = models.CharField(max_length=300)
    chapitre = models.CharField(max_length=300)
    lecon = models.CharField(max_length=300)
    contenu = models.TextField()
    mot_cles = models.TextField()
    enseignant_nom = models.CharField(max_length=100)
    enseignant_prenom = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()
    def __str__(self):
            return self.module+" "+self.chapitre+" "+self.lecon

class Cours(models.Model):
    nom_matiere = models.CharField(max_length=100)
    id_matiere = models.IntegerField(default=1)
    code_matiere = models.CharField(max_length=100)
    coef = models.FloatField()
    annee_scolaire = models.CharField(max_length=100)
    volume_horaire_hebdo = models.CharField(max_length=10)
    volume_horaire_annuel = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    nom_cycle = models.CharField(max_length=100)
    nom_sousetab = models.CharField(max_length=100)
    nom_etab = models.CharField(max_length=100)
    id_classe = models.IntegerField(default=1)
    nom_classe = models.CharField(max_length=100)
    id_cycle = models.IntegerField(default=1)
    id_sousetab = models.IntegerField(default=1)
    id_etab = models.IntegerField(default=1)
    id_groupe = models.IntegerField(default=1)
    # id_groupe = models.IntegerField(default=1)
    # nom_groupe = models.CharField(max_length=100)


    eleves = models.ArrayReferenceField(
        to=Eleve,
        # on_delete=models.CASCADE, 
    )
    cahier_de_textes = models.ArrayReferenceField(
        to=CahierDeTexte,
        #on_delete=models.CASCADE,
    )
    matiere = models.ArrayReferenceField(
        to=Matiere,
        #on_delete=models.CASCADE,
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        #on_delete=models.CASCADE,
    )
    divisions_temps = models.ArrayReferenceField(
        # to=DivisionTemps,
        # plutôt
        to=DivisionTempsCours,
    )
    # classe = models.ArrayReferenceField(
    #     to=Classe,
    #     #on_delete=models.CASCADE,
    # )

    # periodes = models.ArrayReferenceField(
    #     to=Periode,
    # )

    objects = models.DjongoManager()
    def __str__(self):
        return self.nom_matiere

class Groupe(models.Model):
    libelle = models.CharField(max_length=200)
    classe = models.CharField(max_length=100)
    id_classe = models.IntegerField(default=1)
    archived = models.CharField(max_length=2,default="0")
    nom_sousetab = models.CharField(max_length=100, default="Section Fr")
    id_sousetab = models.IntegerField(default=1)
    cours = models.ArrayReferenceField(
        to=Cours,
        #on_delete=models.CASCADE,
    )

    divisions_temps = models.ArrayReferenceField(
        # to=DivisionTemps,
        # plutôt
        to=DivisionTempsGroupe,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class AnneeScolaire(models.Model):
    annee = models.CharField(max_length=30)
    archived = models.CharField(max_length=2,default="0")
    eleves = models.ArrayReferenceField(
        to=Eleve,
        # on_delete=models.CASCADE,
    )

    groupes = models.ArrayReferenceField(
        to=Groupe,
        #on_delete=models.CASCADE,
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.annee

class Specialite(models.Model):
    
    id_etab = models.IntegerField(default=1)
    nom_etab = models.CharField(max_length=200,default="")
    id_sousetab = models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=100,default="")
    id_niveau = models.IntegerField()
    nom_niveau = models.CharField(max_length=100,default="")
    # specialite correspond à Scientifique,...
    specialite = models.CharField(max_length=200)
    annee_scolaire = models.CharField(max_length=100)
    # liste_classes elle contient les classes avec les id associées à la spécialité
    # ex: 1*TleC1,2*TleC2,
    liste_classes = models.TextField(default="")
    liste_classes_afficher = models.TextField(default="")

    archived = models.CharField(max_length=2,default="0")
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.specialite

class Classe(models.Model):
    nom_classe = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    id_etab = models.IntegerField(default=1)
    id_sousetab = models.IntegerField(default=1)
    id_cycle = models.IntegerField(default=1)
    id_niveau = models.IntegerField(default=1)
    id_specialite = models.IntegerField(default=1)
    nom_etab = models.CharField(max_length=100,default="")
    nom_sousetab = models.CharField(max_length=100,default="")
    nom_cycle = models.CharField(max_length=100,default="")
    nom_niveau = models.CharField(max_length=100,default="")
    # specialite correspond à Scientifique,...
    specialite = models.CharField(max_length=200,default="")
    
    annees = models.ArrayReferenceField(
        to=AnneeScolaire,
        #on_delete=models.CASCADE,
    )
    titulaire = models.ArrayReferenceField(
        to=Enseignant,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_classe

    # def liste_eleves(self):
    #     p = Cours.
    #     my_sous_etab = SousEtab.objects.filter(cycles__id = self.id )

class AdminStaff(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    date_entree = models.CharField(max_length=10)
    date_sortie = models.CharField(max_length=10)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    liste_classes_tutelle = models.ArrayReferenceField(
        to=Classe,
        #on_delete=models.CASCADE,
    )

    documents = models.ArrayReferenceField(
        to=Document,
        #on_delete=models.CASCADE,
    )
    type_admin_staff = models.ArrayReferenceField(
        to=TypeAdminStaff,
        #on_delete=models.CASCADE,
    )
    absences = models.ArrayReferenceField(
        to=AbsenceAdminStaff,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.nom+" "+self.prenom

class Niveau(models.Model):
    nom_niveau = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    id_etab = models.IntegerField(default=1)
    id_sousetab = models.IntegerField(default=1)
    id_cycle = models.IntegerField(default=1)
    nom_etab = models.CharField(max_length=100,default="")
    nom_sousetab = models.CharField(max_length=100,default="")
    nom_cycle = models.CharField(max_length=100,default="")

    classes = models.ArrayReferenceField(
        to=Classe,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_niveau

class Cycle(models.Model):
    nom_cycle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    id_etab = models.IntegerField(default=1)
    id_sousetab = models.IntegerField(default=1)
    nom_etab = models.CharField(max_length=100,default="")
    nom_sousetab = models.CharField(max_length=100,default="")

    niveaux = models.ArrayReferenceField(
        to=Niveau,
        #on_delete=models.CASCADE,
    )
 
    def sous_etablissement_id(self):
        my_sous_etab = SousEtab.objects.filter(cycles__id = self.id )
        return my_sous_etab[0].id
    def sous_etablissement(self):
        my_sous_etab = SousEtab.objects.filter(cycles__id = self.id )
        return my_sous_etab[0].nom_sousetab

    def etablissement(self):
        my_etab = Etab.objects.filter(sous_etabs__id = self.sous_etablissement_id())
        return my_etab[0].nom_etab
    class Meta:
        ordering = ['nom_cycle']
    def __str__(self):
            return self.nom_cycle
    
    objects = models.DjongoManager()
# Payements liées aux adminstaff et aux enseignants
class TypePayementAdminStaff(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    # type peut etre: Pers Administratif, Pers Appui, Enseignant
    type_payement = models.CharField(max_length=100,default="Pers Administratif")
    person = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle
# class TypePayementEnseignant(models.Model):
#     annee_scolaire =  models.CharField(max_length=20)
#     libelle = models.CharField(max_length=100)
#     person = models.TextField()
#     entree_sortie_caisee = models.CharField(max_length=2)
#     montant = models.FloatField()
#     archived = models.CharField(max_length=2,default="0")
#     objects = models.DjongoManager()

#     def __str__(self):
#             return self.libelle
class TypePayementDivers(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    # type peut etre: Tansport, Dortoir, Cantine, Facture, Divers
    type_payement = models.CharField(max_length=100,default="Divers")
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
    date_deb = models.CharField(max_length=20,default="")
    date_fin = models.CharField(max_length=20,default="")
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class PayementAdminStaff(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    montant = models.FloatField()
    date = models.CharField(max_length=100)
    objects = models.DjongoManager()
    archived = models.CharField(max_length=2,default="0")
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        #on_delete=models.CASCADE,
    )
    admin_staffs = models.ArrayReferenceField(
        to=AdminStaff,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle

class PayementFacture(models.Model):
    libelle = models.CharField(max_length=200)
    montant = models.FloatField()
    cumul_montant = models.FloatField(default=0.0)
    date_payement = models.CharField(max_length=30)
    date_deb_valide = models.CharField(max_length=20,default="")
    date_fin_valide = models.CharField(max_length=20,default="")
    id_type_facture = models.IntegerField() 
    # Lié à la table TypePayementDivers avec type_payement="Facture"
    is_more_recent = models.BooleanField(default=True)
    archived = models.CharField(max_length=2,default="0")

    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class TypePayementEleve(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    date_deb = models.CharField(max_length=50)
    date_fin = models.CharField(max_length=50)
    # date_deb_en et date_fin_en sont les date au format anglais pr faciliter les comparaison ex "2020-09-21"
    date_deb_en = models.CharField(max_length=50, default="")
    date_fin_en = models.CharField(max_length=50, default="")
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    liste_classes = models.TextField(default="")
    liste_classes_afficher = models.TextField(default="")
    # indicateur_liste_classes permet de savoir ce qui est dans liste_classes
    # indicateur_liste_classes est sous la forme id_portee ex; 1_etab_College etoile, 
    # 7_sousetab_Section Fr, 4_cycle_Cycle1, 9_niveau_6e et est vide si liste_classes contient une
    # liste de classe sous la forme: 1_6eA_2_6eB_...
    indicateur_liste_classes = models.CharField(max_length=100, default="")
    # Permet de connaitre l'ordre de payement pour les classes concernées
    ordre_paiement = models.IntegerField(default=0)
    # niveau permet de stocker le nom du niveau si c'est un paiement lié au spécialité
    # de m que sousetab id_sousetab
    niveau = models.CharField(max_length=30,default="")
    id_niveau = models.IntegerField(default=0)

    sousetab = models.CharField(max_length=30,default="")
    id_sousetab = models.IntegerField(default=0)
    id_cycle = models.IntegerField(default=0)
    id_etab = models.IntegerField(default=0)
    
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class Bourse(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    # Concatenation du nom et prenom
    nom_eleve = models.CharField(max_length=100)
    id_eleve = models.IntegerField()
    matricule_eleve = models.CharField(max_length=20)
    nom_bourse = models.CharField(max_length=100)
    id_bourse = models.IntegerField()
    nom_classe = models.CharField(max_length=100)
    id_classe = models.IntegerField()
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class PayementEleve(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    type_payement_eleves = models.ArrayReferenceField(
        to=TypePayementEleve,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class AnneeScolaireActive(models.Model):
    active_year = models.CharField(max_length=10, default="2019-2020")
    id_sousetab = models.IntegerField(default=1)
    objects = models.DjongoManager()
    def __str__(self):
            return self.active_year

class SousEtab(models.Model):
    nom_sousetab = models.CharField(max_length=100)
    date_creation = models.CharField(max_length=100)
    nom_fondateur = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    appellation_coef = models.CharField(max_length=100)
    position = models.CharField(max_length=30)
    bp = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    tel1 = models.CharField(max_length=100)
    tel2 = models.CharField(max_length=100)
    devise = models.CharField(max_length=100)
    logo = models.CharField(max_length=200)
    langue = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    site_web = models.CharField(max_length=100)
    notation_sur = models.FloatField()
    format_bulletin = models.CharField(max_length=100)
    bulletin_base_sur = models.CharField(max_length=100)
    couleur_bulletin = models.CharField(max_length=30)
    date_rentree = models.CharField(max_length=100)
    date_fin_annee = models.CharField(max_length=100)
    profondeur_division_temps = models.IntegerField()
    deja_configure = models.BooleanField()
    has_group_matiere = models.BooleanField()
    format_matricule = models.CharField(max_length=100)
    first_matricule = models.CharField(max_length=100)
    mat_fixedindex = models.CharField(max_length=10)
    mat_yearindex = models.CharField(max_length=10)
    mat_varyindex = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    nom_etab = models.CharField(max_length=100)
    id_etab = models.IntegerField()
    appellation_bulletin = models.CharField(max_length=200, default="")
    nom_division_temps_saisisable = models.CharField(max_length=100, default="")
    # Durée de la tranche horaire dans le sousetab
    duree_tranche_horaire = models.IntegerField(default=0)
    # Par ex: séquence
    # Sous la forme 1~petite pause²²20]2~grande pause²²60]
    liste_jours_ouvrables = models.TextField(default="")
    liste_pauses = models.TextField(default="")
    # Sous la forme petite pause: 20', grande pause: 60'
    liste_pauses_afficher = models.TextField(default="")
    heure_deb_cours = models.CharField(max_length=10,default="")
    # Options d'arrondi des notes
    options_arrondi_notes = models.TextField(default="0.25²²0.5²²0.75")



    cycles = models.ArrayReferenceField(
        to=Cycle,
        #on_delete=models.CASCADE,
    )
    config_annee = models.ArrayReferenceField(
        to=ConfigAnnee,
        #on_delete=models.CASCADE,
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        #on_delete=models.CASCADE,
    )
    admin_staffs = models.ArrayReferenceField(
        to=AdminStaff,
        #on_delete=models.CASCADE,
    )
    appreciations_notes = models.ArrayReferenceField(
        to=AppreciationNote,
        #on_delete=models.CASCADE,
    )
    correspondance_note_lettres = models.ArrayReferenceField(
        to=CorrepondanceNoteLettre,
        #on_delete=models.CASCADE,
    )
    dortoirs = models.ArrayReferenceField(
        to=Dortoir,
        #on_delete=models.CASCADE,
    )
    chauffeurs = models.ArrayReferenceField(
        to=Chauffeur,
        #on_delete=models.CASCADE,
    )
    payement_eleves = models.ArrayReferenceField(
        to=PayementEleve,
        #on_delete=models.CASCADE,
    ) 
    payement_admin_staffs = models.ArrayReferenceField(
        to=PayementAdminStaff,
        #on_delete=models.CASCADE,
    )
    payement_divers = models.ArrayReferenceField(
        to=TypePayementDivers,
        #on_delete=models.CASCADE,
    )
    appellation_module_chapitre_lecon = models.ArrayReferenceField(
        to=AppellationModuleChapitreLecon,
        #on_delete=models.CASCADE,
    ) 
    appellation_apprenant_formateur = models.ArrayReferenceField(
        to=AppellationApprenantFormateur,
        #on_delete=models.CASCADE,
    )
    divisions_temps = models.ArrayReferenceField(
        to=LesDivisionTempsSousEtab,
        #on_delete=models.CASCADE,
    )
    jours = models.ArrayReferenceField(
        to=Jour, default=[]
    )
    objects = models.DjongoManager()

    def __str__(self):
            return self.nom_sousetab

    def liste_cycles(self):
        #print("-----self.cycles.objects.all()--------")
        return self.cycles.objects.all()

class Etab(models.Model):

    nom_etab = models.CharField(max_length=100)
    date_creation = models.CharField(max_length=100)
    nom_fondateur = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    bp = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    devise = models.CharField(max_length=100)
    logo = models.CharField(max_length=200)
    langue = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    active_year = models.CharField(max_length=100)
    site_web = models.CharField(max_length=100)
    deja_configure = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()

    def __str__(self):
        return self.nom_etab

    # def cycles(self):
    #     my_cycles = C.objects.filter(cycles__id = self.id )
    #     return my_sous_etab[0].nom_sousetab

class EmploiDuTemps(models.Model):
    id_cours = models.IntegerField(default=1)
    id_matiere = models.IntegerField(default=1)
    nom_matiere = models.CharField(max_length=150, default="")
    id_classe = models.IntegerField(default=1)
    nom_classe = models.CharField(max_length=100, default="")
    id_sousetab = models.IntegerField(default=1)
    id_jour = models.IntegerField(default=1)
    id_tranche= models.IntegerField(default=1)
    nom_sousetab = models.CharField(max_length=150, default="")
    enseignants = models.ArrayReferenceField(
        to=Enseignant
    )
    annee_scolaire = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_matiere+" _ "+self.nom_classe
