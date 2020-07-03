from django.urls import path
from django.urls import include
from django.conf.urls import url
from TaskRestAPI.views import *

urlpatterns = [
	path('ljubavni_roman/', include('TaskRestAPI.knjige_urls.ljubavni_roman'), name="ljubavni_roman/"),
	path('istorija/', include('TaskRestAPI.knjige_urls.istorija'), name="istorija/"),
	path('horor/', include('TaskRestAPI.knjige_urls.horor'), name="horor/"),
	path('filozofija/', include('TaskRestAPI.knjige_urls.filozofija'), name="filozofija/"),
	path('fantastika/', include('TaskRestAPI.knjige_urls.fantastika'), name="fantastika/"),
	path('drama/', include('TaskRestAPI.knjige_urls.drama'), name="drama/"),
	path("pretraga", Kategorija_look.as_view(), name="pretraga")
]



