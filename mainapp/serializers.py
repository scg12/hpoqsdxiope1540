from rest_framework import serializers
from mainapp.models import Profil, Etudiant, SousEtab, Etab, Cycle, Cours
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'is_active', 'groups')

class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    #photo = serializers.ImageField(max_length=None, use_url=True)
    #photo = serializers.Field('photo.url',read_only = True)
    #photo = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=False)

    class Meta:
        model = Profil
        fields = ('id','telephone', 'ville', 'quartier', 'user','photo_url')

class EtudiantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    matricule = serializers.CharField(max_length=150)
    nom = serializers.CharField(max_length=150)
    prenom = serializers.CharField(max_length=250)
    age = serializers.IntegerField()

    def create(self, validated_data):
        return Etudiant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.matricule = validated_data.get('matricule', instance.matricule.lower())
        instance.nom = validated_data.get('nom', instance.nom.lower())
        instance.prenom = validated_data.get('prenom', instance.prenom.lower())
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        
        return instance

class EleveSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    matricule = serializers.CharField(max_length=30)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=150)
    sexe = serializers.CharField(max_length=2)
    date_naissance = serializers.CharField(max_length=100)
    lieu_naissance = serializers.CharField(max_length=100)
    date_entree = serializers.CharField(max_length=50)
    nom_pere = serializers.CharField(max_length=100)
    prenom_pere = serializers.CharField(max_length=100)
    nom_mere = serializers.CharField(max_length=100)
    prenom_mere = serializers.CharField(max_length=100)
    tel_pere = serializers.CharField(max_length=100)
    tel_mere = serializers.CharField(max_length=100)
    email_pere = serializers.CharField(max_length=100)
    email_mere = serializers.CharField(max_length=100)
    # photo_url = serializers.CharField(max_length=200)
    annee_scolaire = serializers.CharField(max_length=100)
    redouble = serializers.CharField(max_length=2)
    age = serializers.IntegerField()
    # archived = serializers.CharField(max_length=2)

    def create(self, validated_data):
        return Eleve.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.matricule = validated_data.get('matricule', instance.matricule.lower())
        instance.nom = validated_data.get('nom', instance.nom.lower())
        instance.prenom = validated_data.get('prenom', instance.prenom.lower())
        instance.date_naissance = validated_data.get('date_naissance', instance.date_naissance.lower())
        instance.lieu_naissance = validated_data.get('lieu_naissance', instance.lieu_naissance.lower())
        instance.date_entree = validated_data.get('date_entree', instance.date_entree.lower())
        instance.nom_pere = validated_data.get('nom_pere', instance.nom_pere.lower())
        instance.prenom_pere = validated_data.get('prenom_pere', instance.prenom_pere.lower())
        instance.nom_mere = validated_data.get('nom_mere', instance.nom_mere.lower())
        instance.prenom_mere = validated_data.get('prenom_mere', instance.prenom_mere.lower())
        instance.tel_pere = validated_data.get('tel_pere', instance.tel_pere.lower())
        instance.tel_mere = validated_data.get('tel_mere', instance.tel_mere.lower())
        instance.email_pere = validated_data.get('email_pere', instance.email_pere.lower())
        instance.email_mere = validated_data.get('email_mere', instance.email_mere.lower())
        # instance.photo_url = validated_data.get('photo_url', instance.photo_url.lower())
        instance.annee_scolaire = validated_data.get('annee_scolaire', instance.annee_scolaire.lower())
        instance.redouble = validated_data.get('redouble', instance.redouble.lower())
        instance.age = validated_data.get('age', instance.age.lower())
        # instance.archived = validated_data.get('archived', instance.archived.lower())

        instance.save()
        
        return instance

class CycleSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    cycle_id = serializers.IntegerField(read_only=True)
    nom_etab = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)
    nom_cycle = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Cycle.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_etab = validated_data.get('nom_etab', instance.nom_etab.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.nom_cycle = validated_data.get('nom_cycle', instance.nom_cycle.lower())
        instance.cycle_id = validated_data.get('cycle_id', instance.cycle_id)

class EtabSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nom_etab = serializers.CharField(max_length=150)
    date_creation = serializers.CharField(max_length=150)
    nom_fondateur = serializers.CharField(max_length=150)
    localisation = serializers.CharField(max_length=150)
    bp = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)
    tel = serializers.CharField(max_length=150)
    devise = serializers.CharField(max_length=150)
    langue = serializers.CharField(max_length=150)
    annee_scolaire = serializers.CharField(max_length=150)
    site_web = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Etab.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_etab = validated_data.get('nom_etab', instance.nom_etab.lower())
        instance.date_creation = validated_data.get('date_creation', instance.date_creation.lower())
        instance.nom_fondateur = validated_data.get('nom_fondateur', instance.nom_fondateur.lower())
        instance.localisation = validated_data.get('localisation', instance.localisation.lower())
        instance.bp = validated_data.get('bp', instance.bp.lower())
        instance.email = validated_data.get('email', instance.email.lower())
        instance.tel = validated_data.get('tel', instance.tel.lower())
        instance.devise = validated_data.get('devise', instance.devise.lower())
        instance.langue = validated_data.get('langue', instance.langue.lower())
        instance.annee_scolaire = validated_data.get('annee_scolaire', instance.annee_scolaire.lower())
        instance.site_web = validated_data.get('langue', instance.site_web.lower())

