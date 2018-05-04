"""SalesAppProj URL Configuration

salesaccounts application is available at salesaccounts/ url
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.urls import reverse

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', admin.site.urls),
	path('salesaccounts/', include('salesaccounts.urls')),
]

def index(request):
    return HttpResponseRedirect(reverse('admin:view_on_site', args=("salesaccounts_saleslead",)))

