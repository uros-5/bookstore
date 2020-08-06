from Knjizara.models import Knjige,Narudzbine,StavkeNarudzbine
def proveraZahteva(request, forma):
	if len(request.POST) > 0:
		if(str(type(forma)) == "<class 'str'>"):
			provera = {}
			if len(request.POST) > 0:
				radnja = request.POST["radnja"]
				provera["radnja"] = radnja
				try:
					knjiga = request.POST["knjigaISBN"]
					provera["knjigaISBN"] = knjiga
				except:
					# narucivanje
					korpa = getKorpa(request)
					provera["korpa"] = korpa

				return provera

		else:
			form = forma(request.POST)
			if form.is_valid():
				return [True,form]
			else:
				return [False, form]
	else:
		return [False,forma]

def getDataFromRequest(request,form):
	stavke = request.session['korpa']
	knjigaISBN = form.cleaned_data["knjigaISBN"]
	kolicina = form.cleaned_data["kolicina"]

	return {"stavke":stavke,"knjigaISBN":knjigaISBN,"kolicina":kolicina}

def proveraKnjigaUKorpi(stavke,knjigaISBN):
	rValue = [False,1]
	for i in stavke:
		if (i["knjigaISBN"] == knjigaISBN):
			print("knjiga je vec u korpi")
			provera = True
			return_value = 5
			rValue =  [provera,return_value]
			break
		else:
			provera = False
			return_value = 1
			rValue = [provera,return_value]

	return rValue

def getKorpa(request):
	return request.session["korpa"]

def getStavke(korpa,Knjige):
	stavke = []
	for stavka in korpa:
		knjiga = Knjige.objects.get(ISBN=stavka["knjigaISBN"])
		isbn = knjiga.ISBN
		slika = knjiga.slika
		naslov = knjiga.naslov
		cena = knjiga.cena
		kolicina = stavka["kolicina"]
		stavke.append({"isbn": isbn, "slika": slika, "naslov": naslov, "cena": cena, "kolicina": kolicina}, )
	return stavke

def setUkupno(stavke):
	ukupno = 0
	for i in range(len(stavke)):
		ukupno += stavke[i]["cena"] * stavke[i]["kolicina"]
	return ukupno

def setKorpa(request,podaci):
	request.session["korpa"] = podaci



def setStavka(knjigaISBN,kolicina):
	stavka = {}
	stavka.setdefault("knjigaISBN", knjigaISBN)
	stavka.setdefault("kolicina", int(kolicina))
	return stavka


def addUKorpu(request,data):
	data["stavke"].append(setStavka(data["knjigaISBN"],data["kolicina"]))
	setKorpa(request, data["stavke"])

def delKnjiga(request,knjiga):
	return_value = {}
	korpa = getKorpa(request)

	for i in range(len(korpa)):
		if (korpa[i]["knjigaISBN"] == knjiga):
			del korpa[i]
			setKorpa(request,korpa)
			return_value = setReturnValue(knjiga,2)
			break
	return return_value
def setKolicina(request,knjiga,akcija):
	return_value = {}
	korpa = getKorpa(request)
	for i in range(len(korpa)):
		if (korpa[i]["knjigaISBN"] == knjiga):
			kolicina = getKolicina(korpa[i])
			if(akcija == "oduzimanje"):
				if (kolicina > 1):
					kolicina -= 1
					korpa[i]["kolicina"] = kolicina
				setKorpa(request,korpa)
				return_value = setReturnValue(knjiga,3,kolicina)
				break

			elif(akcija == "dodavanje"):
				if (kolicina <= 11):
					kolicina += 1
					korpa[i]["kolicina"] = kolicina
				setKorpa(request, korpa)
				return_value = setReturnValue(knjiga, 4, kolicina)
				break
	return return_value

def narucivanjeKnjige(request,korisnik,timezone):

	narudzbina = Narudzbine(korisnik=korisnik)
	narudzbina.datumNarucivanja = timezone.now()
	narudzbina.placeno = False
	narudzbina.save()

	korpa = getKorpa(request)



	for i in range(len(korpa)):

		stavkeNarudzbine = StavkeNarudzbine()
		stavkeNarudzbine.knjiga = Knjige.objects.filter(ISBN=korpa[0]["knjigaISBN"])[0]
		stavkeNarudzbine.kolicina = getKolicina(korpa[0])
		stavkeNarudzbine.narudzbina = narudzbina
		stavkeNarudzbine.save()

		del korpa[0]

	setKorpa(request, korpa)

	return setReturnValue(knjigaISBN="000000", poruka = 1, kolicina=0)

def getKolicina(knjiga):
	return knjiga["kolicina"]

def setReturnValue(knjigaISBN="",poruka=0,kolicina = 0):
	return {"knjigaISBN":knjigaISBN,"poruka":poruka,"kolicina":kolicina}