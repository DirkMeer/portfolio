from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import calendar, random, uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta


from .models import Category, MonthlyExpense, MonthlyIncome, Expense, Income
from .demo_user_data import *


def create_category(name, user) -> None:
    Category.objects.create(
        name=name,
        created_by=user,
    )


def create_monthly_expense(description, amount, user) -> None:
    MonthlyExpense.objects.create(
        description=description,
        amount=amount,
        created_by=user,
    )


def create_expense(description, amount, user, category, date) -> None:
    Expense.objects.create(
        description=description,
        amount=amount,
        created_by=user,
        date=date,
        category=category,
    )


def create_monthly_income(description, amount, user) -> None:
    MonthlyIncome.objects.create(
        description=description,
        amount=amount,
        created_by=user,
    )


def create_income(description, amount, user) -> None:
    Income.objects.create(
        description=description,
        amount=amount,
        created_by=user,
        date=timezone.now(),
    )


def get_category(name, user) -> Category:
    return Category.objects.get(created_by=user, name=name)


def get_date(month_offset=0):
    """Returns the year, month and a random day for the current month + the offset"""
    date = datetime.now() + relativedelta(months=month_offset)
    _, days_in_month = calendar.monthrange(date.year, date.month)
    random_day = random.randrange(1, days_in_month + 1)
    return datetime(date.year, date.month, random_day)


def create_and_log_in_demo_user(request):
    # Generate a unique name and details for the demo user
    User = get_user_model()
    unique_id = str(uuid.uuid4())
    username = f"demo_user_{unique_id[-8:]}"
    user_email = f"{unique_id[-8:]}@dirkmeer.com"
    currency_symbol = "$"
    raw_password = "Microwaveoven123"
    # Hash the password and keep the raw password to login
    password = make_password(raw_password)
    demo_user = User.objects.create(
        username=username, email=user_email, password=password
    )
    demo_user.currency_symbol = currency_symbol
    demo_user.save()
    print(demo_user)
    # Login as the demo user account just created (demo_account starts as activate)
    user = authenticate(request, username=username, password=raw_password)
    if user is not None:
        login(request, user)
        return user
    else:
        return None


