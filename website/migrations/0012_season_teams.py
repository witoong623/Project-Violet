# Generated by Django 2.1.2 on 2018-11-25 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20181123_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='teams',
            field=models.ManyToManyField(to='website.Team'),
        ),
    ]
