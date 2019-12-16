#from django.db import models
from djongo import models

from django.contrib.auth.models import User

def renommage_photo(instance, filename):
	name, ext = filename.split('.')
	photo_repertoire = "photos/"
	
	name_file = photo_repertoire + str(instance.user.id)+ '_' + instance.user.last_name + '.' + ext
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
    def __str__(self):
            return self.appellation_module+" "+appellation_chapitre+" "+appellation_lecon
class AppellationApprenantFormateur(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    appellation_apprenant = models.CharField(max_length=200)
    appellation_formateur = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.appellation_apprenant+" "+appellation_formateur

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
class Periode(models.Model):
    jour = models.CharField(max_length=100) # Lundi, Mardi, ...    
    date = models.CharField(max_length=100) # 2019-12-02    
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.jour

class Absence(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    periodes = models.ArrayReferenceField(
        to=Periode,
        #on_delete=models.CASCADE,
    )

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
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    mapiere_specialisation1 = models.CharField(max_length=100)
    mapiere_specialisation2= models.CharField(max_length=100)
    mapiere_specialisation3= models.CharField(max_length=100)
    date_entree = models.CharField(max_length=10)
    date_sortie = models.CharField(max_length=10)
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    documents = models.ArrayReferenceField(
        to=Document,
        #on_delete=models.CASCADE,
    )
    type_enseignant = models.ArrayReferenceField(
        to=TypeEnseignant,
        #on_delete=models.CASCADE,
    )
    absences = models.ArrayReferenceField(
        to=Absence,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.nom+" "+self.prenom

class TypeAdminStaff(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    priorite = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle


class Pause(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.libelle

class Jour(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    heure_deb_cours = models.CharField(max_length=10)
    heure_fin_cours = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
    pauses = models.ArrayReferenceField(
        to=Pause,
        #on_delete=models.CASCADE,
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
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.fait

class Note(models.Model):
    libelle = models.CharField(max_length=100)
    score = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
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
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "
class GroupeInfosRecap(models.Model):
    cours_note_min = models.FloatField()
    cours_note_max = models.FloatField()
    total_Coef = models.FloatField()
    moy = models.FloatField()
    nxc = models.FloatField()
    rang = models.IntegerField()
    appreciation = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "

class CoursInfosRecap(models.Model):
    cours_note_min = models.FloatField()
    cours_note_max = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return "["+self.cours_note_min+" - "+self.cours_note_max+"] "

class LesDivisionTemps(models.Model):
    libelle = models.CharField(max_length=200)
    date_deb = models.CharField(max_length=10)
    date_fin = models.CharField(max_length=10)
    niveau_division_temps = models.IntegerField()
    is_active = models.BooleanField()
    archived = models.CharField(max_length=2,default="0")
    # sous_divisionstemps = models.ArrayReferenceField(
    #     to=LesDivisionTemps,
    #     #on_delete=models.CASCADE,
    # )
    sous_divisionstemps = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle + " " + str(self.niveau_division_temps)

class ObservationsEleve(models.Model):
    observations = models.TextField()
    def __str__(self):
            return self.observations


class DivisionTemps(models.Model):
    # libelle = models.CharField(max_length=200)
    # date_deb = models.CharField(max_length=10)
    # date_fin = models.CharField(max_length=10)
    # niveau_division_temps = models.IntegerField()
    rang = models.IntegerField()
    moy = models.FloatField()
    nxc = models.FloatField()
    appreciation = models.CharField(max_length=200)
    archived = models.CharField(max_length=2,default="0")

    notes = models.ArrayReferenceField(
        to=Note,
        #on_delete=models.CASCADE,
    )
    absences = models.ArrayReferenceField(
        to=Absence,
        #on_delete=models.CASCADE,
    ) 
    disciplines = models.ArrayReferenceField(
        to=Discipline,
        #on_delete=models.CASCADE,
    )
    type_divisions_temps = models.ArrayReferenceField(
        to=LesDivisionTemps,
        #on_delete=models.CASCADE,
    )
    # divisions_temps = models.ArrayReferenceField(
    #     to=DivisionTemps,
    #     #on_delete=models.CASCADE,
    # )
    divisions_temps = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)

    cours_info_recap = models.ArrayReferenceField(
        to=CoursInfosRecap,
        #on_delete=models.CASCADE,
    )
    groupe_infos_recap = models.ArrayReferenceField(
        to=GroupeInfosRecap,
        #on_delete=models.CASCADE,
    )
    resultat_final = models.ArrayReferenceField(
        to=ResultatEleve,
        #on_delete=models.CASCADE,
    )
    observation_final = models.ArrayReferenceField(
        to=ObservationsEleve,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.libelle + " " + str(self.niveau_division_temps)

class Message(models.Model):
    infos = models.TextField()
    annee_scolaire = models.CharField(max_length=100)
    date = models.CharField(max_length=30)
    archived = models.CharField(max_length=2,default="0")
    def __str__(self):
            return self.infos

class Matiere(models.Model):
    titre = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")

    def __str__(self):
            return self.titre

class Eleve(models.Model):
    matricule = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=150)
    date_naissance = models.CharField(max_length=100)
    lieu_naissance = models.CharField(max_length=100)
    matricule = models.CharField(max_length=100)
    date_entree = models.CharField(max_length=50)
    nom_pere = models.CharField(max_length=100)
    prenom_pere = models.CharField(max_length=100)
    nom_mere = models.CharField(max_length=100)
    prenom_mere = models.CharField(max_length=100)
    tel_pere = models.CharField(max_length=100)
    tel_mere = models.CharField(max_length=100)
    email_pere = models.CharField(max_length=100)
    email_mere = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=200)
    annee_scolaire = models.CharField(max_length=100)
    redouble = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")

    divisions_temps = models.ArrayReferenceField(
        to=DivisionTemps,
        #on_delete=models.CASCADE,
    )
    messages = models.ArrayReferenceField(
        to=Message,
        #on_delete=models.CASCADE,
    )
    chambres = models.ArrayReferenceField(
        to=Chambre,
        #on_delete=models.CASCADE,
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
    def __str__(self):
            return self.module+" "+self.chapitre+" "+self.lecon

class Cours(models.Model):
    nom_cours = models.CharField(max_length=100)
    coef = models.FloatField()
    archived = models.CharField(max_length=2,default="0")

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
    periodes = models.ArrayReferenceField(
        to=Periode,
        #on_delete=models.CASCADE,
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        #on_delete=models.CASCADE,
    )
    divisions_temps = models.ArrayReferenceField(
        to=DivisionTemps,
        #on_delete=models.CASCADE,
    )

    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_cours

class Groupe(models.Model):
    libelle = models.CharField(max_length=200)
    classe = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")
    cours = models.ArrayReferenceField(
        to=Cours,
        #on_delete=models.CASCADE,
    )

    divisions_temps = models.ArrayReferenceField(
        to=DivisionTemps,
        #on_delete=models.CASCADE,
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

class Classe(models.Model):
    nom_classe = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    annee_scolaire = models.CharField(max_length=100)
    archived = models.CharField(max_length=2,default="0")

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
        to=Absence,
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
    niveaux = models.ArrayReferenceField(
        to=Niveau,
        #on_delete=models.CASCADE,
    )
    
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_cycle
# Payements liées aux adminstaff et aux enseignants
class TypePayementAdminStaff(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    person = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    objects = models.DjongoManager()

    def __str__(self):
            return self.libelle

class TypePayementDivers(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
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



class TypePayementEleve(models.Model):
    annee_scolaire =  models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    date_deb = models.CharField(max_length=20)
    date_fin = models.CharField(max_length=20)
    entree_sortie_caisee = models.CharField(max_length=2)
    montant = models.FloatField()
    archived = models.CharField(max_length=2,default="0")
    classes = models.ArrayReferenceField(
        to=Classe,
        #on_delete=models.CASCADE,
    )
    
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

class SousEtab(models.Model):
    nom_sousetab = models.CharField(max_length=100)
    date_creation = models.CharField(max_length=100)
    nom_fondateur = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    appellation_coef = models.CharField(max_length=100)
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
    mat_fixedindex = models.CharField(max_length=10)
    mat_yearindex = models.CharField(max_length=10)
    mat_varyindex = models.CharField(max_length=10)
    archived = models.CharField(max_length=2,default="0")
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
        to=LesDivisionTemps,
        #on_delete=models.CASCADE,
    )
    objects = models.DjongoManager()
    def __str__(self):
            return self.nom_sousetab

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
