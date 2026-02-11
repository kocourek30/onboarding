from django.urls import path
from . import views

urlpatterns = [
    path("dotazniky/", views.dotaznik_list, name="dotaznik_list"),
    path("dotazniky/novy/", views.dotaznik_create, name="dotaznik_create"),
    path("dotazniky/<int:pk>/", views.dotaznik_detail, name="dotaznik_detail"),
    path("dotazniky/<int:pk>/upravit/", views.dotaznik_update, name="dotaznik_update"),
    path(
    "dotazniky/<int:pk>/smlouva-pracovni-pomer/",
    views.smlouva_pracovni_pomer_docx,
    name="smlouva_pracovni_pomer",
),
    ]
