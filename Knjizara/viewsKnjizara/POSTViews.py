from Knjizara.views import *
# from Knjizara.viewsKnjizara.knjigeViews import oceneKnjiga
from Knjizara.utils import Korpa as korpa
from Knjizara.utils import Knjiga as knjiga

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

class Forms__za_korpu(forms.Form):
	knjigaISBN = forms.CharField()
	kolicina = forms.IntegerField()


@csrf_exempt
def dodavanje_knjiga_za_korpu(request):
	provera = [False,5]
	zahtev = korpa.proveraZahteva(request, Forms__za_korpu)

	# zahtev ispravan
	if(zahtev[0] == True):
		data = korpa.getDataFromRequest(request,zahtev[1])
		provera = korpa.proveraKnjigaUKorpi(data["stavke"],data["knjigaISBN"])
		#knjiga nije u korpi dakle moze add
		if (provera[0] == False):
			korpa.addUKorpu(request,data)
			provera[1] = 1
	return HttpResponse(json.dumps(provera[1]), content_type=
	"application/json")

@login_required
def prikaz_korpe(request):
	knjige = korpa.getKorpa(request)
	stavke = korpa.getStavke(knjige,Knjige)
	ukupno = korpa.setUkupno(stavke)
	return render(request, 'public/knjige/dodavanje_stavke_narudzbine.html',
				  {"korpa": stavke, "ukupno": str(ukupno)})

@csrf_exempt
def akcije_za_korpu(request):
	return_value = {}
	zahtev = korpa.proveraZahteva(request, "akcijaZaKorpu")
	if("radnja" in zahtev):
		if (zahtev["radnja"] == "brisanje"):
			return_value = korpa.delKnjiga(request,zahtev["knjigaISBN"])

		elif (zahtev["radnja"] == "oduzimanje"):
			return_value = korpa.setKolicina(request,zahtev["knjigaISBN"],"oduzimanje")

		elif (zahtev["radnja"] == "dodavanje"):
			return_value = korpa.setKolicina(request, zahtev["knjigaISBN"], "dodavanje")

		elif (zahtev["radnja"] == "narucivanje"):
			korisnik = Korisnici.objects.get(id=int(request.session["korisnikInfoId"]))

			return_value = korpa.narucivanjeKnjige(request,korisnik, timezone)

	return HttpResponse(json.dumps(return_value), content_type=
	"application/json")


@csrf_exempt
def ocenjivanje_knjige(request):
	return_value = {}

	if(knjiga.isPost(request) == True):
		data = knjiga.getDataFromRequest(request)

		# knjiga je ranije ocenjena,ovo je azuriranje
		if(knjiga.getOcene()==1):
			knjiga.azurirajOcenu()
			return_value.setdefault("poruka",2)

		# knjiga se prvi put ocenjuje
		elif(knjiga.getOcene()==0):
			knjiga.oceniKnjigu()
			return_value.setdefault("poruka",1)

		# funkcija za DOM
		oceneKnjige = knjiga.oceneKnjiga(data["knjigaObj"].id,forJson = True)
		return_value.setdefault("oceneKnjige",oceneKnjige)

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
