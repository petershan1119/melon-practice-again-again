# Generated by Django 2.0.3 on 2018-03-14 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='artists',
        ),
    ]
