from testlibrary.models import *

def setupSessionForKorisnik(request):
    if "korisnik" not in request.session.keys():
        if "_auth_user_id" in request.session.keys():
            korisnik1 = Korisnici.objects.filter(korisnik_id=request.session["_auth_user_id"])
            if len(korisnik1) > 0:
                request.session["korisnik"] = korisnik1[0].id

def set_korpa(request):
    if "korpa" not in request.session.keys():
        request.session["korpa"] = []

def get_korpa(request):
    return request.session["korpa"]

def getStavke(korpa,Knjige):
    stavke = []
    for stavka in korpa:
        knjiga = Knjige.objects.get(ISBN=stavka["isbn"])
        stavke.append(Knjige.for_korpa(knjiga,stavka))
    return stavke

def get_kolicina(request,isbn):
    for i in get_korpa(request):
        if i["isbn"] == isbn:
            return i["kolicina"]

def set_kolicina_knjiga(request,isbn,kolicina):
    korpa = get_korpa(request)
    for i in korpa:
        if i["isbn"] == isbn:
            i["kolicina"] = kolicina
            request.session["korpa"] = korpa
            return None

def set_ukupno(stavke):
    ukupno = 0
    for i in range(len(stavke)):
        ukupno += get_ukupna_cena_for_knjiga(stavke[i]["isbn"],stavke[i]["kolicina"])
    return round(float(ukupno),2)

def get_ukupna_cena_for_knjiga(isbn,kolicina):
    cena = Knjige.objects.filter(ISBN=isbn)[0].cena
    return round(float(kolicina*cena),2)


def add_to(request):
    korpa = get_korpa(request)
    if "ISBN" in request.POST:
        if not book_exists(korpa,request.POST["ISBN"]):
            if len(Knjige.objects.filter(ISBN=request.POST["ISBN"]))==1:
                korpa.append({"isbn":request.POST["ISBN"],"kolicina":1})
                request.session["korpa"] = korpa
                return True
            else:
                print(len(Knjige.objects.filter(ISBN=request.POST["ISBN"])))
                return None
        else:
            return False

def book_exists(korpa,isbn):
    for i in korpa:
        print(i)
        if i["isbn"] == isbn:
            return True
    return False

def reduce_kol(request,isbn,kolicina):
    ukupno_knjiga = get_ukupna_cena_for_knjiga(isbn,kolicina)
    if (kolicina > 1):
        kolicina -= 1
        set_kolicina_knjiga(request,isbn,kolicina)
        ukupno_knjiga = get_ukupna_cena_for_knjiga(isbn,kolicina)
        return set_return_value(isbn,3,kolicina,ukupno_knjiga,set_ukupno(get_korpa(request)))
    else:
        return set_return_value(isbn,3,kolicina,ukupno_knjiga,set_ukupno(get_korpa(request)))

def increase_kol(request,isbn,kolicina):
    ukupno_knjiga = get_ukupna_cena_for_knjiga(isbn,kolicina)
    if kolicina <= 11:
        kolicina +=1
        set_kolicina_knjiga(request,isbn,kolicina)
        ukupno_knjiga = get_ukupna_cena_for_knjiga(isbn,kolicina)
        return set_return_value(isbn,4,kolicina,ukupno_knjiga,set_ukupno(get_korpa(request)))
    else:
        return set_return_value(isbn,3,kolicina,ukupno_knjiga,set_ukupno(get_korpa(request)))

def set_return_value(knjiga,num,kolicina,ukupno,ukupnoSve):
    return_value = {}
    return_value.setdefault("knjigaISBN",knjiga)
    return_value.setdefault("poruka",num)
    return_value.setdefault("kolicina",kolicina)
    return_value.setdefault("ukupno",ukupno)
    return_value.setdefault("ukupnoSve",ukupnoSve)
    return return_value

def delete_item(request,knjiga):
    korpa = get_korpa(request)
    for i in range(len(korpa)):
        if korpa[i]["isbn"] == knjiga:
            del korpa[i]
            request.session["korpa"] = korpa
            return {"poruka":2,"knjigaISBN":knjiga,"ukupnoSve":set_ukupno(get_korpa(request))}


def kreiraj_narudzbinu(request):
    narudzbina = Narudzbine()
    narudzbina.datumNarucivanja = timezone.now()
    narudzbina.placeno = False
    narudzbina.korisnik = Korisnici.objects.filter(
        korisnik=User.objects.get(id=request.session["_auth_user_id"]))[0]
    narudzbina.save()
    return narudzbina

def kreiraj_stavke(request,narudzbina):
    korpa = get_korpa(request)
    for i in range(len(korpa)):
        stavka = StavkeNarudzbine(narudzbina=narudzbina)
        stavka.knjiga = Knjige.objects.filter(ISBN=korpa[i]["isbn"])[0]
        stavka.kolicina = korpa[i]["kolicina"]
        stavka.save()
    request.session["korpa"] = []

    