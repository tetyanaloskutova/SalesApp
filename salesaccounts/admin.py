from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class SalesLeadHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["CRM_id", "history"]
    history_list_display = ["sales_narrative"]
    search_fields = ['CRM_id', 'user__username']
	
admin.site.register(Account, SimpleHistoryAdmin)
admin.site.register(CREmployee, SimpleHistoryAdmin)
admin.site.register(ServiceType, SimpleHistoryAdmin)

admin.site.register(SalesLead, SalesLeadHistoryAdmin)

