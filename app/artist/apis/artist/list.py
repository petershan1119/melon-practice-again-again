import json

from django.http import JsonResponse, HttpResponse

from ...models import Artist

__all__ = (
    'artist_list',
)


def artist_list(request):
    artists = Artist.objects.all()
    # data = {
    #     'artists': artists,
    # }

    # artist_data_list = []
    # for artist in artists:
    #     artist_data = {
    #         'melon_id': artist.melon_id,
    #         'name': artist.name,
    #     }
    #     artist_data_list.append(artist_data)
    #
    # data = {
    #     'artists': artist_data_list,
    # }
    data = {
        'artists': [artist.to_json() for artist in artists],
    }
    # return HttpResponse(json.dump(data), content_type="application/json")
    return JsonResponse(data)