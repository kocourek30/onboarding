from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Provoz, Uzivatel


@admin.register(Provoz)
class ProvozAdmin(admin.ModelAdmin):
    list_display = (
        "cislo_provozu",
        "nazev",
        "ulice",
        "mesto",
        "kraj",
        "psc",
        "manazer",
        "email",
        "spravci_jmena",
    )
    search_fields = (
        "cislo_provozu",
        "nazev",
        "ulice",
        "mesto",
        "kraj",
        "psc",
        "manazer",
        "email",
    )
    list_filter = ("cislo_provozu", "mesto", "kraj", "manazer")
    list_per_page = 10000

    def spravci_jmena(self, obj):
        uzivatele = obj.uzivatele.all()
        return ", ".join(u.username for u in uzivatele)
    spravci_jmena.short_description = "Správci"


@admin.register(Uzivatel)
class UzivatelAdmin(UserAdmin):
    model = Uzivatel

    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Osobní údaje", {"fields": ("first_name", "last_name", "email")}),
        ("Role a provozy", {"fields": ("role", "provozy")}),
        ("Oprávnění", {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
        ("Důležité termíny", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "role", "provozy"),
        }),
    )

    filter_horizontal = ("provozy", "groups")
