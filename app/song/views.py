from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .models import Song


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    return render(request, 'song/song_list.html', context)


def song_search(request):
    context = {}
    # request.GET.get('keyword') vs. request.GET['keyword']
    keyword = request.GET.get('keyword')
    # if request.method == "POST":
    # songs = Song.objects.filter(title__contains=keyword)
    if keyword:
        # songs = Song.objects.filter(
        #     Q(album__title__contains=keyword) |
        #     Q(title__contains=keyword)
        # ).distinct()
        # context['songs'] = songs

        songs_from_albums = Song.objects.filter(album__title__contains=keyword)
        context['songs_from_albums'] = songs_from_albums
        songs_from_title = Song.objects.filter(title__contains=keyword)
        context['songs_from_title'] = songs_from_title
    return render(request, 'song/song_search.html', context)