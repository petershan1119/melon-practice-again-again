from django.shortcuts import get_object_or_404, render, redirect

from ...forms import ArtistForm
from ...models import Artist

__all__ = (
    'artist_edit',
)


def artist_edit(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list')
    else:
        form = ArtistForm(instance=artist)
    context = {
        'artist_form': form,
    }
    return render(request, 'artist/artist_edit.html', context)