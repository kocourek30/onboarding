from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("onboarding/", include("onboarding.urls")),
    path("portal/", include("portal.urls")),
    

]
