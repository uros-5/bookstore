from django.urls import path
from django.urls import include
from django.conf.urls import url
from TaskRestAPI.viewsKnjizara.POSTViews import *

urlpatterns = [

	path(r'registracija', regpage, name="registracija"),
	path(r'unos_knjige', login_required(Unos_knjiga_forma.as_view()), name="unos_knjige"),
	path(r'dodavanje_u_korpu', dodavanje_knjiga_za_korpu, name="dodavanje_u_korpu"),
	path(r'dodavanje_stavke_narudzbine/', prikaz_korpe, name="dodavanje_stavke_narudzbine"),
	path(r'brisanje_iz_korpe', akcije_za_korpu, name="brisanje_iz_korpe"),
	path(r'smanji_kolicinu', akcije_za_korpu, name="smanji_kolicinu"),
	path(r'povecaj_kolicinu', akcije_za_korpu, name="povecaj_kolicinu"),
	path(r'naruci_iz_korpe', akcije_za_korpu, name="naruci_iz_korpe"),
	# path(r'ocenjivanje_knjiga', login_required(Ocenjivanje_knjiga_forma.as_view()), name="ocenjivanje_knjiga"),
	path(r'ocenjivanje_knjige',ocenjivanje_knjige,name="ocenjivanje_knjige"),
	path(r'komentarisanje_knjiga', login_required(Komentarisanje_knjiga_forma.as_view()), name="komentarisanje_knjiga"),
	path(r'komentarisanje^(?P<idKnjige>.*)$', komentarisanje, name="komentarisanje"),
	path(r'azuriranje',azuriranje,name="azuriranje") 

]
