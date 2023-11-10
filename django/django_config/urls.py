from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userauth.urls')),  # Include URLs of userauth app
    path('', include('phase_two.urls')),  # Include URLs of phase_two app
]
