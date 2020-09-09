from django.urls import path
from Knjizara.viewsKnjizara.POSTViews import *
from Knjizara.viewsKnjizara.knjigeViews import Kategorija_view,knjiga_look

urlpatterns = [


	#UNOS KNJIGA AUTOR
	path(r'unos_knjige', login_required(Unos_knjiga_forma.as_view()), name="unos_knjige"),

	#DODAVANJE U KORPU
	path(r'dodavanje_u_korpu', dodavanje_knjiga_za_korpu, name="dodavanje_u_korpu"),

	#PRIKAZ KORPE
	path(r'korpa/', prikaz_korpe, name="korpa"),

	#BRISANJE IZ KORPE
	path(r'brisanje_iz_korpe', akcije_za_korpu, name="brisanje_iz_korpe"),

	#SMANJIVANJE KOLICINE
	path(r'smanji_kolicinu', akcije_za_korpu, name="smanji_kolicinu"),

	#POVECAVANJE KOLICINE
	path(r'povecaj_kolicinu', akcije_za_korpu, name="povecaj_kolicinu"),

	#NARUCIVANJE KNJIGE/KNJIGA
	path(r'naruci_iz_korpe', akcije_za_korpu, name="naruci_iz_korpe"),

	#OCENJIVANJE JEDNE KNJIGE
	path(r'ocenjivanje_knjige', ocenjivanje_knjige, name="ocenjivanje_knjige"),

	#KOMENTARISANJE KNJIGE
	path(r'komentarisanje^(?P<idKnjige>.*)$', komentarisanje, name="komentarisanje"),

	#AZURIRANJE
	path(r'azuriranje', azuriranje, name="azuriranje"),


	#LINKOVI ZA KATEGORIJE

	path(r'ljubavni_roman/', Kategorija_view.as_view(), name="ljubavni_roman"),
	path(r'ljubavni_roman/<str:ISBN>/',knjiga_look,name="ljubavni_roman_id"),

	path('istorija/', Kategorija_view.as_view(), name="istorija"),
	path(r'istorija/<str:ISBN>/',knjiga_look,name="istorija_id"),

	path('horor/', Kategorija_view.as_view(), name="horor"),
	path(r'horor/<str:ISBN>/',knjiga_look,name="horor_id"),

	path('filozofija/', Kategorija_view.as_view(), name="filozofija"),
	path(r'filozofija/<str:ISBN>/',knjiga_look,name="filozofija_id"),

	path('fantastika/', Kategorija_view.as_view(), name="fantastika"),
	path(r'fantastika/<str:ISBN>/',knjiga_look,name="fantastika_id"),

	path('drama/', Kategorija_view.as_view(), name="drama"),
	path(r'drama/<str:ISBN>/',knjiga_look,name="drama_id"),

	path("pretraga/", Kategorija_view.as_view(), name="pretraga"),
	path(r"pretraga/?page=2", Kategorija_view.as_view(), name="pretraga_id"),

	path(r'autor/', Kategorija_view.as_view(), name="autor"),
	# path(r'autor/<int:id>/',Kategorija_look.as_view(), name="autor")

]
