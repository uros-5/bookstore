from Knjizara.models import *
from django.contrib.auth.models import User

knjigaIsbn = ""
ocena = ""
knjigaObj = ""
oceneZaKnjigu = ""
korisnikInfoId = ""



def getDataFromRequest(request):

	global korisnikInfoId,knjigaIsbn, knjigaObj, ocena, oceneZaKnjigu


	knjigaISBN = request.POST["knjigaISBN"]
	ocena = request.POST["ocena"]
	knjigaObj = Knjige.objects.get(ISBN=knjigaISBN)
	korisnikInfoId = request.session["korisnikInfoId"]
	oceneZaKnjigu = OceneKnjiga.objects.filter(korisnik_id=int(korisnikInfoId),
											   knjiga_id=knjigaObj.id)

	return {"knjigaISBN":knjigaISBN,"ocena":ocena,
			"knjigaObj":knjigaObj,"oceneZaKnjigu":oceneZaKnjigu}

def azurirajOcenu():
	global oceneZaKnjigu,ocena

	oceneZaKnjigu[0].ocena = ocena
	oceneZaKnjigu[0].save()

def oceniKnjigu():
	global korisnikInfoId,knjigaObj,ocena,OceneKnjiga

	ocenaObj = OceneKnjiga()
	ocenaObj.knjiga = knjigaObj
	ocenaObj.korisnik_id = int(korisnikInfoId)
	ocenaObj.ocena = ocena
	ocenaObj.save()

def komentarisanjeKnjige(komentar,korisnik,knjiga,knk):
	knk.korisnik = korisnik
	knk.knjiga = knjiga
	knk.odobren = False
	knk.komentar = komentar
	knk.save()

def isPost(request):
	if(request.POST):
		if len(request.POST) > 0:
			return True
		return False
	return False

def getOcene():
	if(len(oceneZaKnjigu)>0):
		return 1
	if (len(oceneZaKnjigu) < 1):
		return 0

def dodavanjeIAutora(knjige):
	for i in range(len(knjige)):
		autor = knjige[i]["autor"]
		userId = Korisnici.objects.filter(id=autor).values("korisnik_id")[0]["korisnik_id"]
		user = User.objects.get(id=userId)
		imeIPrezime = user.first_name + " " + user.last_name
		knjige[i]["autor"] = imeIPrezime
	return knjige
def getKategorija(kategorija,range):
	knjige = list(Knjige.objects.values("kategorija","naslov","opis","autor","cena","slika","ISBN").filter(kategorija=kategorija)[:range][:])
	return knjige
def getNajnovije():
	return Knjige.objects.values("kategorija", "naslov", "cena", "slika", "id", "ISBN").order_by("-id")[:5].all()

def oceneKnjiga(knjigaID,forJson = False):
	oceneLista = []
	knjiga = knjigaID

	ocene = OceneKnjiga.objects.filter(knjiga=knjiga)
	for i in range(len(ocene)):
		ocena = ocene[i].ocena
		if(forJson == True):
			username = User.objects.get(id=Korisnici.objects.get(id=ocene[i].korisnik_id).korisnik_id).username
			oceneLista.append([username, ocena])
		else:
			username = ocene[i].korisnik
			oceneLista.append([username, ocena])
	return oceneLista

def srediNaslov(naslov):
	duzina = len(naslov)
	brojac = 0
	naslov2 = ""
	if(duzina>16):
		for i in range(0, duzina):
			naslov2 += naslov[i]
			brojac += 1
			if (brojac == 18):
				naslov2 += "\n"
				brojac = 0
		return naslov2
	return naslov
def komentariLook(knjigaID):
	komentarLista = []
	komentari = KomentariNaKnjigama.objects.filter(knjiga=knjigaID, odobren=True)
	for i in range(len(komentari)):
		korisnik = Korisnici.objects.get(id=komentari[i].korisnik.id)
		grad = korisnik.grad
		komentar = komentari[i].komentar
		username = komentari[i].korisnik
		komentarLista.append([username, grad, komentar])
	return komentarLista


def setKnjigaLook(ISBN):
	knjiga = Knjige.objects.get(ISBN=ISBN)
	naslov = srediNaslov(knjiga.naslov)
	oceneLista = oceneKnjiga(knjiga.id)
	komentarLista = komentariLook(knjiga.id)
	knjiga.naslov = naslov

	return knjiga,oceneLista,komentarLista

def setOcenjivanje(request,knjiga):
	narudzbineIDs = Narudzbine.objects.filter(korisnik_id=
											  int(request.session["korisnikInfoId"]))[:]
	ocenjivanje = ""

	for i in narudzbineIDs:
		idNar = i.id

		stavkeNar = StavkeNarudzbine.objects.filter(narudzbina_id=idNar).filter(knjiga_id=knjiga.id)
		if (len(stavkeNar) > 0):
			if (i.placeno == True):
				ocenjivanje = "DA"
				break
			else:
				ocenjivanje = "NE JOS"
		else:
			ocenjivanje = "NE"

	return ocenjivanje