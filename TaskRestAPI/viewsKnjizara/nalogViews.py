from TaskRestAPI.views import *
from TaskRestAPI.viewsKnjizara.kategorijaViews import oceneKnjiga

# login korisnika
def login_korisnika(request):
	setupSessionForKorisnik(request)

	if ("korpa" not in request.session.keys()):
		request.session["korpa"] = []
	if request.POST:
		form = Form_login(request.POST)
		if (form.is_valid()):
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username, password=password)
			print(user)
			if user:
				print("postoji")
				login(request, user)
				setupSessionForKorisnik(request)
				if request.GET.get('next') is not None:
					return redirect(request.GET['next'])
				return HttpResponseRedirect(reverse('index'))
		else:
			print("pogresno")
			return render(request, 'public/korisnik/nalog.html', {'form': form})
	else:
		form = Form_login()
		return render(request, 'public/korisnik/nalog.html', {'form': form})


class Form_login(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Lozinka", widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(Form_login, self).clean()
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("Wrong login or password!")
		return self.cleaned_data


class Korisnici_podaci(DetailView):
	model = Korisnici
	template_name = 'public/korisnik/korisnik_podaci.html'

	def get_context_data(self, **kwargs):
		context = super(Korisnici_podaci, self).get_context_data(**kwargs)
		if(self.object.id != 1):
			korisnik = Korisnici.objects.get(korisnik_id=self.object.id)
			context["korisnik"] = korisnik
		return context

# za prikaz liste
class Korisnici_lista(ListView):
	model = Korisnici
	template_name = 'public/korisnik/lista_korisnika.html'
	paginate_by = 5

	def get_queryset(self):
		queryset = Korisnici.objects.filter(is_korisnik=True)
		lista = []
		for i in range(len(queryset)):
			recnik = {}
			recnik.setdefault("ulicaIBroj", queryset[i].ulicaIBroj)
			recnik.setdefault("brojPoste", queryset[i].brojPoste)
			recnik.setdefault("grad", queryset[i].grad)
			recnik.setdefault("telefon", queryset[i].telefon)

			user = User.objects.get(id=queryset[i].korisnik_id)
			recnik.setdefault("first_name", user.first_name)
			recnik.setdefault("last_name", user.last_name)
			recnik.setdefault("username", user.username)

			lista.append(recnik)

			user = None

		return lista
class Korisnici_narudzbine(ListView):
	model = Korisnici
	template_name = 'public/korisnik/narudzbine.html'
	paginate_by = 5

	def get_queryset(self):
		narudzbine_korisnika = Narudzbine.objects.filter(korisnik_id=self.request.session["korisnikInfoId"]).order_by("-id")
		narudzbine = []
		if (len(narudzbine_korisnika) > 0):
			narudzbine = []
			# narudzbine = [[{'id':6,'poslato':"ne"},["naslov","cena","kom"],["naslov","cena","kom"]]]
			for i in range(len(narudzbine_korisnika)):
				narudzbina = []
				narudzbina.append(
					{'id': narudzbine_korisnika[i].id, 'placeno': narudzbine_korisnika[i].placeno, 'ukupno': 0,
					 'kolicina': 0, 'datum': narudzbine_korisnika[i].datumNarucivanja})
				stavke_narudzbine = StavkeNarudzbine.objects.filter(narudzbina_id=narudzbine_korisnika[i].id)
				knjige = []

				for i2 in range(len(stavke_narudzbine)):
					knjiga0 = []
					knjiga = Knjige.objects.get(id=stavke_narudzbine[i2].knjiga_id)
					knjiga0.append(knjiga.naslov)
					knjiga0.append(float(knjiga.cena))
					narudzbina[0]['kolicina'] += stavke_narudzbine[i2].kolicina
					narudzbina[0]['ukupno'] += float(knjiga.cena * stavke_narudzbine[i2].kolicina)
					knjiga0.append(stavke_narudzbine[i2].kolicina)
					knjiga0.append(knjiga.slika)
					knjige.append(knjiga0)
				if (len(stavke_narudzbine) > 0):
					narudzbina.append(knjige)
					narudzbina[0]['ukupno'] = round(narudzbina[0]['ukupno'],2)
					narudzbine.append(narudzbina)
		print(len(narudzbine))
		return narudzbine
class Korisnici_ocenjene_knjige(ListView):
	model = Korisnici
	template_name = 'public/korisnik/ocenjene_knjige.html'
	paginate_by = 5

	def get_queryset(self):
		ocene = OceneKnjiga.objects.filter(korisnik_id=self.request.session["korisnikInfoId"])
		lista = []

		for i in range(len(ocene)):
			review = {}
			review.setdefault('ocena', ocene[i].ocena)
			knjiga = Knjige.objects.get(id=ocene[i].knjiga_id)
			review.setdefault('naslov', knjiga.naslov)
			lista.append(review)
		return lista
# logout korisnika
def logout_korisnika(request):
	logout(request)
	return render(request, 'public/korisnik/logout.html')