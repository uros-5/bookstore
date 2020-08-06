from django.urls import path
from Knjizara.viewsKnjizara.nalogViews import *

urlpatterns = [

    #NALOG LOG IN
    path('',login_korisnika,name="nalog"),

	# REGISTRACIJA
    path(r'registracija', regpage, name="registracija"),

    #PODACI KORISNIKA
    path(r'korisnik_podaci_(?P<pk>\d+)$',Korisnici_podaci.as_view(),name="korisnik_podaci"),

    #NARUDZBINE KORISNIKA
    path(r'narudzbine',Korisnici_narudzbine.as_view(),name="narudzbine"),

    #SVE OCENJENE KNJIGE KORISNIKA
    path(r'ocenjene_knjige',Korisnici_ocenjene_knjige.as_view(),name="ocenjene_knjige"),

    #LOGOUT KORISNIKA
    path(r'logout',logout_korisnika,name="logout")

]
