from django.contrib import admin
from django.urls import path, include
from home.views import index

urlpatterns = [

    path("", index, name=""),

    path("accounts/", include("accounts.urls")),
    path("core/", include("core.urls")),

    path('admin/', admin.site.urls),
]
