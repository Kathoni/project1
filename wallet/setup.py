#!/usr/bin/env python3
"""
FinanceAI Setup Script
Helps users quickly set up and initialize the FinanceAI application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print the FinanceAI banner"""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║              🤖 FinanceAI Setup              ║
    ║                                               ║
    ║        Intelligent Financial Management       ║
    ║              with AI Integration              ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        sys.exit(1)
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run(['pip', '--version'], capture_output=True, check=True)
        print("✅ pip is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: pip is not available. Please install pip first.")
        sys.exit(1)

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_example.exists():
        print("❌ Error: .env.example file not found")
        sys.exit(1)
    
    if not env_file.exists():
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your OpenAI API key!")
    else:
        print("✅ .env file already exists")

def run_migrations():
    """Run Django migrations"""
    print("\n🗄️  Setting up database...")
    try:
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Database migrations completed")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to run migrations")
        sys.exit(1)

def create_superuser():
    """Create Django superuser"""
    print("\n👤 Creating admin user...")
    try:
        # Check if superuser already exists
        result = subprocess.run([
            'python', 'manage.py', 'shell', '-c',
            'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())'
        ], capture_output=True, text=True)
        
        if 'True' in result.stdout:
            print("✅ Admin user already exists")
        else:
            print("Please create an admin user for the application:")
            subprocess.run(['python', 'manage.py', 'createsuperuser'])
            print("✅ Admin user created")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to create admin user")

def initialize_data():
    """Initialize default categories and sample data"""
    print("\n📊 Initializing default data...")
    try:
        subprocess.run(['python', 'manage.py', 'init_data', '--sample-jobs'], check=True)
        print("✅ Default categories and sample jobs created")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to initialize data")

def check_openai_key():
    """Check if OpenAI API key is configured"""
    print("\n🔑 Checking OpenAI configuration...")
    env_file = Path('.env')
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=your-openai-api-key-here' in content or 'OPENAI_API_KEY=' in content and len(content.split('OPENAI_API_KEY=')[1].split('\n')[0].strip()) < 10:
                print("⚠️  Warning: OpenAI API key not configured properly")
                print("   Please edit .env file and add your OpenAI API key")
                print("   AI features will not work without a valid API key")
            else:
                print("✅ OpenAI API key appears to be configured")
    else:
        print("⚠️  Warning: .env file not found")

def print_success_message():
    """Print success message with next steps"""
    success_message = """
    🎉 FinanceAI setup completed successfully!
    
    Next steps:
    1. Edit .env file and add your OpenAI API key if you haven't already
    2. Run: python manage.py runserver
    3. Open your browser to: http://127.0.0.1:8000
    4. Register a new account or use the admin interface at /admin/
    
    Features available:
    ✓ Financial transaction tracking
    ✓ Budget management with alerts
    ✓ Savings goals tracking
    ✓ AI-powered financial advisor (with API key)
    ✓ Student job recommendations
    ✓ Analytics and insights
    
    Need help? Check README.md for detailed documentation.
    
    Happy budgeting! 💰🤖
    """
    print(success_message)

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    check_python_version()
    check_pip()
    
    # Setup steps
    install_dependencies()
    setup_environment()
    run_migrations()
    create_superuser()
    initialize_data()
    check_openai_key()
    
    # Success message
    print_success_message()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)