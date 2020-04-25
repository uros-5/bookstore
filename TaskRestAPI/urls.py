from django.urls import path
from django.urls import include
from TaskRestAPI import views
from django.conf.urls import url
from TaskRestAPI.models import *
from TaskRestAPI.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

# from TaskRestAPI.views import regpage,Unos_knjiga_forma,Dodavanje_stavki_narudzbine_forma,Ocenjivanje_knjiga_forma,Komentarisanje_knjiga_forma,Korisnici_lista

urlpatterns = [
    path(r'',views.index,name="index"),
    #deo sajta sa formama
    path(r'registracija',regpage,name="registracija"),
    path(r'unos_knjige',login_required(Unos_knjiga_forma.as_view()),name="unos_knjige"),
    path(r'dodavanje_u_korpu',dodavanje_knjiga_za_korpu,name="dodavanje_u_korpu"),
    path(r'dodavanje_stavke_narudzbine', login_required(prikaz_korpe), name="dodavanje_stavke_narudzbine"),
    path(r'brisanje_iz_korpe',akcije_za_korpu,name="brisanje_iz_korpe"),
    path(r'smanji_kolicinu',akcije_za_korpu,name="smanji_kolicinu"),
    path(r'povecaj_kolicinu',akcije_za_korpu,name="povecaj_kolicinu"),
    path(r'ocenjivanje_knjiga', login_required(Ocenjivanje_knjiga_forma.as_view()), name="ocenjivanje_knjiga"),
    path(r'komentarisanje_knjiga', login_required(Komentarisanje_knjiga_forma.as_view()), name="komentarisanje_knjiga"),


    # informacije korisnika
    path('nalog/',include('TaskRestAPI.korisnik_urls')),

    # linkovi sa knjigama
    path('ljubavni_roman/',include('TaskRestAPI.knjige_urls.ljubavni_roman')),
    path('istorija/',include('TaskRestAPI.knjige_urls.istorija')),
    path('horor/',include('TaskRestAPI.knjige_urls.horor')),
    path('filozofija/',include('TaskRestAPI.knjige_urls.filozofija')),
    path('fantastika/',include('TaskRestAPI.knjige_urls.fantastika')),
    path('drama/',include('TaskRestAPI.knjige_urls.drama'))


]

