# Generated by Django 2.1.2 on 2018-10-18 08:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0005_userwatchhistory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userwatchhistory',
            unique_together={('user', 'match')},
        ),
    ]
