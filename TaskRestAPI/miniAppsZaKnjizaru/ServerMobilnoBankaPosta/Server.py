import socketserver
import pickle
import numpy as np
import json

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(10000)
        print("Poruka od {} :".format(self.client_address[0]))

        poruka = str(data.decode())
        print(poruka)
        if(poruka == "python\n"):
            jsonVar = json.dumps({"lista":[("sdfsdf","fddfdsf"),("sdfsdf","fddfdsf"),("sdfsdf","fddfdsf"),("sdfsdf","fddfdsf")]})
            self.request.sendall(jsonVar.encode())



HOST, PORT = "192.168.1.4", 34300
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server.serve_forever()
