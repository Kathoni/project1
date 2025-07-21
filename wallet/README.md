# FinanceAI - Intelligent Financial Management Tool

A comprehensive financial management application integrated with AI-powered advice and job recommendations for students. Built with Django and OpenAI GPT.

## Features

### 🧠 AI-Powered Financial Advisor
- Real-time financial advice using OpenAI GPT
- Personalized recommendations based on your financial profile
- Context-aware responses considering your income, expenses, and goals
- Chat interface with conversation history

### 💰 Financial Management
- **Transaction Tracking**: Record income and expenses with categories
- **Budget Management**: Set and monitor budgets with usage alerts
- **Savings Goals**: Track progress toward financial objectives
- **Analytics Dashboard**: Visual insights into spending patterns
- **Multi-currency Support**: Handle different currencies

### 👨‍🎓 Student Features
- **Remote Job Opportunities**: Curated list of student-friendly remote jobs
- **Job Application Tracking**: Manage your job applications
- **Student-specific Financial Advice**: Tailored recommendations for students
- **Part-time & Internship Focus**: Filtered job listings for students

### 📊 Analytics & Insights
- Monthly spending breakdown by category
- Income vs expenses trends
- Budget usage visualization
- Savings progress tracking
- Financial goal monitoring

## Technology Stack

- **Backend**: Django 5.1.7, Python
- **Database**: SQLite (default), PostgreSQL/MySQL support
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd wallet
```

### 2. Create Virtual Environment
```bash
python -m venv financeai_env
source financeai_env/bin/activate  # On Windows: financeai_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Initialize default categories and sample data
python manage.py init_data --sample-jobs
```

### 6. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Getting Started

### 1. Create an Account
- Navigate to the registration page
- Create your user account
- Complete your profile setup (user type, income, etc.)

### 2. Set Up Your Profile
- Choose your user type (Student, Working Professional, etc.)
- Enter your monthly income and preferred savings percentage
- Set your financial goals

### 3. Start Managing Finances
- Add your first transaction
- Create budgets for different categories
- Set savings goals
- Use the AI advisor for financial guidance

### 4. For Students: Explore Job Opportunities
- Browse remote job listings
- Apply to student-friendly positions
- Track your applications

## User Types & Features

### Student
- Job recommendations and application tracking
- Student-friendly budgeting advice
- Part-time income management
- Educational expense tracking

### Working Professional
- Advanced budgeting and investment tracking
- Salary management and tax planning
- Retirement and long-term savings goals

### Freelancer
- Irregular income management
- Project-based expense tracking
- Tax preparation assistance

### Entrepreneur
- Business expense tracking
- Cash flow management
- Investment planning

## API Integration

### OpenAI Integration
The application uses OpenAI's GPT-3.5-turbo model for:
- Personalized financial advice
- Budget analysis and recommendations
- Savings strategy suggestions
- General financial queries

### Job Search APIs (Future Enhancement)
The application is structured to integrate with:
- Indeed API
- Adzuna API
- RemoteOK API
- GitHub Jobs (when available)

## Admin Interface

Access the Django admin at `/admin/` to:
- Manage user accounts and profiles
- Add/edit categories and job opportunities
- View transaction and conversation data
- Monitor application usage

## File Structure

```
wallet/
├── manage.py
├── requirements.txt
├── .env.example
├── wallet/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── walletstatus/
    ├── models.py          # Database models
    ├── views.py           # Application logic
    ├── urls.py            # URL routing
    ├── admin.py           # Admin configuration
    ├── templates/         # HTML templates
    ├── management/
    │   └── commands/
    │       └── init_data.py  # Data initialization
    └── migrations/        # Database migrations
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `DEBUG` | Debug mode (True/False) | No |
| `SECRET_KEY` | Django secret key | Yes |
| `DATABASE_URL` | Database connection string | No |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Security Notes

- Never commit your `.env` file or API keys
- Use environment variables for sensitive configuration
- Regularly update dependencies
- Enable HTTPS in production
- Set `DEBUG=False` in production

## Support

For questions or issues:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

### Version 2.0 (Planned)
- Real-time job API integration
- Mobile application
- Advanced analytics with machine learning
- Multi-user household management
- Investment portfolio tracking
- Cryptocurrency support

### Version 2.1 (Planned)
- Voice commands for transaction entry
- Receipt scanning with OCR
- Automated expense categorization
- Integration with banking APIs
- Social features for financial challenges

## Acknowledgments

- OpenAI for GPT API
- Django community for the excellent framework
- Bootstrap team for UI components
- Font Awesome for icons

---

**Made with ❤️ for better financial wellness**