from allauth.account.forms import ResetPasswordForm as BaseResetPasswordForm
from allauth.account.forms import SignupForm as BaseSignupForm


class ResetPasswordForm(BaseResetPasswordForm):
    def _send_unknown_account_mail(self, request, email):
        # Overriding this method to prevent sending emails to unknown accounts
        pass


class SignupForm(BaseSignupForm):
    def _send_account_already_exists_mail(self, request):
        # Overriding this method to prevent sending emails to account already exists accounts
        pass
