from django.contrib import admin
from .models import *

admin.site.register(Account)

admin.site.register(SalesLead)

admin.site.register(CREmployee)
admin.site.register(ServiceType)