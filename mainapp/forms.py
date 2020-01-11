from django import forms

from django.contrib.auth.models import Group, User

# from .models import Etab, SousEtab

from django.utils.translation import ugettext_lazy as _

class EtudiantForm(forms.Form):
    matricule = forms.CharField(
        label=_('MATRICULE'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE MATRICULE', 'class': 'form-control form-group matricule', 'style': 'text-transform:uppercase' }),
    )
    nom = forms.CharField(
        label='NOM',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'ENTRER VOTRE AGE', 'class': 'form-control form-group nom', 'style': 'text-transform:uppercase'}),
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
        label=_('Libelle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Libelle', 'class': 'form-control form-group libelle' }),
    )
    date_deb= forms.CharField(
        label=_('Date Début'),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': '16-07-2020', 'class': 'form-control form-group date_deb' }),
    )
    date_fin= forms.CharField(
        label=_('Date Fin'),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': '27-09-2020', 'class': 'form-control form-group date_fin' }),
    )
    montant= forms.FloatField(
        label=_('Montant'),
        widget=forms.TextInput(attrs={'placeholder': '20', 'class': 'form-control form-group montant' }),
    )
    classe = forms.CharField(
        label='Classe',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Classe', 'class': 'form-control form-group classe'}),
    )
    entree_sortie_caisee = forms.CharField(
        label='E/S de Caisse',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'E/S de Caisse', 'class': 'form-control form-group entree_sortie_caisee'}),
    ) 
    
class TypePayementPersAdministratifForm(forms.Form):
    # fields = ('nom_etab','date_creation','nom_fondateur','localisation','bp','email','tel','devise','langue','annee_scolaire','site_web')
    libelle= forms.CharField(
        label=_('Libelle'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrer Libelle', 'class': 'form-control form-group libelle' }),
    )
    type_payement= forms.CharField(
        label=_('Type Payement'),
        max_length=250,
        widget=forms.TextInput(attrs={'placeholder': 'Type Payement', 'class': 'form-control form-group type_payement' }),
    )
    person= forms.CharField(
        label=_('Concerne'),
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