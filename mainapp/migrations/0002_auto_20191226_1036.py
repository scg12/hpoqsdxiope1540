# Generated by Django 2.1.3 on 2019-12-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appellationapprenantformateur',
            name='id_sousetab',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='appellationapprenantformateur',
            name='nom_sousetab',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appellationmodulechapitrelecon',
            name='id_sousetab',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='appellationmodulechapitrelecon',
            name='nom_sousetab',
            field=models.CharField(default='', max_length=100),
        ),
    ]
