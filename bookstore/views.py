from django.shortcuts import render, redirect
from django.urls import reverse
from bookstore.basket2 import (
    init_basket,
    set_count,
    setup_user_session,
    create_order,
    create_items,
)
from bookstore.models import *
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django import forms
import re
from django.views.generic import ListView


# Create your views here.
def index(request):
    """Korisnici.objects.filter(
    korisnik=User.objects.get(id=request.session["_auth_user_id"]))"""
    init_basket(request)
    setup_user_session(request)
    najnovije_knjige = Knjige().get_najnovije()
    knjige_istorija = Knjige().get_kategorija("istorija", 5)
    knjige_filozofija = Knjige().get_kategorija("filozofija", 5)
    template = template_str(request, "index.html")
    return render(
        request,
        template,
        {
            "najnovije_knjige": najnovije_knjige,
            "knjige_istorija": knjige_istorija,
            "knjige_filozofija": knjige_filozofija,
        },
    )


def narudzbine_korisnik(request):
    narudzbine = Narudzbine().narudzbine_korisnik(request.session["_auth_user_id"])
    template = template_str(request, "narudzbine.html")
    return render(request, template, {"narudzbine": narudzbine})


def knjiga(request, isbn):
    knjiga = Knjige.objects.filter(ISBN=isbn)[0]
    placeno_poruka = "Ulogujte se"
    placeno = 0
    komentari = KomentariNaKnjigama.objects.filter(knjiga=knjiga)
    ocene = OceneKnjiga().get_ocene(knjiga)

    try:
        naruceno = Narudzbine().narudzbine_korisnik(request.session["_auth_user_id"])
        for i in naruceno:
            for j in naruceno[i]:
                if j.knjiga == knjiga:
                    if i.placeno == False:
                        placeno_poruka = "Niste platili ovu knjigu"
                        placeno = 2
                    else:
                        if len(ocene) > 0:
                            placeno_poruka = ""
                            placeno = 4
                        elif len(ocene) == 0:
                            placeno_poruka = "Budite prvi koji ce da oceni knjigu"
                            placeno = 3
                        break
                else:
                    placeno_poruka = "Niste kupili ovu knjigu"
                    placeno = 1
            if placeno in (2, 3, 4):
                naruceno = []
                break
    except:
        placeno = 0
    template = template_str(request, "knjiga.html")
    return render(
        request,
        template,
        {
            "knjiga": knjiga,
            "komentari": komentari,
            "ocene": ocene,
            "placeno": placeno,
            "placeno_poruka": placeno_poruka,
        },
    )


def author(request, id):
    author = Korisnici.objects.get(id=id)


@login_required
def user_info(request):
    user2 = get_korisnik(request)
    template = template_str(request, "user-info.html")
    return render(request, template, {"korisnik": user2})


@login_required
def user_info_update(request: HttpRequest):
    user_fields = ["first_name", "last_name"]
    korisnik_fields = ["grad", "ulicaIBroj", "telefon"]
    user = User.objects.get(id=request.session["_auth_user_id"])
    korisnik = get_korisnik(request)
    for group in [user_fields, korisnik_fields]:
        for i in group:
            field = request.POST[i]
            if i in user_fields:
                exec(f'user.{i} = "{field}" ')
            elif i in korisnik_fields:
                exec(f'korisnik.{i} = "{field}" ')
    user.save()
    korisnik.save()
    return HttpResponse(json.dumps({"ok": True}))


def basket(request: HttpRequest):
    init_basket(request)
    isbn = request.POST["ISBN"]
    action = request.POST["action"]
    response = set_count(request, isbn, action)

    if response[0] == None:
        return HttpResponse(response[1])
    elif response[1] != {}:
        return render(
            request,
            "partials/components/basket_item.html",
            {"book": response[1]},
        )

    return HttpResponse(json.dumps({"ok": response[0]}))


def basket_empty(request: HttpRequest):
    return HttpResponse(json.dumps({"ok": True}))


