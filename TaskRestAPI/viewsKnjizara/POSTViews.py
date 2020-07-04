from TaskRestAPI.views import *

# registracija
def regpage(request):
	if request.POST:
		form = Registraciona_forma(request.POST)

		if form.is_valid():

			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			userType = form.cleaned_data["userType"]

			novi_korisnik = User.objects.create_user(username=username,
													 email=email,
													 password=password
													 )
			novi_korisnik.is_active = True
			novi_korisnik.first_name = first_name
			novi_korisnik.last_name = last_name
			novi_korisnik.save()

			korisnik = Korisnici()
			korisnik.korisnik = novi_korisnik

			if (str(userType) == "korisnik"):
				korisnik.is_korisnik = True
			elif (str(userType) == "autor"):
				korisnik.is_autor = True
			korisnik.save()
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, 'public/korisnik/registracija.html', {'form': form})
	else:

		form = Registraciona_forma()
		return render(request, 'public/korisnik/registracija.html', {'form': form})

class Registraciona_forma(forms.Form):
	first_name = forms.CharField(label="first_name", max_length=30)
	last_name = forms.CharField(label="last_name", max_length=150)
	username = forms.CharField(label="username", max_length=150)
	email = forms.EmailField(label="email")
	password = forms.CharField(label="password", widget=forms.PasswordInput)
	password_bis = forms.CharField(label="password", widget=forms.PasswordInput)
	CHOICES = (('korisnik', 'korisnik'),
			   ('autor', 'autor'))
	userType = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

	def clean(self):
		cleaned_data = super(Registraciona_forma, self).clean()
		password = self.cleaned_data.get("password")
		password_bis = self.cleaned_data.get("password_bis")
		if password and password_bis and password != password_bis:
			raise forms.ValidationError("Sifre nisu iste!")
		return self.cleaned_data

	# unosne forme

	# class Registraciona_forma(CreateView):
	# model = Korisnici
	# template_name = 'public/registracija.html'
	# success_url = "index"
	# fields = ("first_name", "last_name", "username", "email", "password")
class Unos_knjiga_forma(CreateView):
	model = Knjige
	template_name = 'public/knjige/unos_knjige.html'
	success_url = "index"
	fields = ("naslov", "cena", "ISBN", "kategorija", "izdavac")

	def get_context_data(self, **kwargs):
		context = super(Unos_knjiga_forma, self).get_context_data(**kwargs)
		korisnici = Korisnici.objects.filter(is_autor=True)
		lista = []
		for i in range(len(korisnici)):
			lista.append(korisnici[i].korisnik_id)
		context['ids'] = lista
		return context


class Dodavanje_stavki_narudzbine_forma(CreateView):
	model = StavkeNarudzbine
	template_name = 'public/knjige/dodavanje_stavke_narudzbine.html'
	success_url = "index"
	fields = ("kolicina", "knjiga")


class Ocenjivanje_knjiga_forma(CreateView):
	model = OceneKnjiga
	template_name = 'public/knjige/ocenjivanje_knjiga.html'
	success_url = "index"
	fields = ("ocena",)


class Komentarisanje_knjiga_forma(CreateView):
	model = KomentariNaKnjigama
	template_name = 'public/knjige/komentarisanje_knjiga.html'
	success_url = "index"
	fields = ("komentar",)


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


# logout korisnika
def logout_korisnika(request):
	logout(request)
	return render(request, 'public/korisnik/logout.html')


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

	# return queryset


class Korisnici_podaci(DetailView):
	model = Korisnici
	template_name = 'public/korisnik/korisnik_podaci.html'

	def get_context_data(self, **kwargs):
		context = super(Korisnici_podaci, self).get_context_data(**kwargs)
		korisnik = Korisnici.objects.get(korisnik_id=self.object.id)
		context["korisnik"] = korisnik
		return context


class Korisnici_narudzbine(ListView):
	model = Korisnici
	template_name = 'public/korisnik/narudzbine.html'
	paginate_by = 5

	def get_queryset(self):
		narudzbine_korisnika = Narudzbine.objects.filter(korisnik_id=self.request.session["korisnikInfoId"])
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

