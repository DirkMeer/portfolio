from django.urls import path
from .views import *

urlpatterns = [
    path('create_item/', create_item, name='create_item'),
    path('edit_item/<int:pk>', edit_item, name='edit_item'),
    path('delete_item/<int:pk>', delete_item, name='delete_item'),
    path('category_dash/', category_dash, name='category_dash'),
    path('set_currency/', set_currency, name='set_currency'),
    path('demo_account/', demo_account, name='demo_account'),
    path('', dashboard, name='dashboard'),
    # User management urls
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password', reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>', reset_password_confirm, name='reset_password_confirm'),
]
