from django.db import models
from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .errors import EmailNotUniqueError



class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(
        verbose_name='Created at',
        # Auto_now_add sets the value only once on object creation.
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name='Created by',
        blank=True,
        related_name='created_%(app_label)s_%(class)s',
        on_delete=models.CASCADE,
    )
    lastmodified_at = models.DateTimeField(
        verbose_name='Last modified at',
        # Auto_now will update the value each time the save() method is called.
        auto_now=True,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Categories'


class CommonTransactionInfo(models.Model):
    description = models.CharField(max_length=25)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name='Created by',
        # Blank skips form validation (we need to add the user object in the view ourselves).
        blank=True, 
        # This is the reverse name, but it must be unique for every single child class. Django provides the %(class)s which will be replaced by Expense-> expenses for each child class. The app label part does the same using the expense_tracker name to guarantee unique names. So the User could reverse lookup it's created expenses through created_expense_tracker_expenses
        related_name='created_%(app_label)s_%(class)s',
        # We left null=False default on. This ensures no ownerless entries are stored in the database.
        on_delete=models.CASCADE,
    )
    lastmodified_at = models.DateTimeField(
        verbose_name='Last modified at',
        auto_now=True,
    )

    class Meta:
        abstract = True
        # This class will only be used to inherit other classes from, no databases tables will be created from this model directly.


class Expense(CommonTransactionInfo):
    # Make sure not to call today() as it would only get called once on class definition (and keep the same date thereafter for however long the server is up)
    date = models.DateField(default=date.today)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f'{self.amount} {self.description} {self.date}'


class MonthlyExpense(CommonTransactionInfo):
    def __str__(self):
        return f'{self.description} {self.amount}'  


class Income(CommonTransactionInfo):
    date = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.description} {self.amount}'  

    class Meta:
        verbose_name_plural = 'Income'


class MonthlyIncome(CommonTransactionInfo):
    def __str__(self):
        return f'{self.description} {self.amount}'

    class Meta:
        verbose_name_plural = 'Monthly income'



# Settings -> linked to User model.
class Setting(models.Model):
    # Field allows only one connection either side
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency_symbol = models.CharField(max_length=3, default='$')
    last_viewed_year_month = models.CharField(max_length=6, null=True)

    def __str__(self):
        return f'Currency: {self.user} - {self.currency_symbol}'

# If email is already in use, raise an error so the view can inform the site user
@receiver(pre_save, sender=User)
def email_unique_check(sender, instance, **kwargs):
    email = instance.email
    if sender.objects.filter(email=email).exclude(username=instance.username).exists():
        raise EmailNotUniqueError

# This receiver listens to a save executed by User, and will execute a post_save action
@receiver(post_save, sender=User)
def create_user_setting(sender, instance, created, **kwargs):
    # If a new user is created a new setting will be created
    if created:
        Setting.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_setting(sender, instance, **kwargs):
    # If a User has been updated the setting will be updated
    try:
        instance.setting.save()
    # If for some reason the setting object does not exist
    except:
        Setting.objects.create(user=instance)

