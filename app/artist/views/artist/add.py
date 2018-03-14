from django.shortcuts import redirect, render

from ...models import Artist

__all__ = (
    'artist_add',
)


def artist_add(request):
    if request.method == "POST":
        name = request.POST['name']
        Artist.objects.create(name=name)
        return redirect('artist:artist-list')
    else:
        return render(request, 'artist/artist_add.html')
