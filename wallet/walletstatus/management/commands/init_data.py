from django.core.management.base import BaseCommand
from django.db import transaction
from walletstatus.models import Category, JobOpportunity
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Initialize default categories and sample data for FinanceAI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sample-jobs',
            action='store_true',
            help='Add sample job opportunities',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            self.create_default_categories()
            if options['sample_jobs']:
                self.create_sample_jobs()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized FinanceAI data!')
        )

    def create_default_categories(self):
        """Create default income and expense categories"""
        
        # Income categories
        income_categories = [
            {'name': 'Salary', 'description': 'Regular employment income', 'color': '#10b981', 'icon': 'fas fa-briefcase'},
            {'name': 'Freelance', 'description': 'Freelance and contract work', 'color': '#6366f1', 'icon': 'fas fa-laptop'},
            {'name': 'Investment', 'description': 'Investment returns and dividends', 'color': '#8b5cf6', 'icon': 'fas fa-chart-line'},
            {'name': 'Side Hustle', 'description': 'Additional income sources', 'color': '#f59e0b', 'icon': 'fas fa-coins'},
            {'name': 'Gifts', 'description': 'Money gifts and bonuses', 'color': '#ec4899', 'icon': 'fas fa-gift'},
            {'name': 'Other Income', 'description': 'Miscellaneous income', 'color': '#6b7280', 'icon': 'fas fa-plus'},
        ]

        # Expense categories
        expense_categories = [
            {'name': 'Housing', 'description': 'Rent, mortgage, utilities', 'color': '#ef4444', 'icon': 'fas fa-home'},
            {'name': 'Food & Dining', 'description': 'Groceries and restaurant meals', 'color': '#f97316', 'icon': 'fas fa-utensils'},
            {'name': 'Transportation', 'description': 'Car, gas, public transport', 'color': '#eab308', 'icon': 'fas fa-car'},
            {'name': 'Entertainment', 'description': 'Movies, games, subscriptions', 'color': '#22c55e', 'icon': 'fas fa-gamepad'},
            {'name': 'Healthcare', 'description': 'Medical expenses and insurance', 'color': '#06b6d4', 'icon': 'fas fa-heartbeat'},
            {'name': 'Education', 'description': 'Tuition, books, courses', 'color': '#3b82f6', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Shopping', 'description': 'Clothing and personal items', 'color': '#8b5cf6', 'icon': 'fas fa-shopping-bag'},
            {'name': 'Bills & Utilities', 'description': 'Phone, internet, electricity', 'color': '#ec4899', 'icon': 'fas fa-file-invoice'},
            {'name': 'Travel', 'description': 'Vacation and travel expenses', 'color': '#14b8a6', 'icon': 'fas fa-plane'},
            {'name': 'Personal Care', 'description': 'Haircuts, gym, beauty', 'color': '#f43f5e', 'icon': 'fas fa-spa'},
            {'name': 'Savings', 'description': 'Money put into savings', 'color': '#10b981', 'icon': 'fas fa-piggy-bank'},
            {'name': 'Other Expenses', 'description': 'Miscellaneous expenses', 'color': '#6b7280', 'icon': 'fas fa-minus'},
        ]

        # Create income categories
        for cat_data in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                category_type='income',
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color'],
                    'icon': cat_data['icon'],
                    'is_default': True
                }
            )
            if created:
                self.stdout.write(f'Created income category: {category.name}')

        # Create expense categories
        for cat_data in expense_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                category_type='expense',
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color'],
                    'icon': cat_data['icon'],
                    'is_default': True
                }
            )
            if created:
                self.stdout.write(f'Created expense category: {category.name}')

    def create_sample_jobs(self):
        """Create sample job opportunities"""
        
        sample_jobs = [
            {
                'title': 'Junior Frontend Developer',
                'company': 'TechStart Remote',
                'description': 'We are looking for a passionate junior frontend developer to join our remote team. You will work on exciting projects using React, TypeScript, and modern web technologies.',
                'requirements': 'Basic knowledge of HTML, CSS, JavaScript, and React. Willingness to learn and grow. Good communication skills for remote work.',
                'location': 'Remote',
                'employment_type': 'full_time',
                'experience_level': 'junior',
                'salary_min': 45000,
                'salary_max': 65000,
                'skills_required': 'React, JavaScript, HTML, CSS, Git, TypeScript',
                'application_url': 'https://example.com/apply/frontend-dev',
                'posted_date': date.today(),
                'is_student_friendly': True,
            },
            {
                'title': 'Part-time Content Writer',
                'company': 'Digital Marketing Co',
                'description': 'Create engaging content for blogs, social media, and marketing materials. Perfect for students looking to gain experience in digital marketing.',
                'requirements': 'Excellent writing skills, creativity, basic understanding of SEO. Portfolio of writing samples preferred.',
                'location': 'Remote',
                'employment_type': 'part_time',
                'experience_level': 'entry',
                'salary_min': 15,
                'salary_max': 25,
                'skills_required': 'Writing, SEO, Social Media, Content Marketing',
                'application_url': 'https://example.com/apply/content-writer',
                'posted_date': date.today() - timedelta(days=2),
                'is_student_friendly': True,
            },
            {
                'title': 'Remote Data Entry Specialist',
                'company': 'DataCorp Solutions',
                'description': 'Remote data entry position with flexible hours. Perfect for students or anyone looking for supplemental income.',
                'requirements': 'Attention to detail, basic computer skills, ability to work independently. No prior experience required.',
                'location': 'Remote',
                'employment_type': 'part_time',
                'experience_level': 'entry',
                'salary_min': 12,
                'salary_max': 18,
                'skills_required': 'Data Entry, Microsoft Excel, Attention to Detail',
                'application_url': 'https://example.com/apply/data-entry',
                'posted_date': date.today() - timedelta(days=1),
                'is_student_friendly': True,
            },
            {
                'title': 'Virtual Assistant Internship',
                'company': 'StartupHub',
                'description': 'Gain valuable experience as a virtual assistant supporting our growing startup. Learn about business operations, project management, and more.',
                'requirements': 'Strong organizational skills, proficiency in Google Workspace, excellent communication skills, eager to learn.',
                'location': 'Remote',
                'employment_type': 'internship',
                'experience_level': 'entry',
                'salary_min': 800,
                'salary_max': 1200,
                'skills_required': 'Organization, Google Workspace, Communication, Project Management',
                'application_url': 'https://example.com/apply/va-internship',
                'posted_date': date.today() - timedelta(days=3),
                'is_student_friendly': True,
            },
            {
                'title': 'Remote Graphic Design Freelancer',
                'company': 'Creative Agency Remote',
                'description': 'Join our team of creative freelancers working on diverse projects. Create designs for websites, social media, and marketing materials.',
                'requirements': 'Proficiency in Adobe Creative Suite, strong portfolio, creativity, ability to meet deadlines.',
                'location': 'Remote',
                'employment_type': 'freelance',
                'experience_level': 'junior',
                'salary_min': 20,
                'salary_max': 40,
                'skills_required': 'Adobe Photoshop, Adobe Illustrator, Graphic Design, Creativity',
                'application_url': 'https://example.com/apply/graphic-designer',
                'posted_date': date.today() - timedelta(days=5),
                'is_student_friendly': True,
            },
        ]

        for job_data in sample_jobs:
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
                    'salary_min': job_data['salary_min'],
                    'salary_max': job_data['salary_max'],
                    'skills_required': job_data['skills_required'],
                    'application_url': job_data['application_url'],
                    'posted_date': job_data['posted_date'],
                    'is_student_friendly': job_data['is_student_friendly'],
                }
            )
            if created:
                self.stdout.write(f'Created job: {job.title} at {job.company}')