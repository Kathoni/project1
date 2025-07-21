from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Transaction, Budget, SavingsGoal,
    JobOpportunity, UserJobApplication, AIConversation
)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_staff')
    list_filter = UserAdmin.list_filter + ('userprofile__user_type',)
    
    def get_user_type(self, obj):
        try:
            return obj.userprofile.get_user_type_display()
        except UserProfile.DoesNotExist:
            return "No Profile"
    get_user_type.short_description = 'User Type'

admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'monthly_income', 'currency', 'preferred_savings_percentage', 'created_at')
    list_filter = ('user_type', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'date_of_birth')
        }),
        ('Financial Information', {
            'fields': ('monthly_income', 'currency', 'preferred_savings_percentage', 'financial_goals')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'color', 'is_default', 'created_at')
    list_filter = ('category_type', 'is_default', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('category_type', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category_type', 'description')
        }),
        ('Display', {
            'fields': ('color', 'icon', 'is_default')
        })
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'amount', 'transaction_type', 'category', 'date', 'created_at')
    list_filter = ('transaction_type', 'category', 'date', 'is_recurring', 'created_at')
    search_fields = ('user__username', 'description', 'notes', 'location')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'amount', 'transaction_type', 'category', 'description', 'date')
        }),
        ('Additional Information', {
            'fields': ('location', 'notes', 'receipt_image')
        }),
        ('Recurring Settings', {
            'fields': ('is_recurring', 'recurring_frequency'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('transaction_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'period', 'start_date', 'end_date', 'is_active', 'get_usage_percentage')
    list_filter = ('period', 'is_active', 'category', 'start_date')
    search_fields = ('user__username', 'category__name')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at', 'get_spent_amount', 'get_remaining_amount', 'get_usage_percentage')
    
    fieldsets = (
        ('Budget Information', {
            'fields': ('user', 'category', 'amount', 'period')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Alerts', {
            'fields': ('alert_threshold',)
        }),
        ('Budget Status', {
            'fields': ('get_spent_amount', 'get_remaining_amount', 'get_usage_percentage'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_usage_percentage(self, obj):
        return f"{obj.get_usage_percentage()}%"
    get_usage_percentage.short_description = 'Usage %'

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_amount', 'current_amount', 'target_date', 'status', 'priority', 'get_progress_percentage')
    list_filter = ('status', 'priority', 'target_date', 'created_at')
    search_fields = ('user__username', 'name', 'description')
    date_hierarchy = 'target_date'
    ordering = ('-priority', 'target_date')
    readonly_fields = ('created_at', 'updated_at', 'get_progress_percentage', 'get_monthly_target')
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'name', 'description', 'priority')
        }),
        ('Financial Targets', {
            'fields': ('target_amount', 'current_amount', 'target_date')
        }),
        ('Status', {
            'fields': ('status', 'get_progress_percentage', 'get_monthly_target'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_progress_percentage(self, obj):
        return f"{obj.get_progress_percentage()}%"
    get_progress_percentage.short_description = 'Progress %'

@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'experience_level', 'is_remote', 'is_student_friendly', 'posted_date')
    list_filter = ('employment_type', 'experience_level', 'is_remote', 'is_student_friendly', 'posted_date', 'created_at')
    search_fields = ('title', 'company', 'description', 'skills_required')
    date_hierarchy = 'posted_date'
    ordering = ('-posted_date',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'company', 'description', 'requirements')
        }),
        ('Location & Type', {
            'fields': ('location', 'is_remote', 'employment_type', 'experience_level')
        }),
        ('Compensation', {
            'fields': ('salary_min', 'salary_max', 'currency')
        }),
        ('Skills & Tags', {
            'fields': ('skills_required', 'is_student_friendly')
        }),
        ('Application', {
            'fields': ('application_url', 'posted_date', 'application_deadline')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(UserJobApplication)
class UserJobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'job_company', 'status', 'applied_date', 'created_at')
    list_filter = ('status', 'applied_date', 'created_at')
    search_fields = ('user__username', 'job__title', 'job__company', 'notes')
    date_hierarchy = 'applied_date'
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def job_title(self, obj):
        return obj.job.title
    job_title.short_description = 'Job Title'
    
    def job_company(self, obj):
        return obj.job.company
    job_company.short_description = 'Company'
    
    fieldsets = (
        ('Application Information', {
            'fields': ('user', 'job', 'status', 'applied_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversation_type', 'truncated_message', 'created_at')
    list_filter = ('conversation_type', 'created_at')
    search_fields = ('user__username', 'user_message', 'ai_response')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('conversation_id', 'created_at')
    
    def truncated_message(self, obj):
        return obj.user_message[:50] + "..." if len(obj.user_message) > 50 else obj.user_message
    truncated_message.short_description = 'User Message'
    
    fieldsets = (
        ('Conversation Details', {
            'fields': ('user', 'conversation_type', 'conversation_id')
        }),
        ('Messages', {
            'fields': ('user_message', 'ai_response')
        }),
        ('Context Data', {
            'fields': ('context_data',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Customize admin site
admin.site.site_header = "FinanceAI Administration"
admin.site.site_title = "FinanceAI Admin"
admin.site.index_title = "Welcome to FinanceAI Administration"
