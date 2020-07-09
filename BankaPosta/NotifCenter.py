import socket
import sys
import pickle
import os
import re
import time
import json


class NotifCenter(object):
	HOST, PORT = "192.168.1.4", 34300
	VELICINA_BUFFERA = 5000
	def __init__(self,tipNotif):
		self.tipNotif = tipNotif
		if(tipNotif=="banka"):
			self.sablon = re.compile("(knjizaraTestNarudzbina(\d+))")
			self.putanja = "izvestajiBanka\\izvestaj.txt"
		elif(tipNotif=="posta"):
			self.sablon = re.compile("(knjizaraTestPosta(\d+))")
			self.putanja = "izvestajiPosta\\izvestaj.txt"

	def posaljiPorukuServeru(self,sock, lista):
		sock.connect((self.HOST, self.PORT))

		pickleporuka = pickle.dumps(lista)
		sock.send(pickleporuka)  # posalji poruku

	def primiPoruku(self,sock):
		received = sock.recv(self.VELICINA_BUFFERA)
		sock.close()
		return json.loads(received)

	def sortForEveryClient(self,podaci):
		return self.sablon.findall(podaci)
	def startCenter(self):
		while (data != "Exit"):
			try:
				time.sleep(5)
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				postaNotifCenter.proveri_fajl(sock)
			except:
				continue
