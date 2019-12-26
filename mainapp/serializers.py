from rest_framework import serializers
from mainapp.models import Profil, Etudiant, SousEtab, Etab, Cycle
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
    classe_id = serializers.IntegerField(read_only=True)
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
        instance.classe_id = validated_data.get('classe_id', instance.classe_id)

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