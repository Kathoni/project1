# FinanceAI Wallet

FinanceAI Wallet is a Django-based personal finance management web application that helps users track transactions, manage budgets, set savings goals, and discover remote job opportunities. It features analytics dashboards, AI-powered financial advice, and a user-friendly interface.

## Features

- **User Registration & Authentication:** Secure sign-up, login, and profile setup.
- **Transactions:** Add, view, and filter income, expenses, and transfers.
- **Budgets:** Set and monitor budgets by category and period.
- **Savings Goals:** Create, track, and prioritize savings goals.
- **Analytics:** Visualize spending, income, and trends with interactive charts.
- **Job Opportunities:** Browse and apply for remote jobs, with student-friendly filters.
- **AI Financial Advisor:** Get personalized financial advice via chat.
- **Responsive UI:** Modern, mobile-friendly design using Bootstrap.

## Project Structure

```
wallet/
├── .env
├── db.sqlite3
├── manage.py
├── requirements.txt
├── wallet/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── walletstatus/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── templates/
│   └── templatetags/
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### Installation

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd wallet
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Copy `.env.example` to `.env` and configure as needed.

5. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser (optional, for admin access):**
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

8. **Access the app:**
    - Open [http://localhost:8000](http://localhost:8000) in your browser.

## Usage

- Register a new account or log in.
- Set up your profile and financial preferences.
- Add transactions, create budgets, and set savings goals.
- Explore analytics and get AI-powered advice.
- Browse and apply for remote job opportunities.

## Customization

- **Templates:** Modify HTML templates in `wallet/walletstatus/templates/` for UI changes.
- **Models:** Extend models in [`walletstatus/models.py`](wallet/walletstatus/models.py) for new features.
- **Admin:** Manage data via Django admin at `/admin/`.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

**FinanceAI Wallet** – Your intelligent financial assistant.