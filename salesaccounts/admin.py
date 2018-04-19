from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class SalesLeadHistoryAdmin(SimpleHistoryAdmin):
	list_display = ["account", "owner", "Probability", "next_action_description", "next_action_date"]
	#form only show open list_display = ["sales lead", "service group", "account",  "service_line_colleagues", "last action", "next_action_date", "probability"]
	history_list_display = [ "next_action_date", "next_action_description", "user_account"]
	search_fields = ['CRM_id']
	#list_filter = ['owner', 'est_decision_date', 'status', "next_action_date"]
	ordering = ('-owner',)
	readonly_fields = ('user_account','CRM_id','account', 'name', 'est_revenue_USD')
	
	fieldsets = (
		('Account info', {
			'fields': ('CRM_id',('account', 'name', 'est_revenue_USD'))
		}),
		('Service Line', {
			'fields': (('service_type', 'pm'))
		}),
		('Next Action', {
			'fields': ( "next_action_date", "next_action_description"),
		}),
	)
	
	def has_delete_permission(self, request, obj=None):
		return False
		
	def has_add_permission(self, request):
		return False
		
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

	
class AccountGroupAdmin(SimpleHistoryAdmin):	
	list_display = ('name',)
	readonly_fields = ('user_account',)
	history_list_display = ( "user_account",'name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

class AccountAdmin(SimpleHistoryAdmin):	
	list_display = ['account_group', 'name', 'sector', 'relationship_status', 'region', 'account_manager', 'date_created']
	readonly_fields = ('user_account',)
	history_list_display = ( "relationship_status",'account_manager')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

class CREmployeeAdmin(SimpleHistoryAdmin):	
	list_display = ['name', 'short_name']
	readonly_fields = ('user_account',)
	history_list_display = ( "name",'short_name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()
		
class ServiceTypeAdmin(SimpleHistoryAdmin):	
	list_display = ('service_type','service_name')
	readonly_fields = ('user_account',)
	history_list_display = ( "user_account",'service_name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

		
#admin.site.register(Account, AccountAdmin)
#admin.site.register(CREmployee, CREmployeeAdmin)
#admin.site.register(ServiceType, ServiceTypeAdmin)

admin.site.register(SalesLead, SalesLeadHistoryAdmin)
#admin.site.register(AccountGroup, AccountGroupAdmin)

