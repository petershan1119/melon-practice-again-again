from django.shortcuts import redirect

from ...models import Artist


__all__ = (
    'artist_like_toggle',
)


def artist_like_toggle(request, artist_pk):
    artist = Artist.objects.get(pk=artist_pk)
    if request.method == "POST":
        artist.toggle_like_user(user=request.user)
        next_path = request.POST.get('next-path', 'artist:artist-list')
        return redirect(next_path)