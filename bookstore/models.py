from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.http import HttpRequest

User._meta.get_field("email")._unique = True
# Create your models here.


class Korisnici(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    ulicaIBroj = models.CharField(
        max_length=45, verbose_name="ulicaIBroj", null=True, default=None, blank=True
    )
    brojPoste = models.IntegerField(verbose_name="brojPoste", null=True, blank=True)
    grad = models.CharField(
        max_length=20, verbose_name="grad", null=True, default=None, blank=True
    )
    telefon = models.CharField(
        max_length=20, verbose_name="telefon", null=True, default=None, blank=True
    )
    is_korisnik = models.BooleanField(verbose_name="korisnikstatus", default=False)
    is_autor = models.BooleanField(verbose_name="autorstatus", default=False)

    def __str__(self):
        if self.is_autor:
            return str(self.korisnik.first_name + " " + self.korisnik.last_name)
        else:
            return self.korisnik.username

    @staticmethod
    def get_from_req(request: HttpRequest):
        return Korisnici.objects.filter(
            korisnik=User.objects.get(id=request.session["_auth_user_id"])
        )[0]


class Izdavaci(models.Model):
    ime = models.CharField(max_length=45, verbose_name="ime")
    racun = models.CharField(
        max_length=45, verbose_name="racun", null=True, default=None, blank=True
    )
    email = models.EmailField(max_length=70, null=True, blank=True, default=None)

    def __str__(self):
        return self.ime


class Narudzbine(models.Model):
    datumNarucivanja = models.DateTimeField(
        auto_now_add=timezone.now(),
        verbose_name="datumNarucivanja",
        null=True,
        blank=True,
    )
    datumPrijema = models.DateTimeField(
        verbose_name="datumPrijema", null=True, blank=True, default=None
    )
    placeno = models.BooleanField(
        verbose_name="placeno", null=True, default=False, blank=True
    )
    korisnik = models.ForeignKey(
        Korisnici,
        verbose_name="korisnik",
        related_name="korisnik+",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("id", "korisnik")

    def __str__(self):
        return str(self.id)

    def narudzbine_korisnik(self, korisnik_id):
        narudzbine = Narudzbine.objects.filter(
            korisnik=Korisnici.objects.get(korisnik_id=korisnik_id)
        )
        korisnik_naruceno = {}
        for i in narudzbine:
            stavke = StavkeNarudzbine.objects.filter(narudzbina=i)
            stavke_2 = []
            for j in stavke:
                stavke_2.append(j)
            korisnik_naruceno.setdefault(i, stavke_2)
        return korisnik_naruceno


class Knjige(models.Model):
    kategorije = ()
    naslov = models.CharField(max_length=30, verbose_name="naslov")
    strana = models.IntegerField(
        verbose_name="strana", null=True, default=None, blank=True
    )
    cena = models.DecimalField(verbose_name="cena", max_digits=9, decimal_places=2)
    opis = models.TextField(
        verbose_name="opis", max_length=300, null=True, default=None, blank=True
    )
    godinaIzdanja = models.IntegerField(verbose_name="godinaIzdanja", default=2020)
    ISBN = models.CharField(verbose_name="ISBN", max_length=28, unique=True)
    slika = models.ImageField(
        upload_to="images/books/real",
        height_field=None,
        width_field=None,
        null=True,
        default=None,
        blank=True,
    )
    kategorija = models.CharField(
        choices=kategorije, verbose_name="kategorija", max_length=30, default=""
    )
    izdavac = models.ForeignKey(
        Izdavaci,
        verbose_name="izdavac",
        related_name="izdavac+",
        on_delete=models.CASCADE,
    )
    autor = models.ForeignKey(
        Korisnici, verbose_name="autor", related_name="autor+", on_delete=models.CASCADE
    )

    # class Meta:
    #     unique_together = ('ISBN','','')
    def __str__(self):
        return self.naslov

    def get_kategorija(self, kategorija, length):
        knjige = Knjige.objects.filter(kategorija=kategorija)[0:length][:]
        return list(knjige)

    def get_najnovije(self):
        return Knjige.objects.order_by("-id")[:5].all()

    def for_korpa(knjiga, stavka):
        return {
            "isbn": knjiga.ISBN,
            "slika": str(knjiga.slika),
            "naslov": knjiga.naslov,
            "cena": round(float(knjiga.cena), 2),
            "kolicina": stavka["kolicina"],
            "ukupno": round(float(knjiga.cena * stavka["kolicina"]), 2),
        }

    @staticmethod
    def get_from_req(request):
        return Knjige.objects.filter(ISBN=request.POST["ISBN"])[0]


class StavkeNarudzbine(models.Model):
    kolicina = models.IntegerField(verbose_name="kolicina", default=1)
    narudzbina = models.ForeignKey(
        Narudzbine,
        verbose_name="narudzbina",
        related_name="narudzbina+",
        on_delete=models.CASCADE,
    )
    knjiga = models.ForeignKey(
        Knjige, verbose_name="knjiga", related_name="knjiga+", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("narudzbina", "knjiga")

    def __str__(self):
        return str(self.id)


class OceneKnjiga(models.Model):
    ocena = models.IntegerField(verbose_name="ocena", default=1)
    korisnik = models.ForeignKey(
        Korisnici,
        verbose_name="korisnik",
        related_name="korisnik+",
        on_delete=models.CASCADE,
    )
    knjiga = models.ForeignKey(
        Knjige,
        verbose_name="knjiga",
        related_name="knjigaID+",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.ocena)

    def get_ocene(self, knjiga):
        return OceneKnjiga.objects.filter(knjiga=knjiga).all()


# filter(kategorija = "Fantastika").order_by("-id")[:5]
class KomentariNaKnjigama(models.Model):
    komentar = models.TextField(
        verbose_name="komentar", max_length=112, null=True, default="", blank=True
    )
    korisnik = models.ForeignKey(
        Korisnici,
        verbose_name="korisnik",
        related_name="korisnik+",
        on_delete=models.CASCADE,
    )
    knjiga = models.ForeignKey(
        Knjige, verbose_name="knjiga", related_name="knjiga+", on_delete=models.CASCADE
    )
    odobren = models.BooleanField(
        verbose_name="odobren", null=True, default=False, blank=True
    )

    def __str__(self):
        return self.komentar

    def get_komentari(self, knjiga):
        return self.objects.get(knjiga=knjiga)


class UtisciKorisnika(models.Model):
    komentar = models.CharField(
        max_length=50, verbose_name="komentar", null=False, default=None, blank=False
    )
    korisnik = models.ForeignKey(
        Korisnici,
        verbose_name="korisnik",
        related_name="korisnik+",
        on_delete=models.CASCADE,
    )
    odobren = models.BooleanField(
        verbose_name="odobren", null=True, default=False, blank=True
    )
    datum = models.DateTimeField(
        verbose_name="datum", null=True, blank=True, default=None
    )

    def get_najnovije(self):
        return self.objects.order_by("-id")[:5].all()
