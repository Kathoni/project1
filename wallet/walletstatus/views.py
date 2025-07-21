from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q, Count
from django.conf import settings
from datetime import datetime, date, timedelta
import json
import openai
import requests
from decimal import Decimal
from django.core.paginator import Paginator

from .models import (
    UserProfile, Transaction, Category, Budget, SavingsGoal, 
    JobOpportunity, UserJobApplication, AIConversation
)

# Initialize OpenAI
openai.api_key = settings.OPENAI_API_KEY

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    """Enhanced dashboard with financial overview"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Financial overview calculations
    current_month = date.today().replace(day=1)
    next_month = (current_month + timedelta(days=32)).replace(day=1)
    
    # Monthly income and expenses
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__gte=current_month,
        date__lt=next_month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    monthly_expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=current_month,
        date__lt=next_month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Recent transactions
    recent_transactions = Transaction.objects.filter(user=request.user)[:10]
    
    # Active budgets with usage
    active_budgets = Budget.objects.filter(
        user=request.user, 
        is_active=True,
        start_date__lte=date.today(),
        end_date__gte=date.today()
    )
    
    # Savings goals
    savings_goals = SavingsGoal.objects.filter(user=request.user, status='active')
    
    # Job recommendations for students
    job_recommendations = []
    if user_profile.user_type == 'student':
        job_recommendations = JobOpportunity.objects.filter(
            Q(is_student_friendly=True) | Q(experience_level='entry'),
            is_remote=True
        )[:5]
    
    context = {
        'user_profile': user_profile,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'net_income': monthly_income - monthly_expenses,
        'recent_transactions': recent_transactions,
        'active_budgets': active_budgets,
        'savings_goals': savings_goals,
        'job_recommendations': job_recommendations,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def profile_setup(request):
    """User profile setup/edit"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.user_type = request.POST.get('user_type', 'other')
        profile.monthly_income = request.POST.get('monthly_income', 0)
        profile.currency = request.POST.get('currency', 'USD')
        profile.preferred_savings_percentage = int(request.POST.get('preferred_savings_percentage', 20))
        profile.financial_goals = request.POST.get('financial_goals', '')
        
        if request.POST.get('date_of_birth'):
            profile.date_of_birth = request.POST.get('date_of_birth')
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
    
    return render(request, 'profile_setup.html', {'profile': profile})

@login_required
def add_transaction(request):
    """Add new transaction"""
    categories = Category.objects.all().order_by('category_type', 'name')
    
    if request.method == 'POST':
        transaction = Transaction(
            user=request.user,
            amount=Decimal(request.POST.get('amount')),
            transaction_type=request.POST.get('transaction_type'),
            description=request.POST.get('description'),
            date=request.POST.get('date'),
            location=request.POST.get('location', ''),
            notes=request.POST.get('notes', ''),
        )
        
        category_id = request.POST.get('category')
        if category_id:
            transaction.category = Category.objects.get(id=category_id)
        
        transaction.save()
        messages.success(request, 'Transaction added successfully!')
        return redirect('transactions')
    
    return render(request, 'add_transaction.html', {'categories': categories})

