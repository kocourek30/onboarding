from django.urls import path, include
from .views import MojeProvozyView, OsobniDotaznikCreateView

app_name = "portal"

urlpatterns = [
    path("provozy/", MojeProvozyView.as_view(), name="moje_provozy"),
    path("onboarding/", include("onboarding.urls")),
    path("provozy/<int:pk>/dotaznik-novy/", OsobniDotaznikCreateView.as_view(), name="dotaznik_novy"),
]
