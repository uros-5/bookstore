from django.urls import path
from django.urls import include
from TaskRestAPI import views
from django.conf.urls import url
from TaskRestAPI.models import *
from TaskRestAPI.views import *

urlpatterns = [
    path(r'',views.index,name="index"),
    path(r'registracija',Registraciona_forma.as_view(),name="registracija"),
    path(r'unos_knjige',Unos_knjiga_forma.as_view(),name="unos_knjige"),
    path(r'dodavanje_stavke_narudzbine', Dodavanje_stavki_narudzbine_forma.as_view(), name="dodavanje_stavke_narudzbine"),
    path(r'ocenjivanje_knjiga', Ocenjivanje_knjiga_forma.as_view(), name="ocenjivanje_knjiga"),
    path(r'komentarisanje_knjiga', Komentarisanje_knjiga_forma.as_view(
    ), name="komentarisanje_knjiga")
]
