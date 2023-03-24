from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

UserModel = get_user_model()

# Custom backend / allow users to login with email or username to conform to current web standards.
class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        # This will never happen but for testing (non-unique emails are rejected on signup).
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # Check password and if user account is active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        # Alert the user if password is correct but account not yet activated
        elif user.check_password(password) and not getattr(user, 'is_active'):
            messages.add_message(
                request, messages.ERROR, f"Your account has not yet been activated. Please check your email and click the activation link before continuing."
            )
            return None
        else:
            return None