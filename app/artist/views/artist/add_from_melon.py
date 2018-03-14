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
        Artist.objects.update_or_create_from_melon(artist_id)
        return redirect('artist:artist-list')