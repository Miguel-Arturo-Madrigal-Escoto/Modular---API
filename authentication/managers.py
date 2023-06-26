from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a user instance in the database.
        """
        if not email:
            raise ValueError('The email must be provided.')
        email = self.normalize_email(email=email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
