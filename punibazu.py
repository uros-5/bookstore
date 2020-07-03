from TaskRestAPI.models import *
from django.utils.timezone import timezone
from string import ascii_lowercase as lista
import random
from django.utils import timezone
import shelve
fajl = shelve.open("zabazu\\podaci.dat","r")
# korisnici

komentari = ["Vrh knjiga preporucujem je svima!",
             "super je knjiga","Morate je procitati","Nisam preterano odusevljen","Moglo je bolje.",
             "Knjiga je must-buy!","Da li ima u knjizari u ","Najbolja u kategoriji ","Predivna avantura."]


def randomm(podatak=''):
    if(podatak=='ulica'):
        ulica = ""
        reci = random.randint(1,2)
        brojUlice = random.randint(1,150)
        duzina = random.randint(10,17)
        if(reci>1):
            recDuzina = int(duzina/2)

            # ulica = str(lista[random.randint(1,25)]).upper()
            for i in range(recDuzina):
                if(len(ulica)==0):
                    ulica = str(lista[random.randint(1, 25)]).upper()
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " "
            for i in range(recDuzina):
                if(ulica[-1] == " "):
                    if(random.randint(1,2)==1):
                        ulica = str(lista[random.randint(1, 25)]).upper()
                    else:
                        ulica += str(lista[random.randint(1, 25)])
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " "+str(brojUlice)
            return ulica

        elif(reci==1):
            for i in range(duzina):
                if(len(ulica)==0):
                    ulica = str(lista[random.randint(1, 25)]).upper()
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " " + str(brojUlice)
            return ulica
    elif(podatak=='brojPoste'):
        brojPoste = random.randint(1000,5000)
        return brojPoste
    elif (podatak == 'grad'):
        gradovi = fajl["gradovi"]
        grad0 = random.choice(list(gradovi.items()))
        return (grad0[0],grad0[1])
    elif (podatak == 'telefon'):
        telefon = ""
        prefiksi = ["060","061","062","063","064","065","066","068","069"]
        telefon += random.choice(prefiksi)+"-"
        for i in range(2):
            for i2 in range(3):
                telefon+=str(random.randint(1,9))
            if(i!=1):
                telefon+="-"
        return telefon


def kreirajKorisnike():
    zaDodati = 101
    redosled = "korisnik"
    fajl = shelve.open("zabazu\\podaci.dat", "r")
    imena = fajl["imena"]
    prezimena = fajl["prezimena"]
    while(True):
        for i in range(1,zaDodati):
            username = redosled + str(i)
            email = redosled + str(i) + '@mejl.com'

            first_name = random.choice(imena)
            last_name = random.choice(prezimena)
            ulicaIBroj = randomm('ulica')
            grad0 = randomm('grad')
            grad = grad0[0]
            brojPoste = grad0[1]
            telefon = randomm('telefon')
            if(redosled=="korisnik"):
                password = "PASSWORD1"
                novi_korisnik = User.objects.create_user(username=username,
                                                         email=email,
                                                         password=password
                                                         )
                novi_korisnik.is_active = True
                novi_korisnik.first_name = first_name
                novi_korisnik.last_name = last_name
                novi_korisnik.save()

                is_korisnik = True
                korisnik = Korisnici(ulicaIBroj=ulicaIBroj,brojPoste=brojPoste,
                                    grad=grad,telefon=telefon,is_korisnik=is_korisnik)

                korisnik.korisnik = novi_korisnik

                korisnik.save()
            else:
                password = "PASSWORD12"
                novi_korisnik = User.objects.create_user(username=username,
                                                         email=email,
                                                         password=password
                                                         )
                novi_korisnik.is_active = True
                novi_korisnik.first_name = first_name
                novi_korisnik.last_name = last_name
                novi_korisnik.save()
                is_autor = True
                korisnik = Korisnici(ulicaIBroj=ulicaIBroj, brojPoste=brojPoste,
                                    grad=grad, telefon=telefon, is_autor=is_autor)
                korisnik.korisnik = novi_korisnik
                korisnik.save()

        if(redosled=="korisnik"):
            zaDodati-=100-36
            redosled="autor"
        elif(redosled=="autor"):
            break
    fajl.close()

