from pathlib import Path

import requests
from django.core.files import File
from django.db import models
from io import BytesIO

from crawler.album import AlbumData
from utils.file import download, get_buffer_ext


class AlbumManager(models.Manager):
    def update_or_create_from_melon(self, album_id):
        album_data = AlbumData(album_id)
        album_data.get_detail()
        album, album_created = self.update_or_create(
            melon_id=album_id,
            defaults={
                'title': album_data.title,
                'release_date': album_data.release_date,
            }
        )
        # response = requests.get(album_data.url_img_cover)
        # binary_data = response.content
        # temp_file = BytesIO()
        # temp_file.write(binary_data)
        # temp_file.seek(0)
        # file_name = Path(album_data.url_img_cover).name
        temp_file = download(album_data.url_img_cover)
        file_name = '{album_id}.{ext}'.format(
            album_id=album_id,
            ext=get_buffer_ext(temp_file),
        )
        album.img_cover.save(file_name, File(temp_file))
        return album, album_created


class Album(models.Model):
    melon_id = models.CharField('멜론 Album ID', max_length=20, blank=True, null=True)
    title = models.CharField('앨범명', max_length=100)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    release_date = models.DateField()

    objects = AlbumManager()

    @property
    def genre(self):
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        return self.title