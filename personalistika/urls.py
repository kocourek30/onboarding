from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("onboarding/", include("onboarding.urls")),
    path("portal/", include("portal.urls")),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)