import os
import django
import pickle
import re
if 'env setting':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')
	django.setup()

from TaskRestAPI.models import *
from django.utils import timezone
import socketserver
import json
from django.db import connection
from django.contrib.auth import authenticate
from TaskRestAPI.miniAppsZaKnjizaru.ServerMobilnoBankaPosta.Upiti import *

cursor = connection.cursor()


class MyTCPHandler(socketserver.BaseRequestHandler):
	userSablon = re.compile(r'\((.*?)\)')
	def handle(self):
		data = self.request.recv(10000)
		print("Poruka od {} :".format(self.client_address[0]))

		try:
			poruka = str(data.decode())
		except:
			poruka = ""
			bankaIPostaRequest(data, self.request)

		if (poruka in upitiZaTab1):
			row = []
			if (poruka == "najpKnjige\n"):
				row = cursor.execute(najpKnjige)

			elif (poruka == "besplKnjige\n"):
				row = cursor.execute(besplKnjige)

			elif (poruka == "hronLista\n"):
				row = cursor.execute(hronLista)
			elif (poruka == "countNarudzbine\n"):
				row = cursor.execute(countNarudzbine)
			# row = cursor.fetchone()
			sendMessageToClient(row, self.request)

		elif (poruka.startswith("mojeKnjige")):
			id = poruka.split(" ")[1]
			print(id)
			row = cursor.execute(mojeKnjige.replace("nesto", id))
			sendMessageToClient(row, self.request)
		elif (poruka.startswith("ids")):
			porukaUDelovima = poruka.split(" ")
			# row = cursor.execute(countNarudzbine)
			# idNarudzbine = createList(row)[0][0]

			korisnikID = porukaUDelovima[-1]
			korisnik = Korisnici.objects.get(id=korisnikID)

			narudzbina = Narudzbine(datumNarucivanja=timezone.now())
			narudzbina.korisnik = korisnik
			narudzbina.save()

			print(poruka)
			print(porukaUDelovima)
			for i in range(1, len(porukaUDelovima) - 1):
				print(porukaUDelovima[i])
				obj = StavkeNarudzbine()
				obj.knjiga = Knjige.objects.get(id=int(porukaUDelovima[i]))
				obj.narudzbina = narudzbina
				obj.kolicina = 1
				obj.save()
			sendMessageToClient(("OK",), self.request)
		elif (poruka.startswith("id")):
			idKnjige = poruka.split(" ")[1]
			upit = idd.replace("kolona", "id").replace("nesto", idKnjige)
			row = cursor.execute(upit)
			sendMessageToClient(row, self.request)
		elif (poruka.startswith("komentari")):
			idKnjige = poruka.split(" ")[1]
			upit = komentari.replace("nesto", idKnjige)
			row = cursor.execute(upit)
			sendMessageToClient(row, self.request)
		elif (poruka.startswith("kategorija")):
			kategorijaPoruka = "'" + poruka.split("kategorija ")[1].replace("\n", "") + "'"
			upit = kategorija.replace("nesto", kategorijaPoruka)
			# print(upit)
			row = cursor.execute(upit)
			sendMessageToClient(row, self.request)
		elif (poruka.startswith("getUser")):
			username = poruka.split(" ")[1]
			sifra = poruka.split(" ")[2].replace("\n", "")
			user = authenticate(username=username, password=sifra)
			if (user != None):
				print("ok")
				korisnikObj = Korisnici.objects.get(korisnik_id=user.id)
				sendMessageToClient([("OK", korisnikObj.id)], self.request)
				print(korisnikObj.id)
				korisnikObj = None
			else:
				sendMessageToClient([("NOT OK",)], self.request)
		elif (poruka.startswith("koMentarisi")):
			userID = poruka.split(" ")[1]
		# komentar = poruka.split
		elif (poruka.startswith("reg")):

			print(poruka)
			podaci = self.userSablon.findall(poruka.replace("\n",""))
			# reg username email sifra ime prezime ulicaIBroj brojPoste grad
			try:
				print(podaci)
				userObj = User.objects.create_user(username=podaci[0],
														 email=podaci[1],
														 password=podaci[2]
														 )
				userObj.is_active = True
				userObj.first_name = podaci[3]
				userObj.last_name = podaci[4]
				userObj.save()

				korisnik = Korisnici()
				korisnik.korisnik = userObj
				korisnik.ulicaIBroj = podaci[5]
				korisnik.brojPoste = int(podaci[6])
				korisnik.grad = podaci[7]
				korisnik.save()

				sendMessageToClient([("OK", korisnik.id)], self.request)


			except Exception as e:
				print(e)
				sendMessageToClient([("NOT OK", 0)], self.request)


def startServer1():
	HOST, PORT = "192.168.1.4", 34300
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()


def sendMessageToClient(row=[], request=""):
	lista = createList(row)
	jsonVar = json.dumps(
		{"lista": [lista]})

	request.sendall(jsonVar.encode())


def createList(row=[]):
	lista = []
	if (row != []):
		for i in row:
			lista.append(i)
		return lista
	else:
		return ("OK",)


def bankaIPostaRequest(data, request):
	primer = pickle.loads(data)
	print(primer)
	if ("knjizaraTestNarudzbine" in primer):
		# izvrsi akciju na bazi
		for i in primer["knjizaraTestNarudzbine"]:
			try:
				narudzbina = Narudzbine.objects.get(id=i)
				if (narudzbina.placeno == False):
					narudzbina.placeno = True
					narudzbina.save()
					print("narudzbina placena!")
			except:
				continue


	elif ("knjizaraTestPosta" in primer):
		# izvrsi akciju na bazi
		for i in primer["knjizaraTestPosta"]:
			try:

				narudzbina = Narudzbine.objects.get(id=i)
				if (narudzbina.placeno == True):
					if (narudzbina.datumPrijema == None):
						narudzbina.datumPrijema = timezone.now()
						narudzbina.save()
						print("narudzbina azurirana")
			except:
				continue
	sendMessageToClient(row=[], request=request)

	# from ServerZaMobilno import ServerZaMobilno
	# ServerZaMobilno.startServer1()
