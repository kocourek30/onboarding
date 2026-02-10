from django.contrib import admin
from django.contrib.auth.models import User
from .models import Provoz, UzivatelskyProfil

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
    list_filter = ("mesto", "kraj", "manazer")
    list_per_page = 10000


class UzivatelskyProfilInline(admin.StackedInline):
    model = UzivatelskyProfil
    can_delete = False
    filter_horizontal = ("provozy",)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser")
    inlines = [UzivatelskyProfilInline]

# odregistruj defaultního User admina a zaregistruj našeho
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
