from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.test import RequestFactory
from expense_tracker.models import *
from expense_tracker.decorators import *
from expense_tracker.utils import *



class ExpenseTrackerTest(TestCase):

    # User tests
    def create_user(self, username='test', email='test@example.com', currency_symbol='T', password='microwaveoven'):
        User = get_user_model()
        test_user = User.objects.create(username=username, email=email, password=password)
        test_user.currency_symbol = currency_symbol
        test_user.save()
        return test_user
    
    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, get_user_model()))
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.currency_symbol, 'T')

    def test_email_unique_enforcement(self):
        user1 = self.create_user()
        with self.assertRaises(IntegrityError):
            self.create_user()
    
    def test_setting_creation(self):
        test_user = self.create_user()
        setting = Setting.objects.get(user=test_user)
        setting.currency_symbol = 'Q'
        setting.save()
        self.assertTrue(isinstance(setting, Setting))
        self.assertEqual(setting.__str__(), f'Currency: test - Q')

    def test_create_user_setting_if_nonexistent(self):
        test_user = self.create_user()
        setting = Setting.objects.get(user=test_user)
        setting.delete()
        setting.save()        
        setting = Setting.objects.get(user=test_user)
        self.assertTrue(isinstance(setting, Setting))
        self.assertEqual(setting.__str__(), f'Currency: test - $')



    # Model tests
    def create_category(self, user, time):
        return Category.objects.create(
            name='Test category',
            created_at=time,
            created_by=user,
            lastmodified_at=time,
        )
    def test_category_creation(self):
        test_user = self.create_user()
        test_time = timezone.now()
        category = self.create_category(test_user, test_time)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), 'Test category')

    def create_expense(self, user, time):
        return Expense.objects.create(
            description='Test expense',
            amount=300,
            created_at=time,
            created_by=user,
            lastmodified_at=time,
            date=time,
            category=self.create_category(user, timezone.now()),
        )
    def test_expense_creation(self):
        test_user = self.create_user()
        test_time = timezone.now()
        expense = self.create_expense(test_user, test_time)
        self.assertTrue(isinstance(expense, Expense))
        self.assertEqual(expense.__str__(), f'300 Test expense {test_time}')

    def create_monthly_expense(self, user, time):
        return MonthlyExpense.objects.create(
            description='Test monthly expense',
            amount=400,
            created_at=time,
            created_by=user,
            lastmodified_at=time,
        )
    def test_monthly_expense_creation(self):
        test_user = self.create_user()
        test_time = timezone.now()
        monthly_expense = self.create_monthly_expense(test_user, test_time)
        self.assertTrue(isinstance(monthly_expense, MonthlyExpense))
        self.assertEqual(monthly_expense.__str__(), f'Test monthly expense 400')

    def create_income(self, user, time):
        return Income.objects.create(
            description='Test income',
            amount=500,
            created_at=time,
            created_by=user,
            lastmodified_at=time,
            date=time,
        )
    def test_income_creation(self):
        test_user = self.create_user()
        test_time = timezone.now()
        income = self.create_income(test_user, test_time)
        self.assertTrue(isinstance(income, Income))
        self.assertEqual(income.__str__(), f'Test income 500')

    def create_monthly_income(self, user, time):
        return MonthlyIncome.objects.create(
            description='Test monthly income',
            amount=2200,
            created_at=time,
            created_by=user,
            lastmodified_at=time,
        )
    def test_monthly_income_creation(self):
        test_user = self.create_user()
        test_time = timezone.now()
        monthly_income = self.create_monthly_income(test_user, test_time)
        self.assertTrue(isinstance(monthly_income, MonthlyIncome))
        self.assertEqual(monthly_income.__str__(), f'Test monthly income 2200')



    # Decorator tests
    def test_user_not_authenticated_decorator_w_authenticated_user(self):
        test_user = self.create_user()
        @user_not_authenticated()
        def test_view(request):
            return HttpResponse()
        request = RequestFactory().get('/foo')
        request.user = test_user
        resp = test_view(request)
        # Test is authenticated user is redirected
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated_decorator_w_unauthenticated_user(self):
        test_user = AnonymousUser()
        @user_not_authenticated()
        def test_view(request):
            return HttpResponse()
        request = RequestFactory().get('/foo')
        request.user = test_user
        resp = test_view(request)
        # Test if unauthenticated user gets to see the page
        self.assertEqual(resp.status_code, 200)

    

    # Utils tests
    def test_query_redirect(self):
        url = reverse('login')
        test_user = AnonymousUser()
        request = RequestFactory().get('/foo')
        request.user = test_user
        def test_view(request):
            return query_redirect(url, {'next': '/expense_tracker/'})
        resp = test_view(request)
        self.assertEqual(resp.url, '/user/login/?next=%2Fexpense_tracker%2F')


    def test_get_reference_year_month_single_digit_month(self):
        test_user = self.create_user()
        setting = Setting.objects.get(user=test_user)
        setting.last_viewed_year_month = '20234'
        setting.save()
        request = RequestFactory().get('/foo')
        request.user = test_user
        ref_ym = get_reference_year_month(request)
        self.assertEqual(ref_ym, ['2023', '4'])

    def test_get_reference_year_month_double_digit_month(self):
        test_user = self.create_user()
        setting = Setting.objects.get(user=test_user)
        setting.last_viewed_year_month = '202312'
        setting.save()
        request = RequestFactory().get('/foo')
        request.user = test_user
        ref_ym = get_reference_year_month(request)
        self.assertEqual(ref_ym, ['2023', '12'])

    def test_get_next_and_previous_month_and_year(self):
        self.assertEqual(
            get_next_and_previous_month_and_year(4, 2023),
            {'month_minus': 3, 'year_minus': 2023, 'month_plus': 5, 'year_plus': 2023}
        )
        self.assertEqual(
            get_next_and_previous_month_and_year(1, 2023),
            {'month_minus': 12, 'year_minus': 2022, 'month_plus': 2, 'year_plus': 2023}
        )
        self.assertEqual(
            get_next_and_previous_month_and_year(12, 2022),
            {'month_minus': 11, 'year_minus': 2022, 'month_plus': 1, 'year_plus': 2023}
        )



    # View tests
    def test_login_redirect_on_protected_views(self):
        test_user = AnonymousUser()
        request = RequestFactory().get('dashboard')
        request.user = test_user
        urls = [
            reverse('dashboard'),
            reverse('create_item'), 
            reverse('edit_item', kwargs={'pk': 1}), 
            reverse('delete_item', kwargs={'pk': 1}), 
            reverse('category_dash'), 
            reverse('set_currency'), 
            reverse('change_password')
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertRedirects(resp, f'{reverse("login")}?next={url}', status_code=302)