from django.urls import path
from django.urls import include
from django.conf.urls import url
from TaskRestAPI.viewsKnjizara.POSTViews import *

urlpatterns = [
    path('',login_korisnika,name="nalog"),
    path(r'korisnik_podaci_(?P<pk>\d+)$',Korisnici_podaci.as_view(),name="korisnik_podaci"),
    path(r'lista_korisnika',Korisnici_lista.as_view(),name="lista_korisnika"),
    path(r'narudzbine',Korisnici_narudzbine.as_view(),name="narudzbine"),
    path(r'ocenjivanje_knjiga',Korisnici_ocenjene_knjige.as_view(),name="ocenjivanje_knjiga"),
    path(r'logout',logout_korisnika,name="logout")

]