@login_required
def transactions(request):
    """View all transactions with filtering"""
    transaction_list = Transaction.objects.filter(user=request.user)
    
    # Apply filters
    transaction_type = request.GET.get('type')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if transaction_type:
        transaction_list = transaction_list.filter(transaction_type=transaction_type)
    if category_id:
        transaction_list = transaction_list.filter(category_id=category_id)
    if date_from:
        transaction_list = transaction_list.filter(date__gte=date_from)
    if date_to:
        transaction_list = transaction_list.filter(date__lte=date_to)
    
    # Pagination
    paginator = Paginator(transaction_list, 20)
    page_number = request.GET.get('page')
    transactions_page = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'transactions': transactions_page,
        'categories': categories,
        'filters': {
            'type': transaction_type,
            'category': category_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    
    return render(request, 'transactions.html', context)

@login_required
def budgets(request):
    """Budget management"""
    user_budgets = Budget.objects.filter(user=request.user)
    categories = Category.objects.filter(category_type='expense')
    
    if request.method == 'POST':
        budget = Budget(
            user=request.user,
            category=Category.objects.get(id=request.POST.get('category')),
            amount=Decimal(request.POST.get('amount')),
            period=request.POST.get('period'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        )
        budget.save()
        messages.success(request, 'Budget created successfully!')
        return redirect('budgets')
    
    return render(request, 'budgets.html', {
        'budgets': user_budgets,
        'categories': categories
    })

@login_required
def savings_goals(request):
    """Savings goals management"""
    goals = SavingsGoal.objects.filter(user=request.user)
    
    if request.method == 'POST':
        goal = SavingsGoal(
            user=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            target_amount=Decimal(request.POST.get('target_amount')),
            target_date=request.POST.get('target_date'),
            priority=int(request.POST.get('priority', 3)),
        )
        goal.save()
        messages.success(request, 'Savings goal created successfully!')
        return redirect('savings_goals')
    
    return render(request, 'savings_goals.html', {'goals': goals})

@login_required
def job_opportunities(request):
    """Job opportunities for students"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Base query for remote jobs
    jobs = JobOpportunity.objects.filter(is_remote=True)
    
    # Additional filters for students
    if user_profile.user_type == 'student':
        jobs = jobs.filter(
            Q(is_student_friendly=True) | 
            Q(experience_level__in=['entry', 'junior']) |
            Q(employment_type__in=['internship', 'part_time'])
        )
    
    # Apply search filters
    search_query = request.GET.get('search')
    employment_type = request.GET.get('employment_type')
    experience_level = request.GET.get('experience_level')
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(skills_required__icontains=search_query)
        )
    
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    
    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)
    
    # User applications
    user_applications = UserJobApplication.objects.filter(user=request.user)
    applied_job_ids = user_applications.values_list('job_id', flat=True)
    
    context = {
        'jobs': jobs_page,
        'applied_job_ids': list(applied_job_ids),
        'search_query': search_query,
        'employment_type': employment_type,
        'experience_level': experience_level,
        'is_student': user_profile.user_type == 'student',
    }
    
    return render(request, 'job_opportunities.html', context)

@login_required
@require_http_methods(["POST"])
def apply_to_job(request, job_id):
    """Apply to a job opportunity"""
    job = get_object_or_404(JobOpportunity, id=job_id)
    
    application, created = UserJobApplication.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={'status': 'interested'}
    )
    
    if created:
        messages.success(request, f'Added {job.title} to your applications!')
    else:
        messages.info(request, 'You have already applied to this job.')
    
    return redirect('job_opportunities')

@login_required
def my_applications(request):
    """View user's job applications"""
    applications = UserJobApplication.objects.filter(user=request.user)
    
    return render(request, 'my_applications.html', {'applications': applications})

@csrf_exempt
@login_required
def ai_financial_advisor(request):
    """AI-powered financial advisor using OpenAI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            conversation_type = data.get('type', 'general')
            
            # Gather user's financial context
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Get recent financial data for context
            recent_transactions = Transaction.objects.filter(user=request.user)[:10]
            active_budgets = Budget.objects.filter(user=request.user, is_active=True)
            savings_goals = SavingsGoal.objects.filter(user=request.user, status='active')
            
            # Prepare context for AI
            financial_context = {
                'user_type': user_profile.user_type,
                'monthly_income': float(user_profile.monthly_income),
                'currency': user_profile.currency,
                'savings_percentage': user_profile.preferred_savings_percentage,
                'recent_transactions_count': recent_transactions.count(),
                'active_budgets_count': active_budgets.count(),
                'savings_goals_count': savings_goals.count(),
            }
            
            # Create AI prompt
            system_prompt = f"""You are a helpful financial advisor AI. The user is a {user_profile.get_user_type_display()} 
            with a monthly income of {user_profile.monthly_income} {user_profile.currency}. 
            They prefer to save {user_profile.preferred_savings_percentage}% of their income.
            
            They have {recent_transactions.count()} recent transactions, {active_budgets.count()} active budgets, 
            and {savings_goals.count()} savings goals.
            
            Provide practical, personalized financial advice. Be concise but helpful. 
            If they're a student, also consider recommending ways to increase income through part-time work or skills development."""
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Save conversation
            conversation = AIConversation.objects.create(
                user=request.user,
                conversation_type=conversation_type,
                user_message=user_message,
                ai_response=ai_response,
                context_data=financial_context
            )
            
            return JsonResponse({
                'success': True,
                'response': ai_response,
                'conversation_id': str(conversation.conversation_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error getting AI response: {str(e)}'
            })
    
    # GET request - show AI chat interface
    recent_conversations = AIConversation.objects.filter(user=request.user)[:10]
    return render(request, 'ai_advisor.html', {'recent_conversations': recent_conversations})

@login_required
def analytics(request):
    """Financial analytics and insights"""
    user = request.user
    
    # Monthly spending by category
    current_month = date.today().replace(day=1)
    next_month = (current_month + timedelta(days=32)).replace(day=1)
    
    monthly_expenses_by_category = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__gte=current_month,
        date__lt=next_month
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Income vs Expenses over time (last 6 months)
    six_months_ago = current_month - timedelta(days=180)
    
    monthly_data = []
    current_date = six_months_ago
    while current_date < current_month:
        next_date = (current_date + timedelta(days=32)).replace(day=1)
        
        income = Transaction.objects.filter(
            user=user,
            transaction_type='income',
            date__gte=current_date,
            date__lt=next_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            date__gte=current_date,
            date__lt=next_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_data.append({
            'month': current_date.strftime('%Y-%m'),
            'income': float(income),
            'expenses': float(expenses),
            'net': float(income - expenses)
        })
        
        current_date = next_date
    
    context = {
        'monthly_expenses_by_category': monthly_expenses_by_category,
        'monthly_data': json.dumps(monthly_data),
    }
    
    return render(request, 'analytics.html', context)

def fetch_remote_jobs():
    """Background task to fetch remote jobs from job APIs"""
    # This would typically be called by a background task runner like Celery
    # For demonstration, this shows how to integrate with job APIs
    
    try:
        # Example using a hypothetical job API
        # You would replace this with actual job board APIs like:
        # - RemoteOK API
        # - Adzuna API
        # - Indeed API
        # - GitHub Jobs (deprecated but showing concept)
        
        # Simulated API call - replace with real implementation
        mock_jobs = [
            {
                'title': 'Junior Frontend Developer',
                'company': 'TechCorp Remote',
                'description': 'Looking for a junior frontend developer with React experience',
                'requirements': 'React, JavaScript, HTML, CSS',
                'location': 'Remote',
                'employment_type': 'full_time',
                'experience_level': 'junior',
                'skills_required': 'React, JavaScript, HTML, CSS, Git',
                'application_url': 'https://example.com/apply/1',
                'posted_date': date.today(),
                'is_student_friendly': True,
                'salary_min': 40000,
                'salary_max': 60000,
            },
            # Add more mock jobs as needed
        ]
        
        for job_data in mock_jobs:
            job, created = JobOpportunity.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults={
                    'description': job_data['description'],
                    'requirements': job_data['requirements'],
                    'location': job_data['location'],
                    'is_remote': True,
                    'employment_type': job_data['employment_type'],
                    'experience_level': job_data['experience_level'],
                    'skills_required': job_data['skills_required'],
                    'application_url': job_data['application_url'],
                    'posted_date': job_data['posted_date'],
                    'is_student_friendly': job_data['is_student_friendly'],
                    'salary_min': job_data.get('salary_min'),
                    'salary_max': job_data.get('salary_max'),
                }
            )
        
        return True
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return False