def create_mock_user_data(request, user):
    for category in categories:
        create_category(category, user)
    cat_groceries = get_category(categories[0], user)
    cat_nonfood = get_category(categories[1], user)
    cat_medical = get_category(categories[2], user)
    cat_rest_deli = get_category(categories[3], user)
    cat_pets = get_category(categories[4], user)
    cat_car = get_category(categories[5], user)
    create_monthly_income("Paycheck", 3100, user)
    create_monthly_expense("Rent", 650, user)
    create_monthly_expense("Health-insurance", 280, user)
    create_monthly_expense("Phones", 60, user)
    create_monthly_expense("Internet", 35, user)
    create_income("Sold old bike", 150, user)

    create_expense("Catfood", 12.50, user, cat_pets, get_date())
    create_expense("Cat grooming", 23.50, user, cat_pets, get_date())
    create_expense("Cat snacks", 8.75, user, cat_pets, get_date())
    create_expense("New toys for cats", 15.40, user, cat_pets, get_date())
    create_expense("Dentist", 180, user, cat_medical, get_date())
    create_expense("Medicine", 8.60, user, cat_medical, get_date())
    create_expense("Pizza delivery", 23.95, user, cat_rest_deli, get_date())
    create_expense("Chinese restaurant", 46, user, cat_rest_deli, get_date())
    create_expense("Thai food", 36.70, user, cat_rest_deli, get_date())
    create_expense("Car payment", 423.86, user, cat_car, get_date())
    create_expense("Gas", 64.78, user, cat_car, get_date())
    create_expense("Grocery shopping", 86.75, user, cat_groceries, get_date())
    create_expense("Birthday cake", 8.75, user, cat_groceries, get_date())
    create_expense("Restocking freezer", 55.18, user, cat_groceries, get_date())
    create_expense("Weekly groceries", 126.25, user, cat_groceries, get_date())
    create_expense("Snacks and bread", 8.60, user, cat_groceries, get_date())
    create_expense("Fruit market", 12, user, cat_groceries, get_date())
    create_expense("Groceries", 23.45, user, cat_groceries, get_date())
    create_expense("Pants + tshirts", 88.90, user, cat_nonfood, get_date())
    create_expense("Cleaning supplies", 17.50, user, cat_nonfood, get_date())
    create_expense("New chairs", 129.50, user, cat_nonfood, get_date())

    create_expense("Catfood", 11.50, user, cat_pets, get_date(-1))
    create_expense("Cat snacks", 12.50, user, cat_pets, get_date(-1))
    create_expense("Cat snacks", 4.95, user, cat_pets, get_date(-1))
    create_expense("New cat tower", 65.40, user, cat_pets, get_date(-1))
    create_expense("Medicine", 9.45, user, cat_medical, get_date(-1))
    create_expense("Italian food", 33.95, user, cat_rest_deli, get_date(-1))
    create_expense("Chinese", 28.30, user, cat_rest_deli, get_date(-1))
    create_expense("Falafel", 16.85, user, cat_rest_deli, get_date(-1))
    create_expense("Pancakes", 23.46, user, cat_rest_deli, get_date(-1))
    create_expense("Car payment", 426.34, user, cat_car, get_date(-1))
    create_expense("Car repairs", 200, user, cat_car, get_date(-1))
    create_expense("Gas", 58.36, user, cat_car, get_date(-1))
    create_expense("Grocery shopping", 92.75, user, cat_groceries, get_date(-1))
    create_expense("Birthday cake", 9.25, user, cat_groceries, get_date(-1))
    create_expense("Restocking freezer", 56.38, user, cat_groceries, get_date(-1))
    create_expense("Weekly groceries", 113.25, user, cat_groceries, get_date(-1))
    create_expense("Snacks and bread", 9.60, user, cat_groceries, get_date(-1))
    create_expense("Fruit market", 10, user, cat_groceries, get_date(-1))
    create_expense("Groceries", 23.68, user, cat_groceries, get_date(-1))
    create_expense("Socks", 12.99, user, cat_nonfood, get_date(-1))
    create_expense("Jacket", 36.95, user, cat_nonfood, get_date(-1))
    create_expense("Cleaning supplies", 12.50, user, cat_nonfood, get_date(-1))
    create_expense("New desk for study", 112.50, user, cat_nonfood, get_date(-1))

    create_expense("Catfood", 20.50, user, cat_pets, get_date(-2))
    create_expense("Cat snacks", 16.50, user, cat_pets, get_date(-2))
    create_expense("Cat snacks", 2.95, user, cat_pets, get_date(-2))
    create_expense("Cat grooming", 18.60, user, cat_pets, get_date(-2))
    create_expense("Turkish kebab", 12.95, user, cat_rest_deli, get_date(-2))
    create_expense("Chinese", 29.60, user, cat_rest_deli, get_date(-2))
    create_expense("Burritos", 16.85, user, cat_rest_deli, get_date(-2))
    create_expense("Chicken", 32.20, user, cat_rest_deli, get_date(-2))
    create_expense("Car payment", 420.34, user, cat_car, get_date(-2))
    create_expense("Gas", 78.56, user, cat_car, get_date(-2))
    create_expense("Grocery shopping", 12.75, user, cat_groceries, get_date(-2))
    create_expense("Grocery shopping", 98.34, user, cat_groceries, get_date(-2))
    create_expense("Cookies", 5.25, user, cat_groceries, get_date(-2))
    create_expense("Restocking freezer", 24.56, user, cat_groceries, get_date(-2))
    create_expense("Weekly groceries", 146.25, user, cat_groceries, get_date(-2))
    create_expense("Snacks and bread", 7, user, cat_groceries, get_date(-2))
    create_expense("Fruit market", 12, user, cat_groceries, get_date(-2))
    create_expense("Groceries", 23.84, user, cat_groceries, get_date(-2))
    create_expense("New Suit", 87.99, user, cat_nonfood, get_date(-2))
    create_expense("Sweater", 36.95, user, cat_nonfood, get_date(-2))
    create_expense("Cleaning supplies", 22.50, user, cat_nonfood, get_date(-2))
    create_expense("Plants", 12.50, user, cat_nonfood, get_date(-2))
