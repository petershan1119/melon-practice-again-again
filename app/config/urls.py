"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from members.views import login_view, logout_view, signup_view, facebook_login
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('album/', include('album.urls')),
    path('artist/', include('artist.urls.views')),
    path('song/', include('song.urls')),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('facebook-login/', facebook_login, name='facebook-login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('api/artist/', include('artist.urls.apis')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)