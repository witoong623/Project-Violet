# Generated by Django 2.1.7 on 2019-03-26 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20181209_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='website.Team'),
        ),
    ]