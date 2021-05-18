from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [path("", views.get_program_input)] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
