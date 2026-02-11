from django.db import models
from django.contrib.auth.models import AbstractUser


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


class Uzivatel(AbstractUser):
    HR = "HR"
    OBLASTNI = "OBL"
    MANAZER = "MAN"

    ROLE_CHOICES = [
        (HR, "HR"),
        (OBLASTNI, "Oblastní manažer"),
        (MANAZER, "Manažer provozu"),
    ]

    role = models.CharField(
        "Role",
        max_length=3,
        choices=ROLE_CHOICES,
        default=MANAZER,
    )
    provozy = models.ManyToManyField(
        Provoz,
        blank=True,
        related_name="uzivatele",
        verbose_name="Provozy",
    )

    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"

    def __str__(self):
        if self.is_superuser:
            return f"{self.username} (Superadmin)"
        return f"{self.username} ({self.get_role_display()})"
