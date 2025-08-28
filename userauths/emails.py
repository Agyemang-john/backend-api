from djoser.email import PasswordResetEmail

class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = 'emails/password_reset.html'  # This is the path to your actual template
