# Generated by Django 2.1.4 on 2020-01-18 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20200118_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cours',
            old_name='code_cours',
            new_name='code_matiere',
        ),
    ]
