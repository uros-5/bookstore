from django.urls import path
from django.urls import include
from Knjizara import views
from django.conf.urls import url
from Knjizara.models import *
from Knjizara.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

# from Knjizara.views import regpage,Unos_knjiga_forma,Dodavanje_stavki_narudzbine_forma,Ocenjivanje_knjiga_forma,Komentarisanje_knjiga_forma,Korisnici_lista

urlpatterns = [
	# POCETNA STRANICA
	path(r'', views.index, name="index"),

	# LINKOVI SA KNJIGAMA
	path('', include('Knjizara.allUrls.knjige_urls')),

	# LINKOVI KORISNIKA
	path('nalog/', include('Knjizara.allUrls.korisnik_urls')),

	path('pocetna2', views.index2,name="index2")



]
