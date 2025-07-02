from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from finance.models import Transcation, Goal

# Resource class for Transcation
class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transcation
        fields = ('date', 'title', 'amount', 'transaction_type')

# Admin class with import-export functionality
@admin.register(Transcation)
class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    list_display = ('date', 'title', 'amount', 'transaction_type')
    search_fields = ('title',)

# Normal admin registration for Goal
@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'current_amount', 'deadline')
    search_fields = ('name',)
