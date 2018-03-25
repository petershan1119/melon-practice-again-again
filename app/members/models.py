from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def toggle_like_artist(self, artist):
        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created