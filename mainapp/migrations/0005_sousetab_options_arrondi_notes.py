# Generated by Django 2.1.3 on 2020-10-15 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_divisiontempscours_quota_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='sousetab',
            name='options_arrondi_notes',
            field=models.TextField(default='0.25²²0.5²²0.75'),
        ),
    ]