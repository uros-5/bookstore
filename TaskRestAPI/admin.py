from django.contrib import admin
from TaskRestAPI.models import *
# Register your models here.

admin.autodiscover()

admin.site.register(Korisnici)
admin.site.register(Izdavaci)
admin.site.register(Narudzbine)
admin.site.register(Knjige)
admin.site.register(StavkeNarudzbine)
admin.site.register(OceneKnjiga)
admin.site.register(KomentariNaKnjigama)
