from djoser import email


class ActivationEmail(email.ActivationEmail):
    """
    Custom class to override the default account
    activation email.
    """
    template_name = 'authentication/activation_email.html'
