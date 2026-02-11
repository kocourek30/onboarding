from django import forms
from .models import OsobniDotaznik


class OsobniDotaznikForm(forms.ModelForm):
    dorucovaci_odlisna = forms.BooleanField(
        label="Adresa pro doručování (liší se od trvalého bydliště)",
        required=False,
    )

    class Meta:
        model = OsobniDotaznik
        exclude = ("vytvoril",)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # textová / číselná pole
        text_like = [
            "titul", "jmeno", "prijmeni", "rodne_prijmeni",
            "misto_narozeni", "telefon", "email", "rodne_cislo",
            "zdravotni_pojistovna",
            "cislo_uctu", "kod_banky", "nazev_banky",
            "trv_ulice", "trv_cislo", "trv_psc", "trv_mesto",
            "dor_ulice", "dor_cislo", "dor_psc", "dor_mesto",
            "duchod_kdo_vyplaci",
            "vzdelani_sou_rok_ukonceni", "vzdelani_ss_mesto",
            "vzdelani_gymnazium_skola", "vzdelani_vs_obor",
            "posledni_zamestnavatel_nazev", "posledni_zamestnavatel_pozice",
            # nová pole – číselná / textová
            "zkusebni_doba_mesice",
            "tydenni_uvazek_hodin",
        ]
        for name in text_like:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-control")

        # datová pole
        for name in [
            "datum_narozeni",
            "duchod_datum_vzniku",
            "posledni_zamestnavatel_od",
            "posledni_zamestnavatel_do",
            # nová datová pole
            "nastup_datum",
            "pomer_do",
        ]:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-control")
                self.fields[name].widget.attrs.setdefault("type", "date")

        # selecty
        for name in [
            "statni_obcanstvi",
            "rodinny_stav",
            "provoz",
            "pozice",
            # nová select pole
            "typ_pomeru",
            "rozvrzeni_pracovni_doby",
        ]:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-select")

        # checkboxy
        checkbox_fields = [
            "dorucovaci_odlisna",
            "duchod_predcasny", "duchod_starobni", "duchod_invalidni",
            "vzdelani_zakladni", "vzdelani_sou", "vzdelani_ss",
            "vzdelani_gymnazium", "vzdelani_vs",
            "vzdelani_zakončeno_vyucni_list",
            "vzdelani_zakončeno_maturita",
            "vzdelani_zakončeno_diplom",
        ]
        for name in checkbox_fields:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-check-input")

        # omezení provozu podle uživatele
        if user and not (user.is_superuser or getattr(user, "role", None) == user.HR):
            if "provoz" in self.fields:
                self.fields["provoz"].queryset = user.provozy.all()


class OsobniUdajeForm(forms.ModelForm):
    class Meta:
        model = OsobniDotaznik
        fields = [
            "titul",
            "jmeno",
            "prijmeni",
            "rodne_prijmeni",
            "datum_narozeni",
            "misto_narozeni",
            "statni_obcanstvi",
            "rodinny_stav",
            "telefon",
            "email",
            "rodne_cislo",
            "zdravotni_pojistovna",
        ]


class AdresyABankaForm(forms.ModelForm):
    class Meta:
        model = OsobniDotaznik
        fields = [
            "cislo_uctu",
            "kod_banky",
            "nazev_banky",
            "trv_ulice",
            "trv_cislo",
            "trv_mesto",
            "trv_psc",
            "dor_ulice",
            "dor_cislo",
            "dor_mesto",
            "dor_psc",
        ]


class DuchodVzdelaniForm(forms.ModelForm):
    class Meta:
        model = OsobniDotaznik
        fields = [
            # důchody
            "duchod_predcasny",
            "duchod_starobni",
            "duchod_invalidni",
            "duchod_datum_vzniku",
            "duchod_kdo_vyplaci",
            # vzdělání
            "vzdelani_zakladni",
            "vzdelani_sou",
            "vzdelani_sou_rok_ukonceni",
            "vzdelani_ss",
            "vzdelani_ss_mesto",
            "vzdelani_gymnazium",
            "vzdelani_gymnazium_skola",
            "vzdelani_vs",
            "vzdelani_vs_obor",
            "vzdelani_zakončeno_vyucni_list",
            "vzdelani_zakončeno_maturita",
            "vzdelani_zakončeno_diplom",
        ]


class ZamestnavatelPoziceForm(forms.ModelForm):
    class Meta:
        model = OsobniDotaznik
        fields = [
            "posledni_zamestnavatel_nazev",
            "posledni_zamestnavatel_pozice",
            "posledni_zamestnavatel_od",
            "posledni_zamestnavatel_do",
            "provoz",
            "pozice",
            # nová pole pro pracovní poměr
            "typ_pomeru",
            "pomer_do",
            "nastup_datum",
            "zkusebni_doba_mesice",
            "tydenni_uvazek_hodin",
            "rozvrzeni_pracovni_doby",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # omezení provozu podle uživatele
        if user and not (user.is_superuser or getattr(user, "role", None) == user.HR):
            if "provoz" in self.fields:
                self.fields["provoz"].queryset = user.provozy.all()
