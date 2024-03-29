import uuid
from django.db import models
from django.conf import settings

from clients.models import Client


class Contract(models.Model):
    """
    Contract model

    Attributes:
    id (uuid) - id of the contract
    total_amount (Decimal) - price of the contract
    amount_due (Decimal) - remaining amount to pay
    signed (bool) - contract is signed or not
    client (int) - client related to the contract
    sales_contact (int) - contact from sales team of the client (assigned during client assignment)
    created_date (str) - date of creation of the instance
    updated_date(str) - date of last update of the instance


    Methods:
        save - save contract. If the sales_contact is not defined,
            assign the one related to client if any.

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    amount_due = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2
    )
    signed = models.BooleanField(default=False)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contracts",
    )
    # Limit choices for the contact to Sales team
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_contracts",
        limit_choices_to={"role_id": 2},
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        db_table = "contract"
        # First created item first
        ordering = ("created_date",)

    def __str__(self):
        """Readable representation of User object."""
        status = "Contract signed" if self.signed else "Contract not signed"
        if self.client:
            return f"{self.id}: {status} - {self.client.full_name}"
        else:
            return f"{self.id}: {status} - Client info is unavailable"

    def save(self, *args, **kwargs):
        if not self.sales_contact and self.client and self.client.sales_contact:
            self.sales_contact = self.client.sales_contact
        if not self.amount_due:
            self.amount_due = 0.0

        super(Contract, self).save(*args, **kwargs)
