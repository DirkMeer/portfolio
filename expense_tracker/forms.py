from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from .models import *


# Base class for the description and amount fields reused in every single form.
class BaseTransactionForm(forms.ModelForm):
    description = forms.CharField(
        required = True,
        max_length = 25,
        widget = forms.widgets.TextInput(
            attrs={
                'placeholder': 'Description',
                'class': 'form-control',
                'autofocus': True,
                'autocomplete': 'off',
            }
        ),
    )
    amount = forms.DecimalField(
        required = True,
        max_digits = 14,
        decimal_places= 2,
        widget = forms.widgets.TextInput(
            attrs={
                'placeholder': 'Amount',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
    )


# Base class to add the default to today date picker
class DateDefaultTodayForm(forms.ModelForm):
    date = forms.DateField(
        required = True,
        initial = date.today,
        widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )


# Python can inherit from multiple base classes in order and then add more fields manually
class ExpenseCreationForm(BaseTransactionForm, DateDefaultTodayForm):
    category = forms.ModelChoiceField(
        # We must provide the queryset, so just set it to none initially
        queryset = None,
        empty_label = "(None)",
        widget = forms.widgets.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Get the request we passed in from the view
        self.request = kwargs.pop('request')
        # Call the init of the super class as it otherwise would have
        super(ExpenseCreationForm, self).__init__(*args, **kwargs)
        # Override the queryset we set to none above to provide the selectors choices.
        self.fields['category'].queryset = Category.objects.filter(created_by=self.request.user.id)

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category']


class MonthlyExpenseCreationForm(BaseTransactionForm):
    class Meta:
        model = MonthlyExpense
        fields = ['description', 'amount']


class IncomeCreationForm(BaseTransactionForm, DateDefaultTodayForm):
    class Meta:
        model = Income
        fields = ['description', 'amount', 'date']


class MonthlyIncomeCreationForm(BaseTransactionForm):
    class Meta:
        model = MonthlyIncome
        fields = ['description', 'amount']


class CategoryCreationForm(forms.ModelForm):
    name = forms.CharField(
        required = True,
        max_length = 20,
        widget = forms.widgets.TextInput(
            attrs={
                'placeholder': 'Description (e.g. groceries)',
                'class': 'form-control',
                'autofocus': True,
                'autocomplete': 'off',
            }
        ),
    )
    class Meta:
        model = Category
        fields = ['name']

    
class CurrencyEditForm(forms.ModelForm):
    currency_symbol = forms.CharField(
        max_length=3,
        required = True,
        widget = forms.widgets.TextInput(
            attrs={
                'placeholder': 'Description',
                'class': 'form-control',
                'autofocus': True,
                'autocomplete': 'off',
            }
        )
    )
    class Meta:
        model = Setting
        fields = ['currency_symbol']




### User Management Forms ###
class AuthenticationFormCaptcha(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormCaptcha, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email or Username'}),
        label="Email or Username")
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please provide a valid email address')
    currency_symbol = forms.CharField(max_length=3, help_text='Provide a valid currency symbol or skip for $')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ('username', 'email', 'currency_symbol', 'password1', 'password2', 'captcha')


class PasswordResetFormCaptcha(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetFormCaptcha, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


