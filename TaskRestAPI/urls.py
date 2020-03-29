from django.urls import path
from django.urls import include
from TaskRestAPI import views
from django.conf.urls import url
urlpatterns = [
    path(r'index',views.index,name="index"),
]
