from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from provozy.models import Provoz
from onboarding.models import OsobniDotaznik
from onboarding.forms import OsobniDotaznikForm


# portal/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from provozy.models import Provoz
from onboarding.models import OsobniDotaznik
from onboarding.forms import OsobniDotaznikForm


class MojeProvozyView(LoginRequiredMixin, ListView):
    model = Provoz
    template_name = "portal/moje_provozy.html"
    context_object_name = "provozy"

    def get_queryset(self):
        user = self.request.user
        # superuser + HR vidí všechny provozy
        if user.is_superuser or getattr(user, "role", None) == user.HR:
            return Provoz.objects.all()
        # ostatní jen provozy, které mají v M2M
        return Provoz.objects.filter(uzivatele=user).distinct()



class OsobniDotaznikCreateView(LoginRequiredMixin, CreateView):
    model = OsobniDotaznik
    form_class = OsobniDotaznikForm
    template_name = "portal/dotaznik_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.vytvoril = self.request.user
        return super().form_valid(form)
    

