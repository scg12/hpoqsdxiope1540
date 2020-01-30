from django.conf import settings
from django.contrib.auth.models import User
from mainapp.models import Profil
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser


MAX_SUPERUSER = 2

class Command(createsuperuser.Command):
    help = 'Create Super user'

    def handle(self, *args, **kwargs):
        current_nb_superuser = self.UserModel.objects.filter(is_superuser=True).count()
        if current_nb_superuser >= MAX_SUPERUSER:
            raise CommandError("There is no room for you, pass your way!")
        else:
            user_ulrich = User.objects.create_user(username='ulrich', email='ulrichguebayie@gmail.com', password='ABCDE2019', is_superuser = True, is_staff = True)
            user_gerard = User.objects.create_user(username='gerard', email='gerard.signe@gmail.com', password='ABCDE2019', is_superuser = True, is_staff = True)


            # Nous créons un nouveau profil utilisateur en associant avec l'utilisateur deja créé
            profil = Profil(
            user = user_ulrich, 
            telephone = "+237676069452",
            ville = "Yaoundé",
            quartier = "Rond Point Nlongkak",
            )
            profil.save()

            profil = Profil(
            user = user_gerard, 
            telephone = "+237674905841",
            ville = "Yaoundé",
            quartier = "Ecole Des Postes",
            )
            profil.save()

            # super().handle(*args, **options)