from urllib.parse import quote_plus
from django import template
from bookstore.models import StavkeNarudzbine
from django.db.models import Sum

register = template.Library()


@register.filter
def stavka_ukupno(narudzbina, kolicina_search=False):
    ukupno = 0
    stavke = StavkeNarudzbine.objects.filter(narudzbina=narudzbina).all()
    for i in stavke:
        ukupno += i.knjiga.cena * i.kolicina
    return round(float(ukupno), 2)


@register.filter
def stavke_kolicina(narudzbina):
    kolicina = StavkeNarudzbine.objects.filter(narudzbina=narudzbina).aggregate(
        Sum("kolicina")
    )
    StavkeNarudzbine.objects.filter(narudzbina=narudzbina).aggregate(Sum("kolicina"))
    return kolicina["kolicina__sum"]


@register.filter
def get_stavke(narudzbina):
    return StavkeNarudzbine.objects.filter(narudzbina=narudzbina).all()
