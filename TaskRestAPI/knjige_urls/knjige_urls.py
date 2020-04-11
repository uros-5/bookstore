from django.urls import path
from django.urls import include
from django.conf.urls import url
from TaskRestAPI.views import knjiga_look
urlpatterns = [
    path(r'^(?P<br>[\d]+)$',knjiga_look,name="test")
]