from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import CommandError

MAX_SUPERUSER = 2

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        current_nb_superuser = self.UserModel.objects.filter(is_superuser=True).count()
        if current_nb_superuser >= MAX_SUPERUSER:
            raise CommandError("There is no room for you, pass your way!")
        #self.stdout.write(self.style.SUCCESS('...'))
        super().handle(*args, **options)