"""
URL configuration for auth_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Versioning
    path('api/v1/auth/', include('accounts.urls')),  # Version 1 of the auth API

    # OpenAPI Schema and Documentation
    path("doc", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(), name="swagger"),
    path("doc/redoc", SpectacularRedocView.as_view(), name="redoc"),
]


# superuser: j.akpa@yahoo.com
# password: 123456
# {
#   "username": "Kingteddy",
#   "email": "jakpaetuk@gmail.com",
#   "password": "Holycraft@30",
#   "first_name": "Jon",
#   "last_name": "Doe"
# }