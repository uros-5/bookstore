from NotifCenter import *
# import socket

class BankNotifCenter(NotifCenter):


	def proveri_fajl(self,sock):
		print(self.putanja)
		if(os.path.exists(self.putanja)):
			#otvori fajl
			fajl = open(self.putanja,"r")
			podaci = fajl.read()
			podaci = self.sortForEveryClient(podaci)
			knjizaraTestNarudzbina = []
			# zatim drugi klijenti banke...

			for i in podaci:

				if(i[0].startswith("knjizaraTestNarudzbina")):
					knjizaraTestNarudzbina.append(int(i[1]))
	# 		....
			if(len(knjizaraTestNarudzbina)>0):
				self.posaljiPorukuServeru(sock,{"knjizaraTestNarudzbine":knjizaraTestNarudzbina})
				odgovor = self.primiPoruku(sock)["lista"]
				# {'lista': [['OK']]}
				if(odgovor[0][0] == "OK"):
					fajl.close()
					os.remove(self.putanja)

bankNotifCenter = BankNotifCenter("banka")
try:
	bankNotifCenter.startCenter()
except Exception as e:
	print(e)


