from django.shortcuts import render, get_object_or_404

from .models import Album


def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'album/album_list.html', context)


def album_detail(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    context = {
        "album": album,
    }
    return render(request, 'album/album_detail.html', context)

