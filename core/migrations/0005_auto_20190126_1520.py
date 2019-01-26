# Generated by Django 2.1.5 on 2019-01-26 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_scoretable'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoretable',
            name='draw',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoretable',
            name='lost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoretable',
            name='played',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoretable',
            name='point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoretable',
            name='won',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scoretable',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
