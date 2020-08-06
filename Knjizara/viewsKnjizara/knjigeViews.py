from Knjizara.views import *
from Knjizara.utils import Knjiga
class Kategorija_look(ListView):
	model = Korisnici
	template_name = 'public/knjige/knjige.html'
	paginate_by = 12

	def get_queryset(self):
		if (str(self.request.path).startswith("/ljubavni")):
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

		elif (self.request.path.startswith("/autor/")):
			print(self.request)
			knjige_all = Knjige.objects.filter(kategorija="Drama")
			return knjige_all

		elif (self.request.path == "/pretraga/"):

			pretraga = str(self.request.GET.get("pretraga")).upper()
			knjige_all = Knjige.objects.all().filter(naslov__contains=pretraga)
			print(knjige_all.count())
			return knjige_all


def knjiga_look(request, ISBN):
	kategorija = "/" + str(request.path).split("/")[1] + "/"
	pathsCategory = ["/ljubavni_roman/","/istorija/",
					 "/fantastika/","/filozofija/",
					 "/horor/","/drama/"
					 ]
	if (kategorija in pathsCategory):
		knjiga,oceneLista,komentarLista = Knjiga.setKnjigaLook(ISBN)

		ocenjivanje = "LOG"

		if ("korisnikInfoId" in request.session.keys()):

			ocenjivanje = Knjiga.setOcenjivanje(request,knjiga)

		form = komentarisanje(request,knjiga.id)

		return render(request, 'public/knjige/knjiga.html', {"knjiga": knjiga, "ocene": oceneLista,
													  "komentarLista": komentarLista,"form":form,
															 "zvezdiceNaModalu":ocenjivanje})



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