@csrf_exempt
def login_user(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, "partials/components/logged_user.html", {})
    return HttpResponse(json.dumps({"login": False}), content_type="application/json")


def register_user(request):
    message = False
    if len(request.POST) > 0:
        message = check_reg_form(request)
        if message == True:
            """user = User.objects.create_user(username = request.POST["username"],
            email = request.POST["email"],password = request.POST["password"])
            user.is_active = True
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            user_2 = Korisnici()
            user_2.korisnik = user
            user_2.is_korisnik = True
            user_2.save()"""
    return HttpResponse(
        json.dumps({"register": message}), content_type="application/json"
    )


def check_reg_form(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    recnik = locals()
    for i in recnik:
        if i != "request":
            if recnik[i] == "":
                return False
            elif i == "username":
                if len(User.objects.filter(username=username)) > 0:
                    return 1
            elif i == "email":
                if len(User.objects.filter(email=email)) > 0:
                    return 2
    return True


@login_required
def user_logout(request):
    logout(request)
    return render(request, "partials/components/unlogged.html")


@login_required
def narucivanje(request: HttpRequest):
    if len(request.session["korpa"]) > 0:
        narudzbina = create_order(request)
        create_items(request, narudzbina)
        return HttpResponse("Vasa narudzbina je uspesno obavljena.")
    return HttpResponse("Vasa narudzina nije obavljena.")


@login_required
def komentarisanje(request: HttpRequest):
    print(request.POST)
    komentar_obj = KomentariNaKnjigama()
    komentar_obj.korisnik = Korisnici.get_from_req(request)
    komentar_obj.knjiga = Knjige.get_from_req(request)
    komentar_obj.komentar = request.POST["komentar"]
    komentar_obj.save()
    return render(request, "partials/komentar.html", {"i": komentar_obj})


@login_required
def ocenjivanje(request):
    ocena = request.POST["ocena"]
    oceneObj = OceneKnjiga()
    oceneObj.korisnik = Korisnici.get_from_req(request)
    oceneObj.knjiga = Knjige.get_from_req(request)
    oceneObj.ocena = ocena
    oceneObj.save()
    return render(request, "partials/components/rating.html", {"i": oceneObj})


class Kategorija_view(ListView):
    model = Korisnici
    paginate_by = 12

    def get_queryset(self):
        self.template_name = template_str(self.request, "knjige.html")
        self.set_kategorija(self.request.path)
        knjige_all = Knjige.objects.filter(kategorija=self.kategorija)
        return knjige_all

    def set_kategorija(self, kategorija):
        self.kategorija = kategorija.split("/")[2]

    def get_context_data(self, **kwargs):
        context = super(Kategorija_view, self).get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        context["kategorija"] = self.kategorija
        return context


class Narudzbine_view(ListView):
    model = Narudzbine
    paginate_by = 3

    def get_queryset(self):
        self.template_name = template_str(self.request, "narudzbine.html")
        return Narudzbine.objects.filter(korisnik=get_korisnik(self.request)).all()

    def get_context_data(self, **kwargs):
        context = super(Narudzbine_view, self).get_context_data(**kwargs)
        context["narudzbina"] = Narudzbine().narudzbine_korisnik(
            self.request.session["_auth_user_id"]
        )

        return context


@login_required
def ocene_i_misljenja(request):
    ocene = OceneKnjiga.objects.filter(korisnik=request.session["_auth_user_id"])
    komentari = KomentariNaKnjigama.objects.filter(
        korisnik=request.session["_auth_user_id"]
    )
    check_data = False
    if ocene.count() > 0 or komentari.count() > 0:
        check_data = True
    template = template_str(request, "ocene-i-misljenja.html")
    return render(
        request,
        template,
        {"komentari": komentari, "ocene": ocene, "check_data": check_data},
    )


def get_korisnik(request):
    return Korisnici.objects.get(korisnik_id=request.session["_auth_user_id"])


def template_str(request, template):
    if request.headers.get("HX-Request"):
        return f"partials/{template}"
    return template


def vue(request):
    return render(request, "vue.html")
