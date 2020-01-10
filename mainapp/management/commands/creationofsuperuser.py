from django.contrib.auth.models import User
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
            User.objects.create_user(username='user', email='gerard.signe@gmail.com', password='user', is_superuser = True, is_staff = True)
        # super().handle(*args, **options)