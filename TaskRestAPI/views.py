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
            korisnik.is_korisnik = True
            korisnik.save()
            return HttpResponseRedirect(reverse('index'))
        else:
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
            return render(request,'public/login.html',{'form':form})
    else:
        form = Form_login()
        return render(request,'public/login.html',{'form':form})
class Form_login(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password",widget=forms.PasswordInput)
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
    return render(request,'public/logout.html')

# za prikaz liste
class Korisnici_lista(ListView):

    model = Korisnici
    template_name = 'public/lista_korisnika.html'
    paginate_by = 0
    def get_queryset(self):
        queryset = Korisnici.objects.all().order_by('username')
        return queryset

class Korisnici_lista(ListView):

    model = Korisnici
    template_name = 'public/lista_korisnika.html'
    paginate_by = 5
    def get_queryset(self):
        queryset = Korisnici.objects.filter(is_korisnik=True)
        print(queryset.count())
        return queryset