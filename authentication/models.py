from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from teams.models import Team


class UserManager(BaseUserManager):
    """
    Personalized User class manager.

    Methods :
    create_user: create and save a user with an email, a password and a role.
        If user is in Management team, it gives the superuser privileges.

    create_superuser: create and save superuser with email, password and admin privileges.
    """

    def create_user(self, email, password=None, role=None, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)

        # If the user is in Management team, set as super user
        if str(role) == "MANAGEMENT":
            user.is_superuser = True

        # Do all validations
        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set the first Team instance, ie Management, as default value for role
        extra_fields.setdefault("role", Team.objects.get_or_create(pk=1)[0])
        # Set a first name as default
        extra_fields.setdefault("first_name", "Epic")
        # Set a last name as default
        extra_fields.setdefault("last_name", "Admin")
        # Create super user by calling create_user
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model

    Attributes:
    email (str): email of the user
    first_name (str): first name of the user
    last_name (str): last name of the user
    role (int): Team model instance's id, by default it is set to Management
    joined_date (str): Date of joining in the company
    created_date (str): Date of creation of an instance

    Property:
    full_name: Returns full name by concatenating last and first name accessible like an attribute.
    """

    email = models.EmailField(max_length=254, unique=True, editable=True)
    first_name = models.CharField(max_length=128, help_text="First name of the user")
    last_name = models.CharField(max_length=128, help_text="Last name of the user")
    role = models.ForeignKey(
        to=Team, on_delete=models.SET_NULL, null=True, related_name="team_members"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """Readable representation of User object."""
        return f"{self.id}: {self.last_name} {self.first_name} ({self.email})"

    @property
    def full_name(self):
        """Returns full name in the format <last name> <first name>."""
        return f"{self.last_name} {self.first_name}"
