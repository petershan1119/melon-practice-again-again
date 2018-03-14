# Generated by Django 2.0.3 on 2018-03-14 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_auto_20180314_1720'),
        ('song', '0002_remove_song_artists'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artists',
            field=models.ManyToManyField(blank=True, to='artist.Artist', verbose_name='아티스트 목록'),
        ),
    ]
