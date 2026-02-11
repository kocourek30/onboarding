from django.db import models
from django.conf import settings
from provozy.models import Provoz


class Pozice(models.Model):
    nazev = models.CharField("Název pozice", max_length=150, unique=True)
    kod = models.CharField(
        "Kód pozice",
        max_length=50,
        unique=True,
        help_text="Krátký kód (např. PPM_KUCHAR, PPM_MANAZER_PROVOZU apod.)",
    )

    class Meta:
        verbose_name = "Pozice"
        verbose_name_plural = "Pozice"
        ordering = ["nazev"]

    def __str__(self):
        return self.nazev


class OsobniDotaznik(models.Model):
    TYP_POMERU_CHOICES = [
        ("DOBA_NEURCITA", "Pracovní poměr na dobu neurčitou"),
        ("DOBA_URCITA", "Pracovní poměr na dobu určitou"),
    ]
    ROZVRZENI_CHOICES = [
        ("ROVNOMERNE", "Rovnoměrné rozvržení pracovní doby"),
        ("NEROVNOMERNE", "Nerovnoměrné rozvržení pracovní doby"),
    ]

    typ_pomeru = models.CharField(
        "Typ pracovního poměru",
        max_length=20,
        choices=TYP_POMERU_CHOICES,
        default="DOBA_NEURCITA",
    )
    pomer_do = models.DateField(
        "Pracovní poměr na dobu určitou do",
        null=True,
        blank=True,
    )
    nastup_datum = models.DateField(
        "Datum nástupu do práce",
        null=True,
        blank=True,
    )
    zkusebni_doba_mesice = models.PositiveSmallIntegerField(
        "Zkušební doba (v měsících)",
        null=True,
        blank=True,
        help_text="Max. 3 měsíce (6 u vedoucích pracovníků) podle ZP.",
    )
    tydenni_uvazek_hodin = models.DecimalField(
        "Týdenní pracovní doba v hodinách",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Např. 40, 38.75, 37.5",
    )
    rozvrzeni_pracovni_doby = models.CharField(
        "Rozvržení pracovní doby",
        max_length=20,
        choices=ROZVRZENI_CHOICES,
        default="ROVNOMERNE",
    )
    # vazby
    provoz = models.ForeignKey(
        Provoz,
        on_delete=models.PROTECT,
        related_name="dotazniky",
        verbose_name="Provoz",
    )
    vytvoril = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vytvorene_dotazniky",
        verbose_name="Vytvořil",
    )

    # osobní údaje
    titul = models.CharField("Titul", max_length=50, blank=True)
    jmeno = models.CharField("Jméno", max_length=100)
    prijmeni = models.CharField("Příjmení", max_length=100)
    rodne_prijmeni = models.CharField("Rodné a dřívější příjmení", max_length=200, blank=True)
    datum_narozeni = models.DateField("Datum narození")
    misto_narozeni = models.CharField("Místo narození", max_length=200)
    statni_obcanstvi = models.CharField("Státní občanství", max_length=100)
    rodinny_stav = models.CharField("Rodinný stav", max_length=100, blank=True)
    telefon = models.CharField("Telefon", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    rodne_cislo = models.CharField("Rodné číslo", max_length=20)
    zdravotni_pojistovna = models.CharField("Zdravotní pojišťovna", max_length=100)

    # bankovní spojení
    cislo_uctu = models.CharField("Číslo účtu", max_length=50, blank=True)
    kod_banky = models.CharField("Kód banky", max_length=10, blank=True)
    nazev_banky = models.CharField("Název banky/spořitelny", max_length=200, blank=True)

    # adresy
    trv_ulice = models.CharField("Trvalé bydliště – ulice", max_length=200)
    trv_cislo = models.CharField("Trvalé bydliště – číslo", max_length=50)
    trv_mesto = models.CharField("Trvalé bydliště – město", max_length=200)
    trv_psc = models.CharField("Trvalé bydliště – PSČ", max_length=20)

    dor_ulice = models.CharField("Doručovací adresa – ulice", max_length=200, blank=True)
    dor_cislo = models.CharField("Doručovací adresa – číslo", max_length=50, blank=True)
    dor_mesto = models.CharField("Doručovací adresa – město", max_length=200, blank=True)
    dor_psc = models.CharField("Doručovací adresa – PSČ", max_length=20, blank=True)

    # důchody (checkboxy)
    duchod_predcasny = models.BooleanField("Předčasný důchod", default=False)
    duchod_starobni = models.BooleanField("Starobní důchod", default=False)
    duchod_invalidni = models.BooleanField("Invalidní důchod", default=False)
    duchod_datum_vzniku = models.DateField(
        "Datum vzniku nároku na důchod", null=True, blank=True
    )
    duchod_kdo_vyplaci = models.CharField(
        "Kdo důchod vyplácí", max_length=200, blank=True
    )

    # vzdělání – checkboxy
    vzdelani_zakladni = models.BooleanField("Základní škola", default=False)
    vzdelani_sou = models.BooleanField("Střední odborné učiliště", default=False)
    vzdelani_sou_rok_ukonceni = models.CharField(
        "SOÚ – rok ukončení", max_length=10, blank=True
    )
    vzdelani_ss = models.BooleanField("Střední škola", default=False)
    vzdelani_ss_mesto = models.CharField(
        "Střední škola – město/obec", max_length=100, blank=True
    )
    vzdelani_gymnazium = models.BooleanField("Gymnázium", default=False)
    vzdelani_gymnazium_skola = models.CharField(
        "Gymnázium – škola (název)", max_length=150, blank=True
    )
    vzdelani_vs = models.BooleanField("Vysoká škola", default=False)
    vzdelani_vs_obor = models.CharField(
        "Vysoká škola – obor", max_length=150, blank=True
    )

    vzdelani_zakončeno_vyucni_list = models.BooleanField(
        "Zakončeno – výuční list", default=False
    )
    vzdelani_zakončeno_maturita = models.BooleanField(
        "Zakončeno – maturitní vysvědčení", default=False
    )
    vzdelani_zakončeno_diplom = models.BooleanField(
        "Zakončeno – diplom", default=False
    )

    # poslední zaměstnavatel
    posledni_zamestnavatel_nazev = models.CharField(
        "Poslední zaměstnavatel – název firmy", max_length=200, blank=True
    )
    posledni_zamestnavatel_pozice = models.CharField(
        "Poslední zaměstnavatel – pracovní zařazení", max_length=200, blank=True
    )
    posledni_zamestnavatel_od = models.DateField(
        "Poslední zaměstnavatel – od", null=True, blank=True
    )
    posledni_zamestnavatel_do = models.DateField(
        "Poslední zaměstnavatel – do", null=True, blank=True
    )

    # TODO: doplnit sekci cizinec, srážky, atd. podle původního modelu

    # pozice (výběr na konci)
    pozice = models.ForeignKey(
        Pozice,
        on_delete=models.PROTECT,
        related_name="dotazniky",
        verbose_name="Pozice",
    )

    datum_vytvoreni = models.DateTimeField(auto_now_add=True)
    datum_aktualizace = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Osobní dotazník"
        verbose_name_plural = "Osobní dotazníky"
        ordering = ["-datum_vytvoreni"]

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni} – {self.provoz}"
