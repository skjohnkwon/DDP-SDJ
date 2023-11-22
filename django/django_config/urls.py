from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userauth.urls')),
    path('', include('phase_two.urls')),
    path('', include('phase_three.urls')),
]
