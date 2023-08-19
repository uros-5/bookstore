from bookstore.models import *
from typing import Tuple, Union


def setup_user_session(request):
    if "korisnik" not in request.session.keys():
        if "_auth_user_id" in request.session.keys():
            korisnik1 = Korisnici.objects.filter(
                korisnik_id=request.session["_auth_user_id"]
            )
            if len(korisnik1) > 0:
                request.session["korisnik"] = korisnik1[0].id


def init_basket(request):
    if "korpa" not in request.session.keys():
        request.session["korpa"] = {}


def set_count(
    request, isbn: str, action: str
) -> Tuple[Union[bool, None], Union[dict, str]]:
    book = request.session["korpa"].get(isbn)
    if action == "a":
        return add_book(request, isbn)
    elif action == "d":
        deleted = request.session["korpa"].pop(isbn, 0)
        request.session.save()
        if deleted == 0:
            return (False, {})
        else:
            return (True, {})
    elif book == None:
        return (False, {})
    elif action == "+":
        request.session["korpa"][isbn]["count"] += 1
        request.session.save()
        return (True, {})
    elif action == "-":
        request.session["korpa"][isbn]["count"] -= 1
        if request.session["korpa"][isbn]["count"] <= 1:
            request.session["korpa"][isbn]["count"] = 1
        request.session.save()
        return (True, {})
    else:
        return (False, {})


def add_book(request, isbn) -> Tuple[Union[bool, None], Union[dict, str]]:
    POST = request.POST
    knjige = Knjige.objects.filter(ISBN=POST["ISBN"])
    if len(knjige) == 1:
        basket = request.session["korpa"]
        if basket.get(isbn) != None:
            return (None, '<span style="display: none;"></span>')
        book = {
            "count": 1,
            "cena": f"{knjige[0].cena}",
            "img": knjige[0].slika.name,
            "ISBN": knjige[0].ISBN,
        }
        basket[POST["ISBN"]] = book
        request.session["korpa"] = basket
        return (True, book)
    return (False, {})


def create_order(request: HttpRequest):
    order = Narudzbine()
    order.datumNarucivanja = timezone.now()
    order.placeno = True
    order.korisnik = Korisnici.objects.filter(
        korisnik=User.objects.get(id=request.session["_auth_user_id"])
    )[0]
    order.save()
    return order


def create_items(request: HttpRequest, narudzbina):
    korpa = request.session["korpa"]
    for k, v in korpa.items():
        item = StavkeNarudzbine(narudzbina=narudzbina)
        item.knjiga = Knjige.objects.filter(ISBN=k)[0]
        item.kolicina = v["count"]
        item.save()
    request.session["korpa"] = {}
