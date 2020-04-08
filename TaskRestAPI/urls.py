from django.urls import path
from django.urls import include
from TaskRestAPI import views
from django.conf.urls import url
from TaskRestAPI.models import *
from TaskRestAPI.views import *
from django.contrib.auth.decorators import login_required
# from TaskRestAPI.views import regpage,Unos_knjiga_forma,Dodavanje_stavki_narudzbine_forma,Ocenjivanje_knjiga_forma,Komentarisanje_knjiga_forma,Korisnici_lista

urlpatterns = [
    path(r'',views.index,name="index"),
    #deo sajta sa formama
    path(r'registracija',regpage,name="registracija"),
    path(r'unos_knjige',login_required(Unos_knjiga_forma.as_view()),name="unos_knjige"),
    path(r'dodavanje_stavke_narudzbine', login_required(Dodavanje_stavki_narudzbine_forma.as_view()), name="dodavanje_stavke_narudzbine"),
    path(r'ocenjivanje_knjiga', login_required(Ocenjivanje_knjiga_forma.as_view()), name="ocenjivanje_knjiga"),
    path(r'komentarisanje_knjiga', login_required(Komentarisanje_knjiga_forma.as_view()), name="komentarisanje_knjiga"),

    #deo sajta za login
    path(r'login',views.login_korisnika,name="login"),
    path(r'logout',views.logout_korisnika,name="logout"),

    # informacije korisnika
    path(r'korisnik_podaci_(?P<pk>\d+)$',Korisnici_podaci.as_view(),name="korisnik_podaci"),
    path(r'lista_korisnika',Korisnici_lista.as_view(),name="lista_korisnika"),
    path(r'narudzbine',Korisnici_narudzbine.as_view(),name="narudzbine")
]
