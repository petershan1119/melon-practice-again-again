from django.shortcuts import redirect, render

from ...forms import ArtistForm
from ...models import Artist

__all__ = (
    'artist_add',
)


# def artist_add(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         Artist.objects.create(name=name)
#         return redirect('artist:artist-list')
#     else:
#         return render(request, 'artist/artist_add.html')

def artist_add(request):
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list')
    else:
        form = ArtistForm()
    context = {
        'artist_form': form,
    }
    return render(request, 'artist/artist_add.html', context)