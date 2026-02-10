from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Provoz(models.Model):
    cislo_provozu = models.IntegerField("Číslo provozu")
    nazev = models.CharField("Název", max_length=255)
    ulice = models.CharField("Ulice", max_length=255, blank=True)
    mesto = models.CharField("Město", max_length=255, blank=True)
    kraj = models.CharField("Kraj", max_length=255, blank=True)
    psc = models.CharField("PSČ", max_length=20, blank=True)
    manazer = models.CharField("Manažer", max_length=255, blank=True)
    email = models.EmailField("E‑mail", blank=True)

    class Meta:
        verbose_name = "Provoz"
        verbose_name_plural = "Provozy"

    def __str__(self):
        return f"{self.cislo_provozu} – {self.nazev}"

    def spravci_jmena(self):
        # uzivatele = related_name z ManyToMany v UzivatelskyProfil
        profily = self.uzivatele.select_related("user").all()
        return ", ".join(p.user.username for p in profily)

    spravci_jmena.short_description = "Správci"


class UzivatelskyProfil(models.Model):
    ROLE_HR = "HR"
    ROLE_OBLASTNI = "OBL"
    ROLE_MANAZER = "MAN"

    ROLE_CHOICES = [
        (ROLE_HR, "HR"),
        (ROLE_OBLASTNI, "Oblastní manažer"),
        (ROLE_MANAZER, "Manažer provozu"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=ROLE_MANAZER)
    provozy = models.ManyToManyField(Provoz, blank=True, related_name="uzivatele")

    class Meta:
        verbose_name = "Uživatelský profil"
        verbose_name_plural = "Uživatelské profily"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=User)
def create_or_update_profil(sender, instance, created, **kwargs):
    if created:
        UzivatelskyProfil.objects.create(user=instance)
    else:
        UzivatelskyProfil.objects.get_or_create(user=instance)
