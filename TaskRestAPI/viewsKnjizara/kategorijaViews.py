from TaskRestAPI.views import *
from TaskRestAPI.viewsKnjizara.POSTViews import komentarisanje

class Kategorija_look(ListView):
	model = Korisnici
	template_name = 'public/knjige/knjige.html'
	paginate_by = 12

	def get_queryset(self):
		print(self.request.path)
		if (str(self.request.path) == "/ljubavni_roman/"):
			knjige_all = Knjige.objects.filter(kategorija="Ljubavni roman")
			return knjige_all
		elif (self.request.path == "/istorija/"):
			knjige_all = Knjige.objects.filter(kategorija="Istorija")
			return knjige_all

		elif (self.request.path == "/fantastika/"):
			knjige_all = Knjige.objects.filter(kategorija="Fantastika")
			return knjige_all

		elif (self.request.path == "/filozofija/"):
			knjige_all = Knjige.objects.filter(kategorija="Filozofija")
			return knjige_all

		elif (self.request.path == "/horor/"):
			knjige_all = Knjige.objects.filter(kategorija="Horor")
			return knjige_all

		elif (self.request.path == "/drama/"):
			knjige_all = Knjige.objects.filter(kategorija="Drama")
			return knjige_all

		elif (self.request.path == "/pretraga"):
			print("nestoooo")
			knjige_all = Knjige.objects.filter(kategorija="Ljubavni roman")
			return knjige_all
def knjiga_look(request, ISBN):
	kategorija = "/" + str(request.path).split("/")[1] + "/"
	pathsCategory = ["/ljubavni_roman/","/istorija/",
					 "/fantastika/","/filozofija/",
					 "/horor/","/drama/"
					 ]
	if (kategorija in pathsCategory):
		knjiga = Knjige.objects.get(ISBN=ISBN)
		knjigaID = Knjige.objects.filter(ISBN=ISBN)[0].id
		naslov = srediNaslov(knjiga.naslov)
		oceneLista = oceneKnjiga(knjigaID)
		komentarLista = komentari(knjigaID)
		knjiga.naslov = naslov
		ocenjivanje = "LOG"
		#OVDE
		if ("korisnikInfoId" in request.session.keys()):
			#udji u narudzbine i vidi korID
			narudzbineIDs = Narudzbine.objects.filter(korisnik_id=
				int(request.session["korisnikInfoId"]))[:]
			for i in narudzbineIDs:
				idNar = i.id
				stavkeNar = StavkeNarudzbine.objects.filter(narudzbina_id=idNar).filter(knjiga_id=knjigaID)
				if(len(stavkeNar)>0):
					if(i.placeno == True):
						ocenjivanje = "DA"
					else:
						ocenjivanje = "NE JOS"
					break
				else:
					ocenjivanje = "NE"


			#za svaku nar udji u stavke
			#za svaku stvaku vidi knjige
			#poredi id knjige sa mojim idknjige
		print(ocenjivanje)
		print(oceneLista)
		form = komentarisanje(request,knjigaID)
		return render(request, 'public/knjige/knjiga.html', {"knjiga": knjiga, "ocene": oceneLista,
													  "komentarLista": komentarLista,"form":form,
															 "ocenjivanje":ocenjivanje})
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


# def oceneKnjiga(knjigaID,forJson = False):
# 	oceneLista = []
# 	knjiga = knjigaID
# 	ocene = OceneKnjiga.objects.filter(knjiga=knjiga)
# 	for i in range(len(ocene)):
# 		ocena = ocene[i].ocena
# 		if(forJson == True)
# 		username = ocene[i].korisnik.
# 		oceneLista.append([username, ocena])
# 	return oceneLista


def komentari(knjigaID):
	komentarLista = []
	komentari = KomentariNaKnjigama.objects.filter(knjiga=knjigaID, odobren=True)
	for i in range(len(komentari)):
		korisnik = Korisnici.objects.get(id=komentari[i].korisnik.id)
		grad = korisnik.grad
		komentar = komentari[i].komentar
		username = komentari[i].korisnik
		komentarLista.append([username, grad, komentar])
	return komentarLista
