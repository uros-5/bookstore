from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from TaskRestAPI.models import Narudzbine
from django.views.generic import CreateView
from TaskRestAPI.models import *
# Create your views here.

def index(request):
    return render(request,'public/index.html')

class Registraciona_forma(CreateView):
    model = Korisnici
    template_name = 'public/registracija.html'
    success_url = "index"
    fields = ("first_name", "last_name", "username", "email", "password")
class Unos_knjiga_forma(CreateView):
    model = Knjige
    template_name='public/unos_knjige.html'
    success_url="index"
    fields=("naslov","cena","ISBN","kategorija","izdavac")
class Dodavanje_stavki_narudzbine_forma(CreateView):
    model = StavkeNarudzbine
    template_name = 'public/dodavanje_stavke_narudzbine.html'
    success_url = "index"
    fields = ("kolicina", "knjiga")
class Ocenjivanje_knjiga_forma(CreateView):
    model = OceneKnjiga
    template_name = 'public/ocenjivanje_knjiga.html'
    success_url = "index"
    fields = ("ocena",)
class Komentarisanje_knjiga_forma(CreateView):
    model = KomentariNaKnjigama
    template_name = 'public/komentarisanje_knjiga.html'
    success_url = "index"
    fields = ("komentar",)