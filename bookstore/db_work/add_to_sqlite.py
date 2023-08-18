import sys

sys.path.append("../temp_project")

from bookstore.models import *

from django.utils.timezone import timezone
from string import ascii_lowercase as lista
import random
from django.utils import timezone
import shelve
from typing import List

SHELVE_DATA = "./bookstore/db_work/shelve_data/podaci.dat"

categories = [
    "ljubavni_roman",
    "istorija",
    "fantastika",
    "filozofija",
    "horor",
    "drama",
]

shelve_file = shelve.open(SHELVE_DATA, "r")
print(shelve_file.keys())


def random_street():
    street = ""
    words = random.randint(1, 2)
    street_number = random.randint(1, 150)
    length = random.randint(10, 17)
    if words > 1:
        word_length = int(length / 2)

        # ulica = str(lista[random.randint(1,25)]).upper()
        for i in range(word_length):
            if len(street) == 0:
                street = str(lista[random.randint(1, 25)]).upper()
            else:
                street += str(lista[random.randint(1, 25)])
        street += " "
        for i in range(word_length):
            if street[-1] == " ":
                if random.randint(1, 2) == 1:
                    street = str(lista[random.randint(1, 25)]).upper()
                else:
                    street += str(lista[random.randint(1, 25)])
            else:
                street += str(lista[random.randint(1, 25)])
        street += " " + str(street_number)
        return street

    elif words == 1:
        for i in range(length):
            if len(street) == 0:
                street = str(lista[random.randint(1, 25)]).upper()
            else:
                street += str(lista[random.randint(1, 25)])
        street += " " + str(street_number)
        return street
    else:
        return "Abcdef 33"


def random_city():
    gradovi = shelve_file["gradovi"]
    grad0 = random.choice(list(gradovi.items()))
    return (grad0[0], grad0[1])


def random_zip():
    return random.randint(1000, 5000)


def random_telephone():
    tel = ""
    prefixes = ["060", "061", "062", "063", "064", "065", "066", "068", "069"]
    tel += random.choice(prefixes) + "-"
    for i in range(2):
        for i2 in range(3):
            tel += str(random.randint(1, 9))
        if i != 1:
            tel += "-"
    return tel


def create_user(order: str, i: int, fnames: List[str], lnames: List[str]):
    username = order + str(i)
    email = order + str(i) + "@mejl.com"
    first_name = random.choice(fnames)
    last_name = random.choice(lnames)
    street = random_street()
    city0 = random_city()
    city1 = city0[0]
    zip = city0[1]
    telefon = random_telephone()
    if order == "korisnik":
        password = "PASSWORD1"
        novi_korisnik = User.objects.create_user(
            username=username, email=email, password=password
        )
        novi_korisnik.is_active = True
        novi_korisnik.first_name = first_name
        novi_korisnik.last_name = last_name
        novi_korisnik.save()

        is_korisnik = True
        korisnik = Korisnici(
            ulicaIBroj=street,
            brojPoste=zip,
            grad=city1,
            telefon=telefon,
            is_korisnik=is_korisnik,
        )

        korisnik.korisnik = novi_korisnik

        korisnik.save()
    else:
        password = "PASSWORD12"
        novi_korisnik = User.objects.create_user(
            username=username, email=email, password=password
        )
        novi_korisnik.is_active = True
        novi_korisnik.first_name = first_name
        novi_korisnik.last_name = last_name
        novi_korisnik.save()
        is_autor = True
        korisnik = Korisnici(
            ulicaIBroj=street,
            brojPoste=zip,
            grad=city1,
            telefon=telefon,
            is_autor=is_autor,
        )
        korisnik.korisnik = novi_korisnik
        korisnik.save()


def create_users():
    to_add = 101
    order = "korisnik"
    fajl = shelve.open(SHELVE_DATA, "r")
    fnames = fajl["imena"]
    lnames = fajl["prezimena"]
    while True:
        for i in range(1, to_add):
            create_user(order, i, fnames, lnames)

        if order == "korisnik":
            to_add -= 100 - 36
            order = "autor"
        elif order == "autor":
            break
    fajl.close()


def create_publisher():
    for i in range(6):
        name = 6 * str(lista[i]).upper()
        acc = ""
        email = ""
        while True:
            if len(acc) == 3 or len(acc) == 9:
                acc += "-"
                continue
            elif len(acc) == 12:
                break
            acc += str(random.randint(1, 9))
        if i % 2 == 0:
            email = 6 * str(lista[i]) + "@mejl.com"
        publisher = Izdavaci(ime=name, racun=acc, email=email)
        publisher.save()


