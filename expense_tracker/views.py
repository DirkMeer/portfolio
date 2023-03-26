from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms.models import model_to_dict
# Signup imports
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q

from .forms import SignUpForm, PasswordResetFormCaptcha, CurrencyEditForm
from .decorators import *
from .demo_user import *
from .models import *
from .app_settings import *
from .graphs import *
from .utils import *
from .tokens import account_activation_token

LOGIN_URL = '/user/login/'


@login_required(login_url=LOGIN_URL)
def dashboard(request):
    try: # Get desired view from url query
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
    except (ValueError, TypeError):
        # Use today as default if not provided
        month: int = datetime.now().month
        year: int = datetime.now().year
    context = {'month': month, 'year': year,}
    current_user = Setting.objects.get(user=request.user.id)
    # Save the last viewed year/month for future cancel button redirects
    current_user.last_viewed_year_month = f'{str(year)}{str(month)}'
    current_user.save()
    # Get the correct 1 month forward/backward date and merge into the current context dictionary
    context = context | get_next_and_previous_month_and_year(month, year)
    # Test if there are expenses to display -> if not render empty_dash
    context['Expense'] = Expense.objects.filter(date__year=year, date__month=month).filter(created_by=request.user.id).order_by('-date')
    if not context['Expense']:
        return render(request, 'expense_tracker/empty_dash.html', context)
    # Get the rest of our display objects
    context['Income'] = Income.objects.filter(date__year=year, date__month=month).filter(created_by=request.user.id).order_by('-date')
    context['MonthlyIncome'] = MonthlyIncome.objects.filter(created_by=request.user.id).order_by('-amount')
    context['MonthlyExpense'] = MonthlyExpense.objects.filter(created_by=request.user.id).order_by('-amount')
    context['Currency'] = current_user.currency_symbol or '$'
    # Get aggregated sums for total balance / expenses. If no return assign 0.
    exp_sum = context['Expense'].aggregate(Sum('amount'))['amount__sum'] or 0
    mon_exp_sum = context['MonthlyExpense'].aggregate(Sum('amount'))['amount__sum'] or 0
    in_sum = context['Income'].aggregate(Sum('amount'))['amount__sum'] or 0
    mon_in_sum = context['MonthlyIncome'].aggregate(Sum('amount'))['amount__sum'] or 0
    context['tot_income'] = in_sum + mon_in_sum
    context['tot_expenses'] = exp_sum + mon_exp_sum
    context['balance'] = context['tot_income'] - context['tot_expenses']
    # Get our graphs and render the dashboard
    category_labels, money_values = get_chart_data(request, mon_exp_sum, year, month)
    context['pie_chart'] = pie_chart(category_labels, money_values)
    context['bar_chart'] = bar_chart(category_labels, money_values, context['Currency'])
    return render(request, './expense_tracker/dashboard.html', context)


@login_required(login_url=LOGIN_URL)
def create_item(request):
    mode = request.GET.get('mode')
    # If the mode is not Category creation and the user has no categories, redirect to category dash.
    # Using .exists() is cheaper here
    if not mode == 'Cat' and not Category.objects.filter(created_by=request.user).exists():
        return redirect('category_dash')
    # Get the appropriate form and title
    form, title = create_view_settings[str(mode)]
    if request.method == 'POST':
        # If it's an expense, pass request to retrieve category choice list
        if mode == 'Ex':
            form = form(request.POST, request=request)
        else:
            form = form(request.POST)
        if form.is_valid():
            # Save but add more before commit, also retain the raw form data as the 'form' variable
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            # If newly created item was a category, add flash message
            if mode == 'Cat':
                messages.add_message(
                    request, messages.SUCCESS, f"Category '{form.cleaned_data['name']}' added successfully"
                )
            # Get currently created/edited objects year/month to redirect to correct view
            elif 'date' in form.cleaned_data:
                year = form.cleaned_data['date'].year
                month = form.cleaned_data['date'].month
                redirect_query = {'year': year, 'month': month}
                return query_redirect('dashboard', redirect_query)
            # If there is no 'data' field available use a regular redirect
            return redirect('dashboard')
    else:
        # Only if the mode is "Ex"pense make sure to pass in the request object to filter the queryset.
        form = form(request=request) if mode == 'Ex' else form()

    context = {'form': form, 'title': title, 'mode': mode}
    # add date of referring dash to refer back if user cancels after multiple create/edit/delete screens
    context['ref_year'], context['ref_month'] = get_reference_year_month(request)
    return render(request, './expense_tracker/create_item.html', context)


@login_required(login_url=LOGIN_URL)
def edit_item(request, pk):
    mode = request.GET.get('mode')
    form, title, model = edit_view_settings[str(mode)]
    # Get the item, wether it belongs to the user or not.
    item_to_edit = get_object_or_404(model, pk=pk)
    # Nothing will be shown nor any post data evaluated unless current user is the owner of this object.
    if item_to_edit.created_by == request.user:
        if request.method == 'POST':
            if mode == 'Ex':
                # expense form requires the request passed in.
                form = form(request.POST, instance=item_to_edit, request=request)
            else:
                form = form(request.POST, instance=item_to_edit)
            if form.is_valid():
                form.save()
                # Get currently created/edited objects year/month to redirect to that year/month's dash
                if 'date' in form.cleaned_data:
                    year = form.cleaned_data['date'].year
                    month = form.cleaned_data['date'].month
                    redirect_query = {'year': year, 'month': month}
                    return query_redirect('dashboard', redirect_query)
                # If there is no 'data' field available redirect to category dash or dashboard
                if mode == 'Cat':
                    return redirect('category_dash')
                else:
                    return redirect('dashboard')
        else:
            # Only if the mode is "Ex"pense make sure to pass in the request object
            if mode == 'Ex':
                form = form(initial=model_to_dict(item_to_edit), request=request)
            else:
                form = form(initial=model_to_dict(item_to_edit))
        context = {'form': form, 'title': title, 'edit': True, 'pk': pk, 'mode': mode}
        # add date of referring dash to refer back if user cancels
        context['ref_year'], context['ref_month'] = get_reference_year_month(request)
        return render(request, './expense_tracker/create_item.html', context)
    # If user failed the ownership check they will be redirected to the dashboard.
    else:
        return redirect('dashboard')