#izdavaci
def kreirajIzdavace():
    for i in range(6):
        ime = 6*str(lista[i]).upper()
        racun = ""
        email=""
        while(True):
            if(len(racun)==3 or len(racun)==9):
                racun+="-"
                continue
            elif(len(racun)==12):
                break
            racun+=str(random.randint(1,9))
        if(i%2==0):
            email = 6*str(lista[i])+"@mejl.com"
        izdavac = Izdavaci(ime=ime,racun=racun,email=email)
        izdavac.save()

def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start

# knjige

def kreirajKnjige():
    fajl = shelve.open("zabazu\\podaci.dat", "r")
    knjigee = fajl["knjige"]
    for i in range(30,500):
        isbn = ""
        strana = random.randint(50,370)
        # cena = randrange_float(450.00,6500.00,0.50)
        godina = random.randint(2000,2020)
        izdavac = random.randint(1,6)
        autor = random.randint(0,35)
        while (True):
            if (len(isbn) == 3 or len(isbn) == 6) or len(isbn) == 11:
                isbn += "-"
                continue
            elif (len(isbn) == 15):
                break
            isbn += str(random.randint(1, 9))
        knjigaizfajla = knjigee[i]
        cena = knjigaizfajla[2].split(",")
        tup1 = cena[0]
        tup2 = ""
        if("." in cena[0]):
            tup1 = cena[0].replace(".","")
        if(cena[1].endswith("0")):
            tup2 = cena[1][0]+"5"
        else:
            tup2 = cena[1]
        cena = float(str(tup1+"."+tup2))
        knjiga = Knjige(naslov=knjigaizfajla[0],strana=strana,cena=(cena),godinaIzdanja=godina,ISBN=isbn)
        knjiga.izdavac = Izdavaci.objects.get(id=izdavac)
        knjiga.autor = Korisnici.objects.filter(is_autor=True)[autor]
        knjiga.save()
        fajl.close()
# narudzbine
def kreirajNarudzbine():
    for i in range(79):
        narudzbina = Narudzbine()
        narudzbina.datumNarucivanja = timezone.now()
        narudzbina.placeno = False
        narudzbina.korisnik = Korisnici.objects.filter(is_korisnik=True)[random.randint(0,75)]
        narudzbina.save()

# stavke narudzbine
def kreirajStavkeNarudzbine():
    #za svaku narudzbinu
    for i in range(1,78):
        brojStavki = random.randint(1,6)
        brojDodatihKnjiga = 0
        #dokle god nije dodato nekoliko knjiga proveravaj i dodaj
        while(brojDodatihKnjiga!=brojStavki):
            knjiga = random.randint(1,140)
            narudzbina = i
            querry = StavkeNarudzbine.objects.filter(knjiga=knjiga, narudzbina=narudzbina)
            #ako ne postoji ovakav querry
            if(querry.count()==0):
                stavkeNarudzbine= StavkeNarudzbine()
                stavkeNarudzbine.kolicina = random.randint(1,3)
                stavkeNarudzbine.knjiga = Knjige.objects.get(id=knjiga)
                stavkeNarudzbine.narudzbina = Narudzbine.objects.get(id=narudzbina)
                stavkeNarudzbine.save()
                brojDodatihKnjiga+=1
# placanje knjiga
def placanjeKnjiga1():
    for i in range(1,Narudzbine.objects.count()+1):
        daNe = [True,False]
        narudzbina = Narudzbine.objects.get(id=i)
        narudzbina.placeno = random.choice(daNe)
        narudzbina.save()
# komentarisanje knjiga
def kreirajKomentareNaKnjigama():
    knk = KomentariNaKnjigama()
    knk.komentar = random.choice(komentari)
    knk.korisnik = Korisnici.objects.filter(is_korisnik=True)[5]
    knk.knjiga = Knjige.objects.get(id=10)
    knk.save()
def kreirajOceneNaKnjigama():
    korisnik = Korisnici.objects.get(id=4)
    knjiga = Knjige.objects.get(id=124)
    narudzbina = Narudzbine.objects.filter(korisnik = korisnik.id,placeno = True)[0]
    stavka = StavkeNarudzbine.objects.filter(narudzbina = narudzbina.id,knjiga = knjiga)
    onk = OceneKnjiga(korisnik=korisnik,ocena=5)

