from django.contrib import admin
from django.urls import path

from persistence.health_views import health_view

urlpatterns = [
    path("health/", health_view, name="health"),
    path("admin/", admin.site.urls),
]