@login_required(login_url=LOGIN_URL)
def delete_item(request, pk):
    mode = request.GET.get('mode')
    model = edit_view_settings[str(mode)][-1]
    item_to_delete = get_object_or_404(model, pk=pk)
    # Before showing or editing/deleting anything check if user is owner of the item.
    if item_to_delete.created_by == request.user:    
        if request.method == 'POST':
            try: # Object to delete has a date property? > redirect back to that date's view
                date = item_to_delete.date
                item_to_delete.delete()
                messages.add_message(request, messages.SUCCESS, "Item was deleted successfully")
                redirect_query = {'year': date.year, 'month': date.month}
                return query_redirect('dashboard', redirect_query)
            except AttributeError: # Else just go back to the dashboard or category view
                item_to_delete.delete()
                messages.add_message(request, messages.SUCCESS, "Item was deleted successfully")
                if mode == 'Cat':
                    return redirect('category_dash')
                else:
                    return redirect('dashboard')

        # For GET requests load the 'are you sure you want to delete' page
        try: # Get either the description or the name
            description = item_to_delete.description
        except AttributeError:
            description = item_to_delete.name
        context = {'pk': pk, 'mode': mode, 'description': description}
        return render(request, './expense_tracker/delete_item.html', context)
    # If user failed the ownership check they will be redirected to the dashboard.
    else:
        return redirect('dashboard')


@login_required(login_url=LOGIN_URL)
def category_dash(request):
    context = {}
    context['categories'] = Category.objects.filter(created_by=request.user.id).order_by('name')
    return render(request, './expense_tracker/category_dash.html', context)


@login_required(login_url=LOGIN_URL)
def set_currency(request):
    # Get the user setting object
    user_settings_object = Setting.objects.get(user=request.user)
    if request.method == 'POST':
        form = CurrencyEditForm(request.POST, instance=user_settings_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Currency setting was successfully updated')
            year, month = get_reference_year_month(request)
            return query_redirect('dashboard', {'year': year, 'month': month})

    # Prepopulate a form with the user's setting object
    form = CurrencyEditForm(initial=model_to_dict(user_settings_object))
    # Call our edit template with the resulting form in context
    context = {'form': form, 'title': 'Set currency symbol', 'edit': True}
    # add date of referring dash to refer back if user cancels
    context['ref_year'], context['ref_month'] = get_reference_year_month(request)
    return render(request, './expense_tracker/set_currency.html', context)



### Email and account registration views ###
def demo_account(request):
    demo_user = create_and_log_in_demo_user(request)
    if demo_user:
        mock_data = create_mock_user_data(request, demo_user)
        messages.add_message(request, messages.SUCCESS, "Welcome to the demo user account. This one has been specially and uniquely generated with some data just for you! So please feel free to edit, delete or add anything and test the functionality, it will not affect anyone else on the site. If you log out a demo account you will not be able to log in to it again, but you can always create another demo account. Alternatively, you can create a real permanent account with password, activation and password reset abilities linked to your email address")
    return redirect('dashboard')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                # Start new user as inactive
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                user.refresh_from_db()
                # Save users currency symbol setting
                settings = Setting.objects.get(user=user)
                settings.currency_symbol = form.cleaned_data.get('currency_symbol')
                settings.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('dashboard')
            except EmailNotUniqueError:
                form = SignUpForm()
                messages.error(request, 'Email address is already associated with another account')

    else:
        form = SignUpForm()
    return render(request, './registration/signup.html', {'form': form})


def activateEmail(request, user, target_email):
    mail_subject = 'DirkMeer account activation link'
    message = render_to_string('email/account_activation_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[target_email])
    if email.send():
        messages.success(request, f'Welcome <b>{user}</b>! Please check your email <b>{target_email}</b> and click on the activation link.<br>(If you did not receive an email, please check your spam folder)')
    else:
        messages.error(request, f'There was a problem sending email to {target_email}, please check if your email address is correct')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email address. You can now log in using your login details')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has already been used.')

    return redirect('dashboard')


@redirect_demo_users_to_dash()
@login_required(login_url=LOGIN_URL)
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been successfully changed, you may now login using your new password.")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = PasswordChangeForm(user)
    return render(request, './registration/change_password.html', {'form': form})


@user_not_authenticated()
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetFormCaptcha(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=email)).first()
            if associated_user:
                subject = "DirkMeer.com password reset request"
                message = render_to_string("email/password_reset_email.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, "We've emailed instructions for resetting your password. If an account exists for the email address you entered you should receive them shortly.")
                else:
                    messages.error(request, "There was a problem sending email to this address.")
            
            return redirect('dashboard')
        
        else:
            # Provide extra clear CAPTCHA error message in case the user misses it
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, 'You must tick the "I\'m not a robot" box')
                    continue

    form = PasswordResetFormCaptcha()
    return render(request, './registration/reset_password.html', {'form': form})


def reset_password_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set successfully. You may go ahead and log in using your new password.')
                return redirect('dashboard')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        
        form = SetPasswordForm(user)
        return render(request, 'registration/reset_password_confirm.html', {'form': form})
    
    else:
        messages.error(request, 'Link is invalid or expired.')

    return redirect('dashboard')