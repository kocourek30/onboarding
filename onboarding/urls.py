from django.urls import path
from . import views

urlpatterns = [
    path("dotazniky/", views.dotaznik_list, name="dotaznik_list"),
    path("dotazniky/novy/", views.dotaznik_create, name="dotaznik_create"),
]
