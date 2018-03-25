from datetime import datetime
from pathlib import Path

import magic
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from io import BytesIO

from django.db.models.fields.files import FieldFile
from django.forms import model_to_dict

from crawler.artist import ArtistData
from utils.file import download, get_buffer_ext


class ArtistManager(models.Manager):
    def to_dict(self):
        result = []
        for instance in self.get_queryset():
            result.append(instance.to_json())
        return result

    def update_or_create_from_melon(self, artist_id):
        artist = ArtistData(artist_id)
        artist.get_detail()

        name = artist.name
        url_img_cover = artist.url_img_cover
        real_name = artist.personal_information.get('본명', '')
        nationality = artist.personal_information.get('국적', '')
        birth_date_str = artist.personal_information.get('생일', '')
        constellation = artist.personal_information.get('별자리', '')
        blood_type = artist.personal_information.get('혈액형', '')

        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
            else:
                blood_type = Artist.BLOOD_TYPE_OTHER



        artist, artist_created = self.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d') if birth_date_str else None,
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )

        temp_file = download(url_img_cover)
        file_name = '{artist_id}.{ext}'.format(
            artist_id=artist_id,
            ext=get_buffer_ext(temp_file),
        )

        # file_name = Path(url_img_cover).name
        if artist.img_profile:
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))
        return artist, artist_created


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = 'x'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )
    melon_id = models.CharField('멜론 Artist ID', max_length=20, blank=True, null=True, unique=True)
    img_profile = models.ImageField('프로필 이미지', upload_to='artist', blank=True)
    name = models.CharField('이름', max_length=50)
    real_name = models.CharField('본명', max_length=50, blank=True)
    nationality = models.CharField('국적', max_length=50, blank=True)
    birth_date = models.DateField('생년월일', blank=True, null=True)
    constellation = models.CharField('별자리', max_length=30, blank=True)
    blood_type = models.CharField('혈액형', max_length=1, choices=CHOICES_BLOOD_TYPE, blank=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ArtistLike',
        related_name='like_artists',
        blank=True,
    )


    objects = ArtistManager()

    def __str__(self):
        return self.name

    def toggle_like_user(self, user):
        # query = ArtistLike.objects.filter(artist=self, user=user)
        # if query.exists():
        #     query.delete()
        #     return False
        # else:
        #     ArtistLike.objects.create(artist=self, user=user)
        #     return True
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created

    def to_json(self):
        user_class = get_user_model()

        ret = model_to_dict(self)

        def convert_value(value):
            if isinstance(value, FieldFile):
                return value.url if value else None
            elif isinstance(value, user_class):
                return value.pk
            # elif isinstance(value, ArtistYoutube):
            #     return value.pk
            return value


        def convert_obj(obj):
            if isinstance(obj, list):
                for index, item in enumerate(obj):
                    obj[index] = convert_obj(item)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = convert_obj(value)
            return convert_value(obj)

        convert_obj(ret)
        return ret


class ArtistLike(models.Model):
    artist = models.ForeignKey(
        Artist,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_artist_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('artist', 'user')
        )

    def __str__(self):
        return  'ArtistLike (User: {user}, Artist: {artist}, Created: {created})'.format(
            user=self.user.username,
            artist=self.artist.name,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )