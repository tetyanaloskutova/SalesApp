"""SalesAppProj URL Configuration

salesaccounts application is available at salesaccounts/ url
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
	path('salesaccounts/', include('salesaccounts.urls')),
]
