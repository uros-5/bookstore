from urllib.parse import quote_plus
from django import template
from django.contrib.auth.models import User
from testlibrary.models import Korisnici,Knjige,OceneKnjiga,KomentariNaKnjigama
from django.db.models import Sum
register = template.Library()

def get_korisnik(korisnik):
    return Korisnici.objects.get(korisnik=User.objects.get(username=korisnik))

@register.filter
def book_comment(knjiga,korisnik):
    comment = KomentariNaKnjigama.objects.filter(knjiga=knjiga,korisnik=get_korisnik(korisnik))
    if comment.count() > 0:
        return comment
    else:
        return "///"

@register.filter
def book_rating(knjiga,korisnik):
    rating = OceneKnjiga.objects.filter(knjiga=knjiga,korisnik=get_korisnik(korisnik))
    if rating.count() > 0:
        return "a"*rating[0].ocena
    else:
        return "///"

@register.filter
def calculate_rating(ocena):
    return "a"*ocena