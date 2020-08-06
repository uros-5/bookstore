from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json
#sve ove importe koriste views iz viewsKnjizara
from django.contrib.auth.decorators import login_required
from Knjizara.models import *
from Knjizara.utils import Korpa as korpa
from Knjizara.utils import Knjiga as knjiga

# Create your views here.



def index(request):
	#PRVA FUNKCIJA SE DO KRAJA IZVRSAVA NAKON LOG-IN-A
	setupSessionForKorisnik(request)

	najnovijeKnjige = knjiga.getNajnovije()

	filozofijaKnjige = knjiga.getKategorija("Filozofija",3)

	istorijaKnjige = knjiga.getKategorija("Istorija",3)

	ljubavniRomanKnjige = knjiga.getKategorija("Ljubavni roman",10)

	dramaKnjige = knjiga.getKategorija("Drama",10)


	return render(request, 'public/index.html', {"najnovijeKnjige":najnovijeKnjige,
												 "filozofijaKnjige":knjiga.dodavanjeIAutora(filozofijaKnjige),
												 "istorijaKnjige":knjiga.dodavanjeIAutora(istorijaKnjige),
												 "ljubavniRomanKnjige":knjiga.dodavanjeIAutora(ljubavniRomanKnjige),
												 "dramaKnjige":knjiga.dodavanjeIAutora(dramaKnjige)})




def setupSessionForKorisnik(request):
	# print(type(request.session["_auth_user_id"]))
	if ("korisnikInfoId" not in request.session.keys()):
		if ("_auth_user_id" in request.session.keys()):
			korisnik1 = Korisnici.objects.filter(korisnik_id=request.session["_auth_user_id"])
			if (len(korisnik1) > 0):
				request.session["korisnikInfoId"] = korisnik1[0].id


	if ("korpa" not in request.session.keys()):
		request.session["korpa"] = []

def komentarisanje(request,idKnjige=""):
	#utils korpa se koristi iako nema veze sa korpom
	zahtev = korpa.proveraZahteva(request, Komentar_forma)
	# zahtev = [True,form]

	if(zahtev[0] == True):
		putanja = str(request.path)
		komentar = zahtev[1].cleaned_data["komentar"]
		korisnikObj = Korisnici.objects.get(id=int(request.session["korisnikInfoId"]))
		knjigaObj = Knjige.objects.get(id=idKnjige)
		knk = KomentariNaKnjigama()

		knjiga.komentarisanjeKnjige(komentar,korisnikObj,knjigaObj,knk)

		return HttpResponseRedirect(reverse('index'))

	else:
		form = Komentar_forma()
		return {'form': form}

class Komentar_forma(forms.Form):
	komentar = forms.CharField(label="komentar", max_length=50)

	def clean(self):
		cleaned_data = super(Komentar_forma, self).clean()
		komentarDuzina = len(self.cleaned_data.get("komentar"))
		if komentarDuzina < 0 and komentarDuzina > 50:
			raise forms.ValidationError("Komentar treba da je max 50 karaktera!")
		return self.cleaned_data