# Generated by Django 2.1.3 on 2020-10-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20201006_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='score',
            field=models.FloatField(default=-111),
        ),
    ]
