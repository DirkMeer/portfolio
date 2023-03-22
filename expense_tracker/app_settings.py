from .forms import *
from .models import *

# Used to provide the appropriate form, title and model to create_item.html.
# create_item.html is used to serve 10 different pages based on the mode.

create_view_settings = {
    'Ex': [ExpenseCreationForm, 'Add a new expense'],
    'MoEx': [MonthlyExpenseCreationForm, 'Add a new monthly expense'],
    'In': [IncomeCreationForm, 'Add new income'],
    'MoIn': [MonthlyIncomeCreationForm, 'Add new monthly income'],
    'Cat': [CategoryCreationForm, 'Add a new category'],
}

edit_view_settings = {
    'Ex': [ExpenseCreationForm, 'Edit expense', Expense],
    'MoEx': [MonthlyExpenseCreationForm, 'Edit monthly expense', MonthlyExpense],
    'In': [IncomeCreationForm, 'Edit income', Income],
    'MoIn': [MonthlyIncomeCreationForm, 'Edit monthly income', MonthlyIncome],
    'Cat': [CategoryCreationForm, 'Edit category', Category],
}