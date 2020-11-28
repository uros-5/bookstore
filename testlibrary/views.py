from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from testlibrary.models import *
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django import forms
from testlibrary.korpa import *
import re
from django.views.generic import ListView

# Create your views here.
def index(request):
    """ Korisnici.objects.filter(
        korisnik=User.objects.get(id=request.session["_auth_user_id"])) """
    set_korpa(request)
    setupSessionForKorisnik(request)
    najnovije_knjige = Knjige().get_najnovije()
    knjige_istorija = Knjige().get_kategorija("Istorija",5)
    knjige_filozofija = Knjige().get_kategorija("Filozofija",5)
    return render(request,"index.html",
    {"najnovije_knjige":najnovije_knjige,
    "knjige_istorija":knjige_istorija,
    "knjige_filozofija":knjige_filozofija}
    )

def narudzbine_korisnik(request):
    narudzbine = Narudzbine().narudzbine_korisnik(request.session["_auth_user_id"])
    return render(request,"narudzbine.html",{"narudzbine":narudzbine})

def knjiga(request,isbn):
    knjiga = Knjige.objects.filter(ISBN=isbn)[0]
    placeno_poruka = "Uloguj te se"
    placeno = 0
    komentari = KomentariNaKnjigama.objects.filter(knjiga = knjiga)
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
            if placeno in (2,3,4):
                naruceno = []
                break
    except:
        placeno = 0
    return render(request,"knjiga.html",{"knjiga":knjiga,"komentari":komentari,"ocene":ocene,"placeno":placeno,
    "placeno_poruka":placeno_poruka})

def author(request,id):
    author = Korisnici.objects.get(id=id)

@login_required
def user_info(request):
    print(request.session.keys())
    user2 = get_korisnik(request)
    return render(request,"user-info.html",{"korisnik":user2})

@login_required
def user_info_update(request):
    data = dict(request.POST)
    sablon = re.compile(r'userInfo\[(.*)\]')
    user_fields = ["username","email","first_name","last_name"]
    user = User.objects.get(id=request.session["_auth_user_id"])
    korisnik = get_korisnik(request)
    for i in data:
        pretraga = sablon.findall(i)
        if pretraga:
            field = pretraga[0]
            if field in user_fields:
                exec(f'user.{field} = "{data[i][0]}" ')
            else:
                exec(f'korisnik.{field} = "{data[i][0]}" ')
    user.save()
    korisnik.save()
    return HttpResponse(json.dumps({"ok":True}))

def prikaz_korpe(request):
    set_korpa(request)
    knjige = get_korpa(request)
    stavke = getStavke(knjige,Knjige)
    ukupno = set_ukupno(stavke)
    return HttpResponse(json.dumps({"stavke":stavke,"ukupno":ukupno,"ukupnoSve":ukupno}),content_type = "application/json")

def add_to_korpa(request):
    msg = add_to(request)
    return HttpResponse(json.dumps({"poruka":msg}),content_type = "application/json")

def brisanje_iz_korpe(request):
    msg = delete_item(request,request.POST["ISBN"])
    return HttpResponse(json.dumps(msg),content_type = "application/json")

def set_kolicina(request):
    radnja = request.POST["radnja"]
    knjiga = request.POST["ISBN"]
    kolicina = get_kolicina(request,knjiga)

    if(radnja == "oduzimanje"):
        return_value = reduce_kol(request,knjiga,kolicina)

    elif(radnja == "dodavanje"):
        return_value = increase_kol(request,knjiga,kolicina)
    
    return HttpResponse(json.dumps(return_value),content_type = "application/json")

def login_user(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return HttpResponse(json.dumps({"login":True}),content_type = "application/json")
        else:
            return HttpResponse(json.dumps({"login":False}),content_type = "application/json")

def register_user(request):
    if len(request.POST) > 0:
        message = check_reg_form(request)
        if message == True:
            print(message)
            """ user = User.objects.create_user(username = request.POST["username"],
            email = request.POST["email"],password = request.POST["password"])
            user.is_active = True
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            user_2 = Korisnici()
            user_2.korisnik = user
            user_2.is_korisnik = True
            user_2.save() """
        return HttpResponse(json.dumps({"register":message}),content_type = "application/json")
            
    else:
        print("not ok")

def check_reg_form(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    """ print(locals()) """
    recnik = locals()
    for i in recnik:
        if i != "request":
            if recnik[i] == "":
                return False
            elif i == "username":
                if len(User.objects.filter(username = username)) > 0:
                    return 1
            elif i == "email":
                if len(User.objects.filter(email = email)) > 0:
                    return 2
    return True

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def narucivanje(request):
    if len(request.session["korpa"])>0:
        narudzbina = kreiraj_narudzbinu(request)
        kreiraj_stavke(request,narudzbina)
        return HttpResponse(json.dumps({"narucivanje":True}),content_type = "application/json")
    return HttpResponse(json.dumps({"narucivanje":False}),content_type = "application/json")

@login_required
def komentarisanje(request):
    komentarObj = KomentariNaKnjigama()
    komentarObj.korisnik = Korisnici.get_from_req(request)
    komentarObj.knjiga = Knjige.get_from_req(request)
    komentarObj.komentari = request.POST["komentar"]
    komentarObj.save()
    return HttpResponse(json.dumps({"poruka":True}),content_type="application/json")

@login_required
def ocenjivanje(request):
    ocena = request.POST["ocena"]
    oceneObj = OceneKnjiga()
    oceneObj.korisnik = Korisnici.get_from_req(request)
    oceneObj.knjiga = Knjige.get_from_req(request)
    oceneObj.ocena = ocena
    oceneObj.save()
    return HttpResponse(json.dumps({"ocenjeno":True}),content_type="application/json")


class Kategorija_view(ListView):
    model = Korisnici
    template_name = 'knjige.html'
    paginate_by = 12

    def get_queryset(self):
        self.set_kategorija(self.request.path)
        knjige_all = Knjige.objects.filter(kategorija=self.kategorija)
        return knjige_all

    def set_kategorija(self,kategorija):
        self.kategorija = kategorija.split("/")[2]
    
    def get_context_data(self, **kwargs):
        context = super(Kategorija_view, self).get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        context["kategorija"] = self.kategorija
        return context

class Narudzbine_view(ListView):
    model = Narudzbine
    template_name = "narudzbine.html"
    paginate_by = 3
    
    def get_queryset(self):
        return Narudzbine.objects.filter(korisnik=get_korisnik(self.request)).all()
    
    """ def get_context_data(self, **kwargs):
        context = super(Narudzbine_view, self).get_context_data(**kwargs)
        context["narudzbine"] = Narudzbine().narudzbine_korisnik(request.session["_auth_user_id"])

        return context """

@login_required  
def ocene_i_misljenja(request):
    ocene = OceneKnjiga.objects.filter(korisnik=request.session["_auth_user_id"])
    komentari = KomentariNaKnjigama.objects.filter(korisnik=request.session["_auth_user_id"])
    check_data = False
    if ocene.count() > 0 or komentari.count() > 0:
        check_data = True
    return render(request,"ocene-i-misljenja.html",{"komentari":komentari,
    "ocene":ocene,"check_data":check_data})


def get_korisnik(request):
    return Korisnici.objects.get(korisnik_id= request.session["_auth_user_id"])