def create_books():
    fajl = shelve.open(SHELVE_DATA, "r")
    knjigee = fajl["knjige"]
    for i in range(30, 500):
        isbn = ""
        strana = random.randint(50, 370)
        # cena = randrange_float(450.00,6500.00,0.50)
        godina = random.randint(2000, 2020)
        izdavac = random.randint(1, 6)
        autor = random.randint(0, 35)
        while True:
            if (len(isbn) == 3 or len(isbn) == 6) or len(isbn) == 11:
                isbn += "-"
                continue
            elif len(isbn) == 15:
                break
            isbn += str(random.randint(1, 9))
        knjigaizfajla = knjigee[i]
        cena = knjigaizfajla[2].split(",")
        tup1 = cena[0]
        tup2 = ""
        if "." in cena[0]:
            tup1 = cena[0].replace(".", "")
        if cena[1].endswith("0"):
            tup2 = cena[1][0] + "5"
        else:
            tup2 = cena[1]
        cena = float(str(tup1 + "." + tup2))
        knjiga = Knjige(
            naslov=knjigaizfajla[0],
            strana=strana,
            cena=(cena),
            godinaIzdanja=godina,
            ISBN=isbn,
            kategorija=random.choice(categories),
        )
        knjiga.izdavac = Izdavaci.objects.get(id=izdavac)
        knjiga.autor = Korisnici.objects.filter(is_autor=True)[autor]
        knjiga.kategorija = random.choice(categories)
        knjiga.save()
        fajl.close()


def create_orders():
    for i in range(79):
        narudzbina = Narudzbine()
        narudzbina.datumNarucivanja = timezone.now()
        narudzbina.placeno = False
        narudzbina.korisnik = Korisnici.objects.filter(is_korisnik=True)[
            random.randint(0, 75)
        ]
        narudzbina.save()


def create_order_items():
    # za svaku narudzbinu
    for i in range(1, 78):
        brojStavki = random.randint(1, 6)
        brojDodatihKnjiga = 0
        # dokle god nije dodato nekoliko knjiga proveravaj i dodaj
        while brojDodatihKnjiga != brojStavki:
            knjiga = random.randint(1, 140)
            narudzbina = i
            querry = StavkeNarudzbine.objects.filter(
                knjiga=knjiga, narudzbina=narudzbina
            )
            # ako ne postoji ovakav querry
            if querry.count() == 0:
                stavkeNarudzbine = StavkeNarudzbine()
                stavkeNarudzbine.kolicina = random.randint(1, 3)
                stavkeNarudzbine.knjiga = Knjige.objects.get(id=knjiga)
                stavkeNarudzbine.narudzbina = Narudzbine.objects.get(id=narudzbina)
                stavkeNarudzbine.save()
                brojDodatihKnjiga += 1


def pay_for_books():
    for i in range(1, Narudzbine.objects.count() + 1):
        daNe = [True, False]
        narudzbina = Narudzbine.objects.get(id=i)
        narudzbina.placeno = random.choice(daNe)
        narudzbina.save()


def create_comments_on_books():
    comments = [
        "Vrh knjiga preporucujem je svima!",
        "super je knjiga",
        "Morate je procitati",
        "Nisam preterano odusevljen",
        "Moglo je bolje.",
        "Knjiga je must-buy!",
        "Da li ima u knjizari u ",
        "Najbolja u kategoriji ",
        "Predivna avantura.",
    ]
    for i in range(70):
        knk = KomentariNaKnjigama()
        knk.komentar = random.choice(comments)
        knk.korisnik = Korisnici.objects.filter(is_korisnik=True)[random.randint(2, 70)]
        knk.knjiga = Knjige.objects.get(id=random.randint(3, 468))
        knk.save()


def create_ratings():
    korisnik = Korisnici.objects.get(id=72)
    knjiga = Knjige.objects.get(id=124)
    narudzbina = Narudzbine.objects.filter(korisnik=korisnik, placeno=False)[0]
    stavka = StavkeNarudzbine.objects.filter(narudzbina=narudzbina, knjiga=knjiga)
    onk = OceneKnjiga(korisnik=korisnik, ocena=5)


def set_imgs():
    counter = 0
    books: List[tuple[str, str, str]] = shelve_file["knjige"]
    books_db = Knjige.objects.filter().all()
    new_books = {}
    for book in range(len(books)):
        new_books[books[book][0]] = books[book][1]
        if book == 700:
            break
    print(len(new_books))
    print(len(books_db))
    for i in range(len(books_db)):
        title = books_db[i].naslov
        slika = books_db[i].slika
        url = new_books.get(title)
        if url:
            name = url.split("/")[9]
            location = f"/images/books/real/{name}"
            books_db[i].slika = location
            books_db[i].save()
            counter += 1
        else:
            print(title)

    print(counter)


def create_categories():
    books_db = Knjige.objects.filter().all()
    for i in range(len(books_db)):
        books_db[i].kategorija = random.choice(categories)
        books_db[i].save()


def run():
    # create_users()

    # create_publisher()

    # create_books()

    # create_orders()

    # create_order_items()

    # pay_for_books()

    # create_comments_on_books()

    set_imgs()

    # create_categories()

    # create_ratings()
