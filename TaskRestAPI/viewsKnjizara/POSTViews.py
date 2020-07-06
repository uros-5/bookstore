from TaskRestAPI.views import *
from TaskRestAPI.viewsKnjizara.kategorijaViews import oceneKnjiga
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




@login_required
def prikaz_korpe(request):
	korpa = request.session["korpa"]
	stavke = []
	for stavka in korpa:
		knjiga = Knjige.objects.get(ISBN=stavka["knjigaISBN"])
		isbn = knjiga.ISBN
		slika = knjiga.slika
		naslov = knjiga.naslov
		cena = knjiga.cena
		kolicina = stavka["kolicina"]
		stavke.append({"isbn": isbn, "slika": slika, "naslov": naslov, "cena": cena, "kolicina": kolicina}, )
	ukupno = 0
	for i in range(len(stavke)):
		ukupno += stavke[i]["cena"] * stavke[i]["kolicina"]

	return render(request, 'public/knjige/dodavanje_stavke_narudzbine.html',
				  {"korpa": stavke, "ukupno": str(ukupno)})




	# return queryset



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
				return_value.setdefault("poruka",2)
			elif(len(oceneZaKnjigu)<1):
				ocenaObj = OceneKnjiga()
				ocenaObj.knjiga = knjigaObj
				ocenaObj.korisnik_id = int(request.session["korisnikInfoId"])
				ocenaObj.ocena = ocena
				ocenaObj.save()
				return_value.setdefault("poruka",1)
			oceneKnjige = oceneKnjiga(knjigaObj.id,forJson = True)
			return_value.setdefault("oceneKnjige",oceneKnjige)

		except Exception as e:
			print(e)
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

@csrf_exempt
def azuriranje(request):

	return_value = {}
	failedInputs = []
	if len(request.POST) > 0:
		userInfo = request.POST

		korisnik = Korisnici.objects.get(korisnik_id=userInfo["userID"])
		user = User.objects.get(id=userInfo["userID"])


		for i in userInfo:
			value = userInfo[i]

			if(len(value) == 0):
				failedInputs.append(i)
				continue
			else:
				if(i == "first_name"):
					user.first_name = value
				elif(i == "last_name"):
					user.last_name = value
				elif(i == "ulicaIBroj"):
					korisnik.ulicaIBroj = value
				elif(i == "brojPoste"):
					korisnik.brojPoste = value
				elif(i == "telefon"):
					korisnik.telefon = value
		if(len(failedInputs) == 0):
			korisnik.save()
			user.save()
			odgovor = "Uspesno ste azurirali svoje podatke."
			return_value["poruka"] = 1
		else:

			odgovor ="Ispravite {}.".format(failedInputs).replace("'","").replace("[","").replace("]","")
			return_value["poruka"] = 2

		return_value["odgovor"] = odgovor


	return HttpResponse(json.dumps(return_value), content_type=
	"application/json")
