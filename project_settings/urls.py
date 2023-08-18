"""project_settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookstore import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # KNJIGE
    path("", views.index, name="index"),
    path("knjiga/<str:isbn>", views.knjiga, name="knjiga"),
    path("narucivanje/", views.narucivanje, name="narucivanje"),
    path("komentarisanje/", views.komentarisanje, name="komentarisanje"),
    path("ocenjivanje", views.ocenjivanje, name="ocenjivanje"),
    path(
        "kategorija/<str:kategorija>",
        views.Kategorija_view.as_view(),
        name="kategorija",
    ),
    path("narudzbine", views.Narudzbine_view.as_view(), name="narudzbine"),
    # KORPA
    path("basket", views.basket),
    path("basket_empty", views.basket_empty),
    # KORISNIK
    path("log-user/", views.login_user, name="log-user"),
    path("reg-user", views.register_user, name="reg-user"),
    path("user_info", views.user_info, name="user_info"),
    path("user-info-update", views.user_info_update, name="user-info-update"),
    path("ocene-i-misljenja", views.ocene_i_misljenja, name="ocene_i_misljenja"),
    path("logout", views.user_logout, name="logout"),
    path("author/<int:id>", views.author, name="author"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
