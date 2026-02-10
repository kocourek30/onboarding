from django.contrib import admin
from .models import OsobniDotaznik, Pozice


@admin.register(OsobniDotaznik)
class OsobniDotaznikAdmin(admin.ModelAdmin):
    list_display = ("jmeno", "prijmeni", "provoz", "pozice", "datum_vytvoreni", "vytvoril")
    search_fields = ("jmeno", "prijmeni", "rodne_cislo", "provoz__nazev", "pozice__nazev")
    list_filter = ("provoz", "pozice", "datum_vytvoreni")
    readonly_fields = ("vytvoril",)


@admin.register(Pozice)
class PoziceAdmin(admin.ModelAdmin):
    list_display = ("nazev", "kod")
    search_fields = ("nazev", "kod")
