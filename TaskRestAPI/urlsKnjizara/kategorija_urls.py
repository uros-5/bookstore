from django.urls import path,re_path
from django.urls import include
from django.conf.urls import url
from TaskRestAPI.viewsKnjizara.kategorijaViews import Kategorija_look,knjiga_look

urlpatterns = [
	path('ljubavni_roman/', Kategorija_look.as_view(), name="ljubavni_roman"),
	path(r'ljubavni_roman/<str:ISBN>/',knjiga_look,name="ljubavni_roman_id"),

	path('istorija/', Kategorija_look.as_view(), name="istorija"),
	path(r'istorija/<str:ISBN>/',knjiga_look,name="istorija_id"),

	path('horor/', Kategorija_look.as_view(), name="horor"),
	path(r'horor/<str:ISBN>/',knjiga_look,name="horor_id"),

	path('filozofija/', Kategorija_look.as_view(), name="filozofija"),
	path(r'filozofija/<str:ISBN>/',knjiga_look,name="filozofija_id"),

	path('fantastika/', Kategorija_look.as_view(), name="fantastika"),
	path(r'fantastika/<str:ISBN>/',knjiga_look,name="fantastika_id"),

	path('drama/', Kategorija_look.as_view(), name="drama"),
	path(r'drama/<str:ISBN>/',knjiga_look,name="drama_id"),

	path("pretraga", Kategorija_look.as_view(), name="pretraga")

]



