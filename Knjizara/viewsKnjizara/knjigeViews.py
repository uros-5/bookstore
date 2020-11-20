from Knjizara.views import *
from Knjizara.utils import Knjiga
class Kategorija_view(ListView):
	model = Korisnici
	template_name = 'public/knjige/knjige.html'
	paginate_by = 12

	def get_queryset(self):
		self.setKategorija(self.request.path)
		knjige_all = Knjige.objects.filter(kategorija=self.kategorija)
		return knjige_all

	def setKategorija(self,kategorija):
		self.kategorija = kategorija.replace("/","").capitalize().replace("_"," ")



def knjiga_look(request, ISBN):
	kategorija = "/" + str(request.path).split("/")[1] + "/"
	print(kategorija)
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

		return render(request, 'public/knjiga2.html', {"knjiga": knjiga, "ocene": oceneLista,
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


