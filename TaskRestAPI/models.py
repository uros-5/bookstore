from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class Korisnici(AbstractUser):
    ulicaIBroj = models.CharField(max_length=45, verbose_name="ulicaIBroj",null=True,default=None,blank=True)
    brojPoste = models.IntegerField(verbose_name="brojPoste",null=True,blank=True)
    grad = models.CharField(max_length=20, verbose_name="grad",null=True,default=None,blank=True)
    telefon = models.CharField(max_length=20, verbose_name="telefon",null=True,default=None,blank=True)
    is_korisnik = models.BooleanField(verbose_name='korisnikstatus', default=True)
    is_autor = models.BooleanField(verbose_name='autorstatus', default=False)

    def __str__(self):
        if(self.is_autor):
            return str(self.first_name + " " + self.last_name)
        else:
            return self.username




class Izdavaci(models.Model):
    ime = models.CharField(max_length=45, verbose_name="ime")
    racun = models.CharField(max_length=45, verbose_name="racun",null=True,default=None,blank=True)
    email = models.EmailField(max_length=70,null=True,blank=True,default=None)
    def __str__(self):
        return self.ime



class Narudzbine(models.Model):
    datumNarucivanja = models.DateTimeField(auto_now_add=timezone.now(),verbose_name="datumNarucivanja",null=True,blank=True)
    datumPrijema = models.DateTimeField(verbose_name="datumPrijema",null=True,blank=True,default=None)
    placeno = models.BooleanField(verbose_name="placeno",null=True,default=False,blank=True)
    korisnik = models.ForeignKey(Korisnici,verbose_name="korisnik",related_name="korisnik+",on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)

class Knjige(models.Model):
    kategorije = ()
    naslov = models.CharField(max_length=30, verbose_name="naslov")
    strana = models.IntegerField(verbose_name="strana",null=True,default=None,blank=True)
    cena = models.DecimalField(verbose_name="cena",max_digits=6, decimal_places=2)
    opis = models.TextField(verbose_name="opis",max_length=300,null=True,default=None,blank=True)
    godinaIzdanja = models.IntegerField(verbose_name="godinaIzdanja", default=2020)
    ISBN = models.CharField(verbose_name="ISBN",max_length=28)
    slika = models.ImageField(upload_to=None, height_field=None, width_field=None,null=True,default=None,blank=True)
    kategorija = models.CharField(choices=kategorije,verbose_name="kategorija",max_length=30,default="")
    izdavac = models.ForeignKey(Izdavaci,verbose_name="izdavac",related_name="izdavac+",on_delete=models.CASCADE)
    autor = models.ForeignKey(Korisnici,verbose_name="autor",related_name="autor+", on_delete=models.CASCADE)
    def __str__(self):
        return self.naslov

class StavkeNarudzbine(models.Model):
    kolicina = models.IntegerField(verbose_name="kolicina",default=1)
    narudzbina = models.ForeignKey(Narudzbine,verbose_name="narudzbina",related_name="narudzbina+",on_delete=models.CASCADE)
    knjiga = models.ForeignKey(Knjige,verbose_name="knjiga",related_name="knjiga+",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)


class OceneKnjiga(models.Model):
    ocena = models.IntegerField(verbose_name="ocena",default=1)
    korisnik = models.ForeignKey(Korisnici, verbose_name="korisnik", related_name="korisnik+",on_delete=models.CASCADE)
    knjiga = models.ForeignKey(Knjige, verbose_name="knjiga", related_name="knjigaID+",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.ocena)

class KomentariNaKnjigama(models.Model):
    komentar = models.TextField(verbose_name="komentar",max_length=112,null=True,default="",blank=True)
    korisnik = models.ForeignKey(Korisnici, verbose_name="korisnik", related_name="korisnik+",on_delete=models.CASCADE)
    knjiga = models.ForeignKey(Knjige, verbose_name="knjiga", related_name="knjiga+", on_delete=models.CASCADE)
    def __str__(self):
        return self.komentar