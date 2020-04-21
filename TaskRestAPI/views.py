from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
# from TaskRestAPI.models import Narudzbine
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from TaskRestAPI.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
# Create your views here.

def index(request):
    return render(request,'public/index.html')

#registracija
def regpage(request):
    if request.POST:
        form = Registraciona_forma(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            userType = form.cleaned_data["userType"]

            novi_korisnik = User.objects.create_user(username=username,
                                                     email=email,
                                                     password=password
                                                     )
            novi_korisnik.is_active = True
            novi_korisnik.first_name = first_name
            novi_korisnik.last_name = last_name
            novi_korisnik.save()

            korisnik = Korisnici()
            korisnik.korisnik = novi_korisnik

            if (str(userType) == "korisnik"):
                korisnik.is_korisnik = True
            elif (str(userType) == "autor"):
                korisnik.is_autor = True
            korisnik.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print("okkk")
            return render(request,'public/registracija.html',{'form':form})
    else:

        form = Registraciona_forma()
        return render(request,'public/registracija.html',{'form':form})
class Registraciona_forma(forms.Form):
    first_name = forms.CharField(label="first_name",max_length=30)
    last_name = forms.CharField(label="last_name",max_length=150)
    username = forms.CharField(label="username",max_length=150)
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password",widget=forms.PasswordInput)
    password_bis = forms.CharField(label="password",widget=forms.PasswordInput)
    CHOICES = (('korisnik', 'korisnik'),
               ('autor', 'autor'))
    userType = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    def clean(self):
        cleaned_data = super(Registraciona_forma,self).clean()
        password = self.cleaned_data.get("password")
        password_bis = self.cleaned_data.get("password_bis")
        if password and password_bis and password != password_bis:
            raise forms.ValidationError("Sifre nisu iste!")
        return self.cleaned_data


# unosne forme

# class Registraciona_forma(CreateView):
    # model = Korisnici
    # template_name = 'public/registracija.html'
    # success_url = "index"
    # fields = ("first_name", "last_name", "username", "email", "password")

class Unos_knjiga_forma(CreateView):
    model = Knjige
    template_name='public/unos_knjige.html'
    success_url="index"
    fields=("naslov","cena","ISBN","kategorija","izdavac")

    def get_context_data(self, **kwargs):
        context = super(Unos_knjiga_forma, self).get_context_data(**kwargs)
        korisnici = Korisnici.objects.filter(is_autor=True)
        lista = []
        for i in range(len(korisnici)):
            lista.append(korisnici[i].korisnik_id)
        context['ids'] = lista
        return context
class Dodavanje_stavki_narudzbine_forma(CreateView):
    model = StavkeNarudzbine
    template_name = 'public/dodavanje_stavke_narudzbine.html'
    success_url = "index"
    fields = ("kolicina", "knjiga")
class Ocenjivanje_knjiga_forma(CreateView):
    model = OceneKnjiga
    template_name = 'public/ocenjivanje_knjiga.html'
    success_url = "index"
    fields = ("ocena",)
class Komentarisanje_knjiga_forma(CreateView):
    model = KomentariNaKnjigama
    template_name = 'public/komentarisanje_knjiga.html'
    success_url = "index"
    fields = ("komentar",)

# login korisnika
def login_korisnika(request):
    if ("korisnikInfoId" not in request.session.keys()):
        if ("_auth_user_id" in request.session.keys()):
            korisnik1 = Korisnici.objects.filter(korisnik_id=request.session["_auth_user_id"])
            if(len(korisnik1)>0):
                request.session["korisnikInfoId"] = korisnik1[0].id
    if request.POST:
        print("jeste")
        form = Form_login(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                print("postoji")
                login(request,user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])
                return HttpResponseRedirect(reverse('index'))
        else:
            print("pogresno")
            return render(request, 'public/korisnik/nalog.html', {'form':form})
    else:
        form = Form_login()
        return render(request, 'public/korisnik/nalog.html', {'form':form})
class Form_login(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Lozinka",widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(Form_login,self).clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if not authenticate(username=username,password=password):
            raise forms.ValidationError("Wrong login or password!")
        return self.cleaned_data

#logout korisnika
def logout_korisnika(request):
    logout(request)
    return render(request, 'public/korisnik/logout.html')

# za prikaz liste
class Korisnici_lista(ListView):

    model = Korisnici
    template_name = 'public/lista_korisnika.html'
    paginate_by = 5
    def get_queryset(self):
        queryset = Korisnici.objects.filter(is_korisnik=True)
        lista = []
        for i in range(len(queryset)):
            recnik = {}
            recnik.setdefault("ulicaIBroj",queryset[i].ulicaIBroj)
            recnik.setdefault("brojPoste", queryset[i].brojPoste)
            recnik.setdefault("grad", queryset[i].grad)
            recnik.setdefault("telefon", queryset[i].telefon)

            user = User.objects.get(id=queryset[i].korisnik_id)
            recnik.setdefault("first_name",user.first_name)
            recnik.setdefault("last_name", user.last_name)
            recnik.setdefault("username", user.username)

            lista.append(recnik)

            user = None

        return lista

        # return queryset
class Korisnici_podaci(DetailView):
    model = Korisnici
    template_name = 'public/korisnik/korisnik_podaci.html'

    def get_context_data(self, **kwargs):
        context = super(Korisnici_podaci, self).get_context_data(**kwargs)
        korisnik = Korisnici.objects.get(korisnik_id=self.object.id)
        context["korisnik"] = korisnik
        return context

class Korisnici_narudzbine(ListView):
    model = Korisnici
    template_name = 'public/korisnik/narudzbine.html'
    paginate_by = 5

    def get_queryset(self):
        narudzbine_korisnika = Narudzbine.objects.filter(korisnik_id=self.request.session["korisnikInfoId"])
        narudzbine = []
        if (len(narudzbine_korisnika) > 0):
            narudzbine = []
            # narudzbine = [[{'id':6,'poslato':"ne"},["naslov","cena","kom"],["naslov","cena","kom"]]]
            for i in range(len(narudzbine_korisnika)):
                narudzbina = []
                narudzbina.append(
                    {'id': narudzbine_korisnika[i].id, 'placeno': narudzbine_korisnika[i].placeno, 'ukupno': 0,
                     'kolicina': 0,'datum':narudzbine_korisnika[i].datumNarucivanja})
                stavke_narudzbine = StavkeNarudzbine.objects.filter(narudzbina_id=narudzbine_korisnika[i].id)
                knjige = []

                for i2 in range(len(stavke_narudzbine)):
                    knjiga0 = []
                    knjiga = Knjige.objects.get(id=stavke_narudzbine[i2].knjiga_id)
                    knjiga0.append(knjiga.naslov)
                    knjiga0.append(float(knjiga.cena))
                    narudzbina[0]['kolicina'] += stavke_narudzbine[i2].kolicina
                    narudzbina[0]['ukupno'] += float(knjiga.cena*stavke_narudzbine[i2].kolicina)
                    knjiga0.append(stavke_narudzbine[i2].kolicina)
                    knjiga0.append(knjiga.slika)
                    knjige.append(knjiga0)
                if(len(stavke_narudzbine)>0):
                    narudzbina.append(knjige)
                    narudzbine.append(narudzbina)
        print(len(narudzbine))
        return narudzbine

class Korisnici_ocenjene_knjige(ListView):
    model = Korisnici
    template_name = 'public/korisnik/ocenjene_knjige.html'
    paginate_by = 5

    def get_queryset(self):
        ocene = OceneKnjiga.objects.filter(korisnik_id=self.request.session["korisnikInfoId"])
        lista = []

        for i in range(len(ocene)):
            review = {}
            review.setdefault('ocena',ocene[i].ocena)
            knjiga = Knjige.objects.get(id=ocene[i].knjiga_id)
            review.setdefault('naslov',knjiga.naslov)
            lista.append(review)
        return lista
# class Knjiga_look(ListView):
#     model = Knjige
#     template_name = 'public/test.html'
#     paginate_by = 5
#
#     def get_queryset(self):
#         br = 1
#         return [br]

class Kategorija_look(ListView):
    model = Korisnici
    template_name = 'public/knjige.html'
    paginate_by = 12

    def get_queryset(self):
        # print(self.request.path)
        if (str(self.request.path) == "/ljubavni_roman/"):
            knjige_all = Knjige.objects.filter(kategorija="Ljubavni roman")
            return knjige_all
        elif (self.request.path == "/istorija/"):
            knjige_all = Knjige.objects.filter(kategorija="Istorija")
            return knjige_all

        elif (self.request.path == "/fantastika/"):
            knjige_all = Knjige.objects.filter(kategorija="Fantastika")
            return knjige_all

        elif (self.request.path == "/filozofija/"):
            knjige_all = Knjige.objects.filter(kategorija="Filozofija")
            return knjige_all

        elif (self.request.path == "/horor/"):
            knjige_all = Knjige.objects.filter(kategorija="Horor")
            return knjige_all

        elif (self.request.path == "/drama/"):
            knjige_all = Knjige.objects.filter(kategorija="Drama")
            return knjige_all



def knjiga_look(request,ISBN=0):
    print(request.path)
    if (request.path.startswith("/ljubavni_roman/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)[0].id
        oceneLista = oceneKnjiga(knjiga)

        return render(request,'public/knjiga.html',{"knjiga":Knjige.objects.get(id=knjiga),"ocene":oceneLista})

    elif (request.path.startswith("/istorija/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)[0].id
        oceneLista = oceneKnjiga(ISBN)
        return render(request, 'public/knjiga.html', {"knjiga": Knjige.objects.get(id=knjiga), "ocene": oceneLista})

    elif (request.path.startswith("/fantastika/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)[0].id
        oceneLista = oceneKnjiga(knjiga)
        komentarLista = komentari(knjiga)
        print(len(komentarLista))
        return render(request, 'public/knjiga.html', {"knjiga": Knjige.objects.get(id=knjiga), "ocene": oceneLista,
                                                      "komentarLista":komentarLista})

    elif (request.path.startswith("/filozofija/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)
        return render(request, 'public/knjiga.html', {"knjiga": Knjige.objects.get(id=knjiga[0].id)})

    elif (request.path.startswith("/horor/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)
        return render(request, 'public/knjiga.html', {"knjiga": Knjige.objects.get(id=knjiga[0].id)})

    elif (request.path.startswith("/drama/")):
        knjiga = Knjige.objects.filter(ISBN=ISBN)
        return render(request, 'public/knjiga.html', {"knjiga": Knjige.objects.get(id=knjiga[0].id)})

def oceneKnjiga(knjigaID):
    oceneLista = []
    knjiga = knjigaID
    ocene = OceneKnjiga.objects.filter(knjiga=knjiga)
    for i in range(len(ocene)):
        ocena = ocene[i].ocena
        username = ocene[i].korisnik
        oceneLista.append([username, ocena])
    return oceneLista
def komentari(knjigaID):
    komentarLista = []
    komentari = KomentariNaKnjigama.objects.filter(knjiga=knjigaID,odobren=True)
    for i in range(len(komentari)):
        korisnik = Korisnici.objects.get(id=komentari[i].korisnik.id)
        grad = korisnik.grad
        komentar = komentari[i].komentar
        username = komentari[i].korisnik
        komentarLista.append([username,grad,komentar])
    return komentarLista
