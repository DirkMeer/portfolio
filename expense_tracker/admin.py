from django.contrib import admin
from .models import Category, Expense, Income, MonthlyExpense, MonthlyIncome, Setting

# Register your models here.
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(MonthlyExpense)
admin.site.register(MonthlyIncome)
admin.site.register(Setting)
