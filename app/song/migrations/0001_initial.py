# Generated by Django 2.0.3 on 2018-03-14 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artist', '0001_initial'),
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='멜론 Song ID')),
                ('img_cover', models.ImageField(blank=True, upload_to='song', verbose_name='커버 이미지')),
                ('title', models.CharField(max_length=100, verbose_name='곡 제목')),
                ('genre', models.CharField(max_length=100, verbose_name='장르')),
                ('lyrics', models.TextField(blank=True, verbose_name='가사')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='album.Album', verbose_name='앨범')),
                ('artists', models.ManyToManyField(blank=True, to='artist.Artist', verbose_name='아티스트 목록')),
            ],
        ),
    ]
