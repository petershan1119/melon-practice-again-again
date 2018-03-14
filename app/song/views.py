from collections import namedtuple
from typing import NamedTuple

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


# def song_search(request):
#     context = {}
#     # request.GET.get('keyword') vs. request.GET['keyword']
#     keyword = request.GET.get('keyword')
#     # if request.method == "POST":
#     # songs = Song.objects.filter(title__contains=keyword)
#     if keyword:
#         # songs = Song.objects.filter(
#         #     Q(album__title__contains=keyword) |
#         #     Q(title__contains=keyword)
#         # ).distinct()
#         # context['songs'] = songs
#
#         songs_from_albums = Song.objects.filter(album__title__contains=keyword)
#         context['songs_from_albums'] = songs_from_albums
#         songs_from_title = Song.objects.filter(title__contains=keyword)
#         context['songs_from_title'] = songs_from_title
#     return render(request, 'song/song_search.html', context)


def song_search(request):
    context = {
        'song_infos': [],
    }
    keyword = request.GET.get('keyword')

    # SongInfo = namedtuple('SongInfo', ['type', 'q'])

    class SongInfo(NamedTuple):
        type: str
        q: Q

    if keyword:
        # songs_from_albums = Song.objects.filter(album__title__contains=keyword)
        # songs_from_title = Song.objects.filter(title__contains=keyword)
        # context['song_infos'].append({
        #     'type': '앨범명',
        #     'songs': songs_from_albums,
        # })
        # context['song_infos'].append({
        #     'type': '노래제목',
        #     'songs': songs_from_title,
        # })
        song_infos = (
            SongInfo(type='앨범명', q=Q(album__title__contains=keyword)),
            SongInfo(type='노래제목', q=Q(title__contains=keyword)),
        )
        for type, q in song_infos:
            context['song_infos'].append({
                'type': type,
                'songs': Song.objects.filter(q),
            })
    return render(request, 'song/song_search.html', context)