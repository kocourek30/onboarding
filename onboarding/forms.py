from django import forms
from .models import OsobniDotaznik

class OsobniDotaznikForm(forms.ModelForm):
    class Meta:
        model = OsobniDotaznik
        exclude = ("vytvoril",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            profil = getattr(user, "profil", None)
            if profil and profil.role != profil.ROLE_HR:
                self.fields["provoz"].queryset = profil.provozy.all()
