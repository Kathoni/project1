from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile management
    path('profile/', views.profile_setup, name='profile_setup'),
    
    # Transaction management
    path('transactions/', views.transactions, name='transactions'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    
    # Budget management
    path('budgets/', views.budgets, name='budgets'),
    
    # Savings goals
    path('savings-goals/', views.savings_goals, name='savings_goals'),
    
    # Job opportunities (for students)
    path('jobs/', views.job_opportunities, name='job_opportunities'),
    path('jobs/apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    
    # AI Financial Advisor
    path('ai-advisor/', views.ai_financial_advisor, name='ai_advisor'),
    
    # Analytics and reports
    path('analytics/', views.analytics, name='analytics'),
]