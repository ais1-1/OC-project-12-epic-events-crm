from django.db import models
from django.conf import settings


class Client(models.Model):
    """
    Client model

    Attributes:


    Methods:

    """

    email = models.EmailField(max_length=254, unique=True, editable=True)
    first_name = models.CharField(max_length=128, help_text="First name of the user")
    last_name = models.CharField(max_length=128, help_text="Last name of the user")
    # Null is to avoid unique constraint violations when saving multiple objects with blank values
    phone = models.CharField(max_length=25, null=True, blank=True, unique=True)
    company = models.CharField(max_length=128, blank=True)
    # Limit choices for the contact to Sales team
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        limit_choices_to={"role_id": 2},
    )
    note = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = "client"
        # Last updated item first
        ordering = ("-updated_date",)

    def __str__(self):
        """Readable representation of User object."""
        if self.sales_contact:
            return (
                f"{self.id}: {self.last_name} {self.first_name}; "
                + f"contact: {self.sales_contact.full_name} "
            )
        else:
            return f"{self.id}: {self.last_name} {self.first_name}; No sales contact yet..."

    @property
    def full_name(self):
        """Returns full name in the format <last name> <first name>.
        It can be called using object.full_name (see property decorator).
        """
        return f"{self.last_name} {self.first_name}"
