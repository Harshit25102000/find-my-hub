# Generated by Django 4.1.4 on 2022-12-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='people_info',
            name='cluster',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
