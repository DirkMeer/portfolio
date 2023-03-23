from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expense_tracker.forms import AuthenticationFormCaptcha

urlpatterns = [
    path('', include('portfolio.urls')),
    # path('blog/', include('blog.urls')), --disabled for now
    path('expense_tracker/', include('expense_tracker.urls')),
    # Custom define the login page to add a captcha to the form
    path('user/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=AuthenticationFormCaptcha),
        name='login'),
    path('user/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
]
