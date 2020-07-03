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
	path(r'', views.index, name="index"),
	# deo sajta sa formama
	path('', include('TaskRestAPI.POST_urls')),

	# informacije korisnika
	path('nalog/', include('TaskRestAPI.korisnik_urls')),

	# linkovi sa knjigama
	path('', include('TaskRestAPI.kategorija_urls'))
	# (?P<pretraga>.*)

]
