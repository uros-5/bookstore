from NotifCenter import *
# import socket

class PostaNotifCenter(NotifCenter):


	def proveri_fajl(self,sock):
		if(os.path.exists(self.putanja)):
			#otvori fajl
			fajl = open(self.putanja,"r")
			podaci = self.sortForEveryClient(fajl.read())
			knjizaraTestPosta = []
			# zatim drugi klijenti poste...

			for i in podaci:
				if (i[0].startswith("knjizaraTestPosta")):
					knjizaraTestPosta.append(int(i[1]))
	# 		....
			if(len(knjizaraTestPosta)>0):
				self.posaljiPorukuServeru(sock,{"knjizaraTestPosta":knjizaraTestPosta})
				odgovor = self.primiPoruku(sock)["lista"]
				# {'lista': [['OK']]}
				if (odgovor[0][0] == "OK"):
					fajl.close()
					os.remove(self.putanja)

postaNotifCenter = PostaNotifCenter("posta")
try:
	postaNotifCenter.startCenter()

except Exception as e:
	print(e)


