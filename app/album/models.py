from django.db import models

class Album(models.Model):
    melon_id = models.CharField('멜론 Album ID', max_length=20, blank=True, null=True)
    title = models.CharField('앨범명', max_length=100)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    release_date = models.DateField()

    @property
    def genre(self):
        return ''

    def __str__(self):
        return self.title