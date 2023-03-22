from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Make a hash including the timestamp (hash should be unique and change every time)
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )
    
account_activation_token = AccountActivationTokenGenerator()