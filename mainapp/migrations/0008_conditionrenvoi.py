# Generated by Django 2.1.3 on 2019-12-27 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_discipline_sanction'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionRenvoi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_heures_max', models.FloatField(default=0)),
                ('age', models.FloatField(default=0)),
                ('moyenne', models.FloatField(default=0)),
                ('nb_jours', models.FloatField(default=0)),
                ('id_sousetab', models.IntegerField(default=1)),
                ('nom_sousetab', models.CharField(default='', max_length=100)),
                ('id_niveau', models.IntegerField(default=1)),
                ('nom_niveau', models.CharField(default='', max_length=100)),
                ('archived', models.CharField(default='0', max_length=2)),
            ],
        ),
    ]
