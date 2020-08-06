from Knjizara.models import Korisnici,Narudzbine,StavkeNarudzbine,Knjige,OceneKnjiga
from django.contrib.auth.models import User

def check_login(form,authenticate,login,request):
	if (form.is_valid()):
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return user,True
		else:
			return user,False
	else:
		return "",None

def getRegInput(form,key):

	return form.cleaned_data[key]

def registracija(form):

	novi_korisnik = User.objects.create_user(username=getRegInput(form,"username"),
											 email=getRegInput(form,"email"),
											 password=getRegInput(form,"password")
											 )
	novi_korisnik.is_active = True

	novi_korisnik.first_name = getRegInput(form,"first_name")

	novi_korisnik.last_name = getRegInput(form,"last_name")

	novi_korisnik.save()

	korisnik = Korisnici()

	korisnik.korisnik = novi_korisnik

	userType = str(getRegInput(form,"userType"))

	if (userType == "korisnik"):

		korisnik.is_korisnik = True

	elif (userType == "autor"):

		korisnik.is_autor = True

	korisnik.save()

def setUpKorisnikPodaci(context,object):
	if (object.id != 1):

		korisnik = Korisnici.objects.get(korisnik_id=object.id)

		context["korisnik"] = korisnik

		return context
	else:
		return context

def listViewNarudzbina(request):

	narudzbine_korisnika = getNarudzbine(request)

	narudzbineHTML = []

	if (len(narudzbine_korisnika) > 0):

		for i in range(len(narudzbine_korisnika)):

			narudzbina = setNarudzbina(narudzbine_korisnika[i])

			stavkeNarudzbine = setStavkeNarudzbine(narudzbina[0]["id"])

			knjige = []

			for j in range(len(stavkeNarudzbine)):

				knjiga0,knjiga = setKnjiga(stavkeNarudzbine[j])

				incrementKolicina(narudzbina,stavkeNarudzbine[j])

				incrementUkupno(narudzbina,knjiga,stavkeNarudzbine[j])

				knjiga0 = setKnjiga2(knjiga,knjiga0,stavkeNarudzbine[j])

				knjige.append(knjiga0)

			if (len(stavkeNarudzbine) > 0):
				setUkupnoNarudzbina(knjige,narudzbineHTML,narudzbina)

	return narudzbineHTML

def getNarudzbine(request):

	return Narudzbine.objects.filter(korisnik_id=getKorisnik(request)).order_by("-id")

def getKorisnik(request):

	return request.session["korisnikInfoId"]

def setNarudzbina(narudzbina):
	lista = []
	lista.append(
		{'id': narudzbina.id, 'placeno': narudzbina.placeno, 'ukupno': 0,
		 'kolicina': 0, 'datum': narudzbina.datumNarucivanja})
	return lista

def setStavkeNarudzbine(narudzbina):

	return StavkeNarudzbine.objects.filter(narudzbina_id=narudzbina)

def setKnjiga(stavka):
	knjiga0 = []

	knjiga = Knjige.objects.get(id=stavka.knjiga_id)

	knjiga0.append(knjiga.naslov)

	knjiga0.append(float(knjiga.cena))

	return knjiga0,knjiga
def incrementKolicina(narudzbina,stavka):

	narudzbina[0]['kolicina'] += stavka.kolicina

def incrementUkupno(narudzbina,knjiga,stavka):

	narudzbina[0]['ukupno'] += float(knjiga.cena * stavka.kolicina)

def setKnjiga2(knjiga,knjiga0,stavka):

	knjiga0.append(stavka.kolicina)

	knjiga0.append(knjiga.slika)

	return knjiga0

def setUkupnoNarudzbina(knjige,narudzbine,narudzbina):
	narudzbina.append(knjige)
	narudzbina[0]['ukupno'] = round(narudzbina[0]['ukupno'], 2)
	narudzbine.append(narudzbina)

def getOcenjeneKnjige(request):
	oceneKnjiga = OceneKnjiga.objects.filter(korisnik_id=getKorisnik(request))
	return oceneKnjiga

def setReviews(request,ocene):
	lista = []

	for i in range(len(ocene)):
		review = {}
		review.setdefault("rbr",str(i+1))
		review.setdefault('ocena', ocene[i].ocena)
		knjiga = Knjige.objects.get(id=ocene[i].knjiga_id)
		review.setdefault('naslov', knjiga.naslov)
		lista.append(review)

	return lista

