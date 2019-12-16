from rest_framework import serializers
from mainapp.models import Profil, Etudiant
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




# class ProfilSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     telephone = serializers.CharField(max_length=150)
#     ville = serializers.CharField(max_length=150)
#     quartier = serializers.CharField(max_length=250)
#     user = UserSerializer(read_only = True)
#     photo = serializers.ImageField(max_length=None, use_url=True)
    

#     def create(self, validated_data):
#         return Profil.objects.create(**validated_data)


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
