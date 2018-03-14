from datetime import datetime
from pathlib import Path

import requests
from django.core.files import File
from django.shortcuts import redirect
from io import BytesIO

from ...models import Artist
from crawler.artist import ArtistData

__all__ = (
    'artist_add_from_melon',
)

def artist_add_from_melon(request):
    if request.method == "POST":
        artist_id = request.POST['artist_id']
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

        response = requests.get(url_img_cover)
        binary_data = response.content
        temp_file = BytesIO()
        temp_file.write(binary_data)
        temp_file.seek(0)

        artist, created = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d'),
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )

        file_name = Path(url_img_cover).name
        artist.img_profile.save(file_name, File(temp_file))

        return redirect('artist:artist-list')