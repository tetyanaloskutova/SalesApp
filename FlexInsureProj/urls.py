"""FlexInsureProj URL Configuration

Risktypes application is available at risktypes/ url
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
	path('risktypes/', include('risktypes.urls')),
]
