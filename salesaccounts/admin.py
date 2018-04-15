from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class SalesLeadHistoryAdmin(SimpleHistoryAdmin):
	list_display = ["owner", "account", "Probability", "description", "next_action", "next_action_date"]
	history_list_display = [ "next_action", "next_action_date", "user"]
	search_fields = ['CRM_id', "owner", "account", 'est_decision_date', "Probability", "description", "next_action"]
	list_filter = ['owner', 'est_decision_date', 'status', "next_action_date"]
	ordering = ('-owner',)
	readonly_fields = ('user_account',)
	
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

		
admin.site.register(Account, AccountAdmin)
admin.site.register(CREmployee, CREmployeeAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)

admin.site.register(SalesLead, SalesLeadHistoryAdmin)
admin.site.register(AccountGroup, AccountGroupAdmin)

