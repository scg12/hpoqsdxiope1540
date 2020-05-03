from django import forms

from django.contrib.auth.models import Group, User

# from .models import Etab, SousEtab

from django.utils.translation import ugettext_lazy as _

class EtudiantForm(forms.Form):
    # matricule = forms.CharField(
    #     label=_('MATRICULE'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE MATRICULE', 'class': 'form-control form-group matricule', 'style': 'text-transform:uppercase' }),
    # )
    nom = forms.CharField(
        label='NOM',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE NOM', 'class': 'form-control form-group nom', 'style': 'text-transform:uppercase'}),
    )
    prenom = forms.CharField(
        label=_('PRENOM'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE PRENOM', 'class': 'form-control form-group prenom', 'style': 'text-transform:capitalize'}),
    )
    age = forms.IntegerField(
        label='ÂGE',
        widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE ÂGE', 'type' : "number", 'min':'0', 'class': 'form-control form-group age'}),
    )

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class EleveForm(forms.Form):
    nom = forms.CharField(
        # label='Nom*',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-group nom', 'style': 'text-transform:uppercase', 'name' : 'nom'}),
    )
    prenom = forms.CharField(
        # label=_('Prénom*'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group prenom', 'style': 'text-transform:capitalize', 'name' : 'prenom'}),
    )
#     gender = (
#     ('masculin', 'Masculin'),
#     ('feminin', 'Féminin'),
# )
#     sexe = forms.ChoiceField(
#         label='Sexe*',
#         widget=forms.Select(choices=gender,attrs={'class': 'form-control form-group sexe', 'name' : 'sexe'}),
#         )
    # sexe = forms.CharField(
    #     label='Sexe*',
    #     max_length=5,
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group sexe', 'style': 'text-transform:capitalize'}),
    # )
    adresse = forms.CharField(
        # label='Adresse*',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-group adresse', 'style': 'text-transform:capitalize', 'name' : 'adresse'}),
    )
    # date_naissance = forms.CharField(
    #     # label='Date Naissance*',
    #     max_length=100,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group date_naissance', 'name' : 'date_naissance'}),
    # )

    # date_naissance = forms.DateField(
    #     required=True
       
    # )

    lieu_naissance = forms.CharField(
        # label='Lieu Naissance*',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-group lieu_naissance', 'name' : 'lieu_naissance'}),
    )
    date_entree = forms.CharField(
        # label='Année Scolaire Entrée*',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group date_entree', 'style': 'text-transform:capitalize', 'name' : 'date_entree'}),
    )
    nom_pere = forms.CharField(
        # label='Nom Père',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group nom_pere', 'style': 'text-transform:capitalize', 'name' : 'nom_pere'}),
    )
    prenom_pere = forms.CharField(
        # label='Prénom Père',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group prenom_pere', 'style': 'text-transform:capitalize', 'name' : 'prenom_pere'}),
    )
    nom_mere = forms.CharField(
        # label='Nom Mère',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group nom_mere', 'style': 'text-transform:capitalize', 'name' : 'nom_mere'}),
    )
    prenom_mere = forms.CharField(
        # label='Prénom Mère',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group prenom_mere', 'style': 'text-transform:capitalize', 'name' : 'prenom_pere'}),
    )
    tel_pere = forms.CharField(
        # label='Téléphone Père',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group tel_pere', 'style': 'text-transform:capitalize', 'name' : 'tel_pere'}),
    )
    tel_mere = forms.CharField(
        # label='Téléphone Mère',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group tel_mere', 'style': 'text-transform:capitalize', 'name' : 'tel_mere'}),
    )
    email_pere = forms.CharField(
        # label='Email Père',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group email_pere', 'style': 'text-transform:capitalize', 'name' : 'email_pere'}),
    )
    email_mere = forms.CharField(
        # label='Email Mère',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-group email_mere', 'style': 'text-transform:capitalize', 'name' : 'email_mere'}),
    )
    photo = forms.ImageField(
        #label='', 
        help_text="Formats accepted: JPEG nd PNG", 
        required=False,
        #validators=[FileTypeValidator(allowed_types=[ 'image/jpeg','image/png'])],
        widget=forms.ClearableFileInput(attrs={ 'class': ' file-image','style':'display:none', 'name' : 'photo', 'id': 'file'}),
    )
#     redouble = (
#     ('non', 'Non'),
#     ('oui', 'Oui'),
# )
#     redouble = forms.ChoiceField(
#     label='Redouble*',
#     widget=forms.Select(choices=redouble),

#     )
    # redouble = forms.CharField(
    #     label='Redouble*',
    #     max_length=2,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group redouble', 'style': 'text-transform:capitalize'}),
    # )

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfilForm(forms.Form):

    nom = forms.CharField(
        label=_('NOM'),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-group user__last_name', 'style': 'text-transform:uppercase'}),
    )
    prenom = forms.CharField(
        label='PRENOM',
        max_length=100,
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group user__first_name', 'style': 'text-transform:capitalize'}),
    )
    pseudo = forms.CharField(
        label='Pseudo',
        max_length=100,

        widget=forms.TextInput(attrs={ 'class': 'form-control form-group user__username' }),
    )
    # photo = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={ 'class': ' file-image', 'style':'display:none', }),
    # )
    photo = forms.ImageField(
        #label='', 
        help_text="Formats accepted: JPEG nd PNG", 
        required=False,
        #validators=[FileTypeValidator(allowed_types=[ 'image/jpeg','image/png'])],
        widget=forms.ClearableFileInput(attrs={ 'class': ' file-image','style':'display:none', 'name' : 'photo', 'id': 'file'}),
    )



    # groupe = forms.ModelChoiceField(
    #     queryset = Group.objects.all(), 
    #     empty_label = "Selectionner votre groupe",
    #     widget=forms.Select(attrs={'class': 'form-control form-group groupe' })

    # )

    telephone = forms.CharField(
        label='TELEPHONE',
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group telephone'}),
        max_length=100,
    )    
    ville = forms.CharField(
        label='Ville de residence',
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group ville'}),
        max_length=100,
    )    
    quartier = forms.CharField(
        label='Quartier de residence',
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group quartier'}),
        max_length=100,
    )

class InitialisationForm(forms.Form):  
    file = forms.FileField(
        label='Selectionner un fichier',     
        widget=forms.ClearableFileInput(attrs={ 'class': ''}),
    ) # for creating file input  

class EtablissementForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_etab = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Etablissement', 'class': 'form-control form-group nom_etab' }),
    )
    date_creation = forms.CharField(
        label='Date Création',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'date création', 'class': 'form-control form-group date_creation'}),
    )
    nom_fondateur = forms.CharField(
        label=_('Fondateur'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom Fondateur', 'class': 'form-control form-group nom_fondateur', 'style': 'text-transform:capitalize'}),
    )
    localisation = forms.CharField(
        label=_('Localisation'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Localisation', 'class': 'form-control form-group localisation' }),
    )
    bp = forms.CharField(
        label=_('Bp'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Bp', 'class': 'form-control form-group bp' }),
    )
    email = forms.CharField(
        label=_('Email'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Email', 'class': 'form-control form-group email' }),
    )
    tel = forms.CharField(
        label=_('Tel'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Tel', 'class': 'form-control form-group tel' }),
    )
    devise = forms.CharField(
        label=_('Devise'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Devise', 'class': 'form-control form-group devise' }),
    )
    langue = forms.CharField(
        label=_('Langue'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Langue', 'class': 'form-control form-group langue' }),
    )
    annee_scolaire = forms.CharField(
        label=_('Annee Scolaire'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Annee Scolaire', 'class': 'form-control form-group annee_scolaire' }),
    )
    site_web = forms.CharField(
        label=_('Site Web'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Site Web', 'class': 'form-control form-group site_web' }),
    )
    # age = forms.IntegerField(
    #     label='ÂGE',
    #     widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE ÂGE', 'type' : "number", 'min':'0', 'class': 'form-control form-group age'}),
    # )

class SousEtablissementForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_sousetab = forms.CharField(
        label=_('Sous Etab'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etablissement', 'class': 'form-control form-group nom_sousetab' }),
    )
    date_creation = forms.CharField(
        label='Date Création',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'date création', 'class': 'form-control form-group date_creation'}),
    )
    nom_fondateur = forms.CharField(
        label=_('Fondateur'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom Fondateur', 'class': 'form-control form-group nom_fondateur', 'style': 'text-transform:capitalize'}),
    )
    localisation = forms.CharField(
        label=_('Localisation'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Localisation', 'class': 'form-control form-group localisation' }),
    )
    # bp = forms.CharField(
    #     label=_('Bp'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Bp', 'class': 'form-control form-group bp' }),
    # )
    # email = forms.CharField(
    #     label=_('Email'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Email', 'class': 'form-control form-group email' }),
    # )
    # tel = forms.CharField(
    #     label=_('Tel'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Tel', 'class': 'form-control form-group tel' }),
    # )
    # devise = forms.CharField(
    #     label=_('Devise'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Devise', 'class': 'form-control form-group devise' }),
    # )
    # langue = forms.CharField(
    #     label=_('Langue'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Langue', 'class': 'form-control form-group langue' }),
    # )
    # annee_scolaire = forms.CharField(
    #     label=_('Annee Scolaire'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Annee Scolaire', 'class': 'form-control form-group annee_scolaire' }),
    # )
    # site_web = forms.CharField(
    #     label=_('Site Web'),
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Entrer Site Web', 'class': 'form-control form-group site_web' }),
    # )
    # age = forms.IntegerField(
    #     label='ÂGE',
    #     widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE ÂGE', 'type' : "number", 'min':'0', 'class': 'form-control form-group age'}),
    # )

class CycleForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_cycle= forms.CharField(
        label=_('Cycle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom Cycle', 'class': 'form-control form-group nom_cycle' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )
    nom_etab = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Etablissement', 'class': 'form-control form-group nom_etab'}),
        # required=False
    )    

class NiveauForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_niveau= forms.CharField(
        label=_('Niveau'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom Niveau', 'class': 'form-control form-group nom_niveau' }),
    )
    nom_cycle= forms.CharField(
        label=_('Cycle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom Cycle', 'class': 'form-control form-group nom_cycle' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )
    nom_etab = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Etablissement', 'class': 'form-control form-group nom_etab'}),
        # required=False
    )  

class ClasseForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_classe= forms.CharField(
        label=_('Classe'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom classe', 'class': 'form-control form-group nom_classe' }),
    )
    nom_niveau= forms.CharField(
        label=_('Niveau'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom Niveau', 'class': 'form-control form-group nom_niveau' }),
    )
    nom_cycle= forms.CharField(
        label=_('Cycle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom Cycle', 'class': 'form-control form-group nom_cycle' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )
    nom_etab = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Etablissement', 'class': 'form-control form-group nom_etab'}),
        # required=False
    )

class SpecialiteForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    speciality= forms.CharField(
        label=_('Classe'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer nom classe', 'class': 'form-control form-group speciality' }),
    )
    nom_sousetaby = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetaby'}),
        # disabled = True  
    )
    nom_etaby = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Etablissement', 'class': 'form-control form-group nom_etaby'}),
        # required=False
    )

class ClasseSpecialiteForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_niveau= forms.CharField(
        label=_('Niveau'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Niveau', 'class': 'form-control form-group nom_niveau' }),
    )
    nom_cycle= forms.CharField(
        label=_('Cycle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Cycle', 'class': 'form-control form-group nom_cycle' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etab',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )
    nom_etab = forms.CharField(
        label=_('Etab'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Etab', 'class': 'form-control form-group nom_etab'}),
        # required=False
    )
    specialite = forms.CharField(
        label=_('Spécialité'),
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Spécialité', 'class': 'form-control form-group specialite'}),
    )
    liste_classes_afficher = forms.CharField(
        label=_('liste_classes'),
        max_length=300,
        widget=forms.TextInput(attrs={'placeholder': '[Classe]', 'class': 'form-control form-group liste_classes_afficher'}),
    )
 
class CoursForm(forms.Form):
    nom_etab = forms.CharField(
        label=_('Etablissement'),
        max_length=100,
        # widget=forms.TextInput(attrs={'placeholder': 'Entrer nom classe', 'class': 'form-control form-group nom_classe' }),
        widget=forms.Select(attrs={'class': 'form-control form-group nom_etab' })
        
    )
    nom_sousetab = forms.CharField(
        label=_('Sous Etablissement'),
        max_length=100,
        widget=forms.Select(attrs={'placeholder': 'Entrer nom Niveau', 'class': 'form-control form-group nom_sousetab' }),
    )
    nom_cycle = forms.CharField(
        label=_('Cycle'),
        max_length=100,
        widget=forms.Select(attrs={'placeholder': 'Entrer nom Cycle', 'class': 'form-control form-group nom_cycle' }),
    )
    nom_classe = forms.CharField(
        label='Classe',
        max_length=100,
        widget=forms.Select(attrs={'placeholder': 'Classe', 'class': 'form-control form-group nom_classe'}),
        # disabled = True  
    )
    nom_matiere = forms.CharField(
        label=_('Cours'),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-group nom_matiere'}),
    )
    code_matiere = forms.CharField(
        label=_('Code'),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-group code_matiere', 'name': 'code_matiere'}),
    )
    coef = forms.FloatField(
        label=_('Coef'),
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group coef', 'name': 'coef'}),
    )
    volume_horaire_hebdo = forms.CharField(
        label=_('Volume Hebdo'),
        widget=forms.TextInput(attrs={'class': 'form-control form-group volume_horaire_hebdo', 'name': 'volume_horaire_hebdo'}),
    )
    volume_horaire_annuel = forms.CharField(
        label=_('Volume Annuel'),
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group volume_horaire_annuel', 'name': 'volume_horaire_annuel'}),
    )

class MatiereForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_matiere= forms.CharField(
        label=_('Matière'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer la Matière', 'class': 'form-control form-group nom_matiere' }),
    )
    code= forms.CharField(
        label=_('Code'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer le Code', 'class': 'form-control form-group code' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )   

class AppellationApprenantFormateurForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    apprenant= forms.CharField(
        label=_('Apprenant'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Appellation Apprenant', 'class': 'form-control form-group appellation_apprenant' }),
    )
    formateur= forms.CharField(
        label=_('Formateur'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Appellation Formateur', 'class': 'form-control form-group appellation_formateur' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etab',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )   

class TypeApprenantForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nom_type_apprenant= forms.CharField(
        label=_('Type Apprenant'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Type Apprenant', 'class': 'form-control form-group nom_type_apprenant' }),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etab',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
        # disabled = True  
    )   

class DisciplineForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    fait= forms.CharField(
        label=_('Titre'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Titre', 'class': 'form-control form-group fait' }),
    )
    description= forms.CharField(
        label=_('Description'),
        max_length=250,
        widget=forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control form-group description' }),
    )
    nb_heures_min= forms.FloatField(
        label=_('# Heures Min'),
        widget=forms.TextInput(attrs={'placeholder': '12', 'class': 'form-control form-group nb_heures_min' }),
    )
    nb_heures_max= forms.FloatField(
        label=_('# Heures Max'),
        widget=forms.TextInput(attrs={'placeholder': '20', 'class': 'form-control form-group nb_heures_max' }),
    )
    sanction = forms.CharField(
        label='Sanction',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sanction', 'class': 'form-control form-group sanction'}),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
    ) 

class ConditionRenvoiForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    nb_heures_max= forms.FloatField(
        label=_('# Heures >'),
        widget=forms.TextInput(attrs={'placeholder': '40', 'class': 'form-control form-group nb_heures_max' }),
    )
    age= forms.FloatField(
        label=_('Age >'),
        widget=forms.TextInput(attrs={'placeholder': '22', 'class': 'form-control form-group age' }),
    )
    moyenne= forms.FloatField(
        label=_('Moyenne <'),
        widget=forms.TextInput(attrs={'placeholder': '7.50', 'class': 'form-control form-group moyenne' }),
    )
    nb_jours= forms.FloatField(
        label=_('# Jours Abs NJ >'),
        widget=forms.TextInput(attrs={'placeholder': '9', 'class': 'form-control form-group nb_jours' }),
    )
    nom_niveau = forms.CharField(
        label='Niveau',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '4e', 'class': 'form-control form-group nom_niveau'}),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
    )

class ConditionSuccesForm(forms.Form):

    moyenne= forms.FloatField(
        label=_('Moyenne >='),
        widget=forms.TextInput(attrs={'placeholder': '10.00', 'class': 'form-control form-group moyenne' }),
    )
    nom_niveau = forms.CharField(
        label='Niveau',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '4e', 'class': 'form-control form-group nom_niveau'}),
    )
    nom_sousetab = forms.CharField(
        label='Sous Etablissement',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sous Etab', 'class': 'form-control form-group nom_sousetab'}),
    )

class TypePayementEleveForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    libelle= forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group libelle', 'name' : 'libelle' }),
    )
    # date_deb= forms.CharField(
    #     max_length=30,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group date_deb', 'name' : 'date_deb' }),
    # )
    # date_fin= forms.CharField(
    #     max_length=30,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group date_fin', 'name' : 'date_fin' }),
    # )
    montant= forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group montant','type' : "number", 'min':'0', 'name' : 'montant' }),
    )
    ordre_paiement= forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control form-group ordre_paiement','type' : "number", 'min':'1', 'name' : 'ordre_paiement' }),
    )
    # entree_sortie_caisee = forms.CharField(
    #     max_length=100,
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control form-group entree_sortie_caisee','name' : 'entree_sortie_caisee'}),
    # ) 
    
class TypePayementPersAdministratifForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    libelle= forms.CharField(
        label=_('Libelle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Libelle', 'class': 'form-control form-group libelle' }),
    )
    type_payement= forms.CharField(
        label=_('Type Payement'),
        max_length=1000,
        widget=forms.TextInput(attrs={'placeholder': 'Type Payement', 'class': 'form-control form-group type_payement' }),
    )
    person= forms.CharField(
        label=_('Concerne'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Concerne', 'class': 'form-control form-group person' }),
    )
    montant= forms.FloatField(
        label=_('Montant'),
        widget=forms.TextInput(attrs={'placeholder': '20', 'class': 'form-control form-group montant' }),
    )
    entree_sortie_caisee = forms.CharField(
        label='E/S de Caisse',
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'E/S Caisse', 'class': 'form-control form-group entree_sortie_caisee'}),
    ) 

class TypePayementDiversForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    libelle= forms.CharField(
        label=_('Libelle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Libelle', 'class': 'form-control form-group libelle' }),
    )
    date_deb= forms.CharField(
        label=_('Date Deb'),
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '16-07-2020', 'class': 'form-control form-group date_deb' }),
    )
    date_fin= forms.CharField(
        label=_('Date Fin'),
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '27-12-2020', 'class': 'form-control form-group date_fin' }),
    )
    montant= forms.FloatField(
        label=_('Montant'),
        widget=forms.TextInput(attrs={'placeholder': '20', 'class': 'form-control form-group montant' }),
    )
    entree_sortie_caisee = forms.CharField(
        label='E/S de Caisse',
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'E/S Caisse', 'class': 'form-control form-group entree_sortie_caisee'}),
    ) 