class SousEtabSerializer(serializers.Serializer):
    """docstring for SousEtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nom_sousetab = serializers.CharField(max_length=150)
    date_creation = serializers.CharField(max_length=150)
    nom_fondateur = serializers.CharField(max_length=150)
    localisation = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return SousEtab.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.date_creation = validated_data.get('date_creation', instance.date_creation.lower())
        instance.nom_fondateur = validated_data.get('nom_fondateur', instance.nom_fondateur.lower())
        instance.localisation = validated_data.get('localisation', instance.localisation.lower())

class SousEtabConfigSerializer(serializers.Serializer):
    """docstring for SousEtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nom_sousetab = serializers.CharField(max_length=150)
    format_matricule = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return SousEtab.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.format_matricule = validated_data.get('format_matricule', instance.format_matricule.lower())

class NiveauSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    niveau_id = serializers.IntegerField(read_only=True)
    nom_etab = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)
    nom_cycle = serializers.CharField(max_length=150)
    nom_niveau = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Niveau.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_etab = validated_data.get('nom_etab', instance.nom_etab.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.nom_cycle = validated_data.get('nom_cycle', instance.nom_cycle.lower())
        instance.nom_niveau = validated_data.get('nom_niveau', instance.nom_niveau.lower())
        instance.niveau_id = validated_data.get('niveau_id', instance.niveau_id)

class ClasseSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nom_etab = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)
    nom_cycle = serializers.CharField(max_length=150)
    nom_niveau = serializers.CharField(max_length=150)
    nom_classe = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Classe.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_etab = validated_data.get('nom_etab', instance.nom_etab.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.nom_cycle = validated_data.get('nom_cycle', instance.nom_cycle.lower())
        instance.nom_niveau = validated_data.get('nom_niveau', instance.nom_niveau.lower())
        instance.nom_classe = validated_data.get('nom_classe', instance.nom_classe.lower())
        # instance.classe_id = validated_data.get('id', instance.id)

class CoursSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    nom_matiere = serializers.CharField(max_length=150)
    id_matiere = serializers.IntegerField(default=1)
    code_matiere = serializers.CharField(max_length=150)
    coef = serializers.FloatField()
    volume_horaire_hebdo = serializers.IntegerField()
    volume_horaire_annuel = serializers.IntegerField()
    nom_cycle = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)
    nom_etab = serializers.CharField(max_length=150)
    nom_classe = serializers.CharField(max_length=150)
    id_cycle = serializers.IntegerField(default=1)
    id_classe = serializers.IntegerField(default=1)
    id_sousetab = serializers.IntegerField(default=1)
    id_etab = serializers.IntegerField(default=1)

    def create(self, validated_data):
        return Classe.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.nom_matiere = validated_data.get('nom_matiere', instance.nom_matiere.lower())
        instance.id_matiere = validated_data.get('id_matiere', instance.id_matiere)
        instance.code_matiere = validated_data.get('code_matiere', instance.code_matiere.lower())
        instance.coef = validated_data.get('coef', instance.coef)
        instance.volume_horaire_hebdo = validated_data.get('volume_horaire_hebdo', instance.volume_horaire_hebdo)
        instance.volume_horaire_annuel = validated_data.get('volume_horaire_annuel', instance.volume_horaire_annuel)
        instance.nom_cycle = validated_data.get('nom_cycle', instance.nom_cycle.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())
        instance.nom_etab = validated_data.get('nom_etab', instance.nom_etab.lower())
        instance.nom_classe = validated_data.get('nom_classe', instance.nom_classe.lower())
        instance.id_cycle = validated_data.get('id_cycle', instance.id_cycle)
        instance.id_classe = validated_data.get('id_classe', instance.id_classe)
        instance.id_sousetab = validated_data.get('id_sousetab', instance.id_sousetab)
        instance.id_etab = validated_data.get('id_etab', instance.id_etab)




class MatiereSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    matiere_id = serializers.IntegerField(read_only=True)
    nom_matiere = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Matiere.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.matiere_id = validated_data.get('matiere_id', instance.matiere_id)
        instance.nom_matiere = validated_data.get('nom_matiere', instance.nom_matiere.lower())
        instance.code = validated_data.get('code', instance.code.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class AppellationApprenantFormateurSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    appellation_apprenant = serializers.CharField(max_length=150)
    appellation_formateur = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return AppellationApprenantFormateur.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.appellation_apprenant = validated_data.get('appellation_apprenant', instance.appellation_apprenant.lower())
        instance.appellation_formateur = validated_data.get('appellation_formateur', instance.appellation_formateur.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class TypeApprenantSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nom_type_apprenant = serializers.CharField(max_length=150)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return TypeApprenant.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.matiere_id = validated_data.get('id', instance.id)
        instance.nom_type_apprenant = validated_data.get('nom_type_apprenant', instance.nom_type_apprenant.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class DisciplineSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    fait = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=250)
    nb_heures_min = serializers.FloatField()
    nb_heures_max = serializers.FloatField()
    nb_heures_max = serializers.FloatField()
    sanction = serializers.CharField(max_length=250)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Discipline.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.fait = validated_data.get('fait', instance.fait.lower())
        instance.description = validated_data.get('description', instance.description.lower())
        instance.nb_heures_min = validated_data.get('nb_heures_min', instance.nb_heures_min.lower())
        instance.nb_heures_max = validated_data.get('nb_heures_max', instance.nb_heures_max.lower())
        instance.sanction = validated_data.get('sanction', instance.sanction.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class ConditionRenvoiSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    nb_heures_max = serializers.FloatField()
    age = serializers.FloatField()
    moyenne = serializers.FloatField()
    nb_jours = serializers.FloatField()
    nom_niveau = serializers.CharField(max_length=250)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return ConditionRenvoi.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.nb_heures_max = validated_data.get('nb_heures_max', instance.nb_heures_max)
        instance.age = validated_data.get('age', instance.age)
        instance.moyenne = validated_data.get('moyenne', instance.moyenne)
        instance.nb_jours = validated_data.get('nb_jours', instance.nb_jours)
        instance.nom_niveau = validated_data.get('nom_niveau', instance.nom_niveau.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class ConditionSuccesSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    moyenne = serializers.FloatField()
    nom_niveau = serializers.CharField(max_length=250)
    nom_sousetab = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return ConditionSucces.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.moyenne = validated_data.get('moyenne', instance.moyenne)
        instance.nom_niveau = validated_data.get('nom_niveau', instance.nom_niveau.lower())
        instance.nom_sousetab = validated_data.get('nom_sousetab', instance.nom_sousetab.lower())

class TypePayementEleveSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    libelle = serializers.CharField(max_length=150)
    date_deb = serializers.CharField(max_length=20)
    date_fin = serializers.CharField(max_length=20)
    entree_sortie_caisee = serializers.CharField(max_length=20)
    montant = serializers.FloatField()
    # classe = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return TypePayementEleve.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.libelle = validated_data.get('libelle', instance.libelle.lower())
        instance.date_deb = validated_data.get('date_deb', instance.date_deb.lower())
        instance.date_fin = validated_data.get('date_fin', instance.date_fin.lower())
        instance.entree_sortie_caisee = validated_data.get('entree_sortie_caisee', instance.entree_sortie_caisee.lower())
        instance.montant = validated_data.get('montant', instance.montant.lower())
        # instance.classe = validated_data.get('classe', instance.classe.lower())

class TypePayementPersAdministratifSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    libelle = serializers.CharField(max_length=150)
    type_payement = serializers.CharField(max_length=150)
    person = serializers.CharField(max_length=150)
    entree_sortie_caisee = serializers.CharField(max_length=5)
    montant = serializers.FloatField()

    def create(self, validated_data):
        return TypePayementAdminStaff.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.libelle = validated_data.get('libelle', instance.libelle.lower())
        instance.type_payement = validated_data.get('type_payement', instance.type_payement.lower())
        instance.person = validated_data.get('person', instance.person.lower())
        instance.entree_sortie_caisee = validated_data.get('entree_sortie_caisee', instance.entree_sortie_caisee.lower())
        instance.montant = validated_data.get('montant', instance.montant.lower())

class TypePayementDiversSerializer(serializers.Serializer):
    """docstring for EtabSerializer"""
    id = serializers.IntegerField(read_only=True)
    libelle = serializers.CharField(max_length=150)
    date_deb = serializers.CharField(max_length=20)
    date_fin = serializers.CharField(max_length=150)
    entree_sortie_caisee = serializers.CharField(max_length=5)
    montant = serializers.FloatField()

    def create(self, validated_data):
        return TypePayementDivers.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.libelle = validated_data.get('libelle', instance.libelle.lower())
        instance.date_deb = validated_data.get('date_deb', instance.date_deb.lower())
        instance.date_fin = validated_data.get('date_fin', instance.date_fin.lower())
        instance.entree_sortie_caisee = validated_data.get('entree_sortie_caisee', instance.entree_sortie_caisee.lower())
        instance.montant = validated_data.get('montant', instance.montant.lower())
