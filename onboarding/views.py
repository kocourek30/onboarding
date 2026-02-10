from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OsobniDotaznikForm
from .models import OsobniDotaznik

@login_required
def dotaznik_list(request):
    qs = OsobniDotaznik.objects.all()
    profil = getattr(request.user, "profil", None)
    if not request.user.is_superuser and profil:
        if profil.role != profil.ROLE_HR:
            qs = qs.filter(provoz__in=profil.provozy.all())
    return render(request, "onboarding/dotaznik_list.html", {"dotazniky": qs})

@login_required
def dotaznik_create(request):
    if request.method == "POST":
        form = OsobniDotaznikForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vytvoril = request.user
            obj.save()
            return redirect("dotaznik_list")
    else:
        form = OsobniDotaznikForm(user=request.user)
    return render(request, "onboarding/dotaznik_form.html", {"form": form})
