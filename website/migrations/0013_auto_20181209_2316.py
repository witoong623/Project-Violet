# Generated by Django 2.1.3 on 2018-12-09 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_season_teams'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competition',
            old_name='currentSeason',
            new_name='current_season',
        ),
    ]
