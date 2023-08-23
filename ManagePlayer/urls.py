from django.urls import path
from .views import addplayer

urlpatterns = [
    path('addplayer', addplayer)
]