from django.urls import path, include
from rest_framework.routers import DefaultRouter



from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),  # include all app URLs
]
