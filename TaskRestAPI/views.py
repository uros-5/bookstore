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
from TaskRestAPI.models import *

# Create your views here.


def index(request):
	setupSessionForKorisnik(request)
	najnovijeKnjige = Knjige.objects.values("kategorija", "naslov", "cena","slika","id","ISBN").order_by("-id")[:5].all()
	kategorija1 = list(Knjige.objects.values("kategorija","naslov","opis","autor","cena","slika","ISBN").filter(kategorija="Filozofija")[:3][:])
	for i in range(len(kategorija1)):
		autor = kategorija1[i]["autor"]
		userId = Korisnici.objects.filter(id=autor).values("korisnik_id")[0]["korisnik_id"]
		userr = User.objects.get(id=userId)
		imeIPrezime = userr.first_name + " " + userr.last_name
		kategorija1[i]["autor"] = imeIPrezime



	kategorija2 = list(Knjige.objects.values("kategorija","naslov","opis","autor","cena","slika","ISBN").filter(kategorija="Istorija")[:3][:])
	for i2 in range(len(kategorija2)):
		autor = kategorija2[i2]["autor"]
		userId = Korisnici.objects.filter(id=autor).values("korisnik_id")[0]["korisnik_id"]
		userr = User.objects.get(id=userId)
		imeIPrezime = userr.first_name + " " + userr.last_name
		kategorija2[i2]["autor"] = imeIPrezime

	kategorijaRandom1 = list(Knjige.objects.values("kategorija","naslov","opis","autor","cena","slika","ISBN").filter(kategorija="Ljubavni roman")[:10][:])
	for i3 in range(len(kategorijaRandom1)):
		autor = kategorijaRandom1[i3]["autor"]
		userId = Korisnici.objects.filter(id=autor).values("korisnik_id")[0]["korisnik_id"]
		userr = User.objects.get(id=userId)
		imeIPrezime = userr.first_name + " " + userr.last_name
		kategorijaRandom1[i3]["autor"] = imeIPrezime

	kategorijaRandom2 = list(
		Knjige.objects.values("kategorija","naslov","opis","autor","cena","slika","ISBN").filter(kategorija="Drama")[:10][:])
	for i4 in range(len(kategorijaRandom2)):
		autor = kategorijaRandom2[i4]["autor"]
		userId = Korisnici.objects.filter(id=autor).values("korisnik_id")[0]["korisnik_id"]
		userr = User.objects.get(id=userId)
		imeIPrezime = userr.first_name + " " + userr.last_name
		kategorijaRandom2[i4]["autor"] = imeIPrezime



	return render(request, 'public/index.html', {"najnovijeKnjige":najnovijeKnjige,
												 "kategorija1":kategorija1,
												 "kategorija2":kategorija2,
												 "randKat1":kategorijaRandom1,
												 "randKat2":kategorijaRandom2})



def setupSessionForKorisnik(request):
	if ("korisnikInfoId" not in request.session.keys()):
		if ("_auth_user_id" in request.session.keys()):
			korisnik1 = Korisnici.objects.filter(korisnik_id=request.session["_auth_user_id"])
			if (len(korisnik1) > 0):
				request.session["korisnikInfoId"] = korisnik1[0].id

def komentarisanje(request,idKnjige=""):

	if request.POST:
		form = Komentar_forma(request.POST)

		if form.is_valid():
			putanja = str(request.path)
			komentar = form.cleaned_data["komentar"]
			korisnik = Korisnici.objects.get(id=idKnjige)
			knjiga = Knjige.objects.get(id=idKnjige)

			knk = KomentariNaKnjigama()
			knk.korisnik = korisnik
			knk.knjiga = knjiga
			knk.odobren = False
			knk.komentar = komentar
			knk.save()

			print("komentarisano")
			return HttpResponseRedirect(reverse('index'))
		else:
			return {'form': form}
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