@csrf_exempt
def ocenjivanje_knjige(request):

	return_value = {}
	if len(request.POST) > 0:
		try:

			knjigaISBN = request.POST["knjigaISBN"]
			ocena = request.POST["ocena"]
			knjigaObj = Knjige.objects.get(ISBN=knjigaISBN)
			oceneZaKnjigu = OceneKnjiga.objects.filter(korisnik_id=int(request.session["korisnikInfoId"]),knjiga_id=knjigaObj.id)

			if(len(oceneZaKnjigu)>0):
				oceneZaKnjigu[0].ocena = ocena
				oceneZaKnjigu[0].save()
				return_value.setdefault("poruka",1)
			elif(len(oceneZaKnjigu)<1):
				ocenaObj = OceneKnjiga()
				ocenaObj.knjiga = knjigaObj
				ocenaObj.korisnik_id = int(request.session["korisnikInfoId"])
				ocenaObj.ocena = ocena
				ocenaObj.save()
				return_value.setdefault("poruka", 2)

		except:
			print("greska")
	print(return_value)
	return HttpResponse(json.dumps(return_value), content_type=
		"application/json")

@csrf_exempt
def akcije_za_korpu(request):
	return_value = {}
	if len(request.POST) > 0:
		radnja = request.POST["radnja"]
		try:
			knjiga = request.POST["knjigaISBN"]
		except:
			korpa = request.session["korpa"][:]

		if (radnja == "brisanje"):
			korpa = request.session["korpa"]
			for i in range(len(korpa)):
				if (korpa[i]["knjigaISBN"] == knjiga):
					del korpa[i]
					request.session["korpa"] = korpa
					return_value.setdefault("knjigaISBN", knjiga)
					return_value.setdefault("poruka", 2)
					break
		elif (radnja == "oduzimanje"):
			korpa = request.session["korpa"]
			for i in range(len(korpa)):
				if (korpa[i]["knjigaISBN"] == knjiga):
					kolicina = korpa[i]["kolicina"]
					if (kolicina > 1):
						kolicina -= 1
						korpa[i]["kolicina"] = kolicina
					request.session["korpa"] = korpa
					return_value.setdefault("knjigaISBN", knjiga)
					return_value.setdefault("poruka", 3)
					return_value.setdefault("kolicina", kolicina)
					break
		elif (radnja == "dodavanje"):
			korpa = request.session["korpa"]
			for i in range(len(korpa)):
				if (korpa[i]["knjigaISBN"] == knjiga):
					kolicina = korpa[i]["kolicina"]
					if (kolicina <= 11):
						kolicina += 1
						korpa[i]["kolicina"] = kolicina
					request.session["korpa"] = korpa
					return_value.setdefault("knjigaISBN", knjiga)
					return_value.setdefault("poruka", 4)
					return_value.setdefault("kolicina", kolicina)
					break
		elif (radnja == "narucivanje"):

			korisnik = Korisnici.objects.get(id=int(request.session["korisnikInfoId"]))

			narudzbina = Narudzbine(korisnik=korisnik)
			narudzbina.datumNarucivanja = timezone.now()
			narudzbina.placeno = False
			narudzbina.save()
			for i in range(len(korpa)):
				# request.session["korisnikInfoId"]

				kolicina = korpa[0]["kolicina"]

				stavkeNarudzbine = StavkeNarudzbine()
				stavkeNarudzbine.knjiga = Knjige.objects.filter(ISBN=korpa[0]["knjigaISBN"])[0]
				stavkeNarudzbine.kolicina = kolicina
				stavkeNarudzbine.narudzbina = narudzbina
				stavkeNarudzbine.save()

				del korpa[0]
			request.session["korpa"] = korpa
			return_value.setdefault("poruka", 1)
			return_value.setdefault("knjigaISBN", "000000")

				# narudzbina.

				# print(korpa[i]["cena"])

	return HttpResponse(json.dumps(return_value), content_type=
	"application/json")

class Forms__za_korpu(forms.Form):
	knjigaISBN = forms.CharField()
	kolicina = forms.IntegerField()


@csrf_exempt
def dodavanje_knjiga_za_korpu(request):
	return_value = "0"
	if len(request.POST) > 0:
		form = Forms__za_korpu(request.POST)
		if form.is_valid():
			stavke = request.session['korpa']
			knjigaISBN = form.cleaned_data["knjigaISBN"]
			kolicina = form.cleaned_data["kolicina"]
			stavka = {}
			provera = False
			for i in stavke:
				if (i["knjigaISBN"] == knjigaISBN):
					print("knjiga je vec u korpi")
					provera = True
					return_value = 5
			if (provera == False):
				stavka.setdefault("knjigaISBN", knjigaISBN)
				stavka.setdefault("kolicina", int(kolicina))
				stavke.append(stavka)
				request.session["korpa"] = stavke
				return_value = 1
	return HttpResponse(json.dumps(return_value), content_type=
	"application/json")



