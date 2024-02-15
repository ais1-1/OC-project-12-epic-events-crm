from django.db import models
from django.conf import settings

from contracts.models import Contract


class Event(models.Model):
    """
    Event model

    Attributes:


    Methods:

    """

    PLANNED = "PLANNED"
    HELD = "HELD"
    NOT_HELD = "NOT HELD"
    NOT_STARTED = "NOT STARTED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

    EVENT_STATUS = (
        (PLANNED, "Planned"),
        (HELD, "Held"),
        (NOT_HELD, "Not Held"),
        (NOT_STARTED, "Not Started"),
        (STARTED, "Started"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
    )

    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.TextField(blank=True)
    number_of_attendees = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        limit_choices_to={"signed": True},
        related_name="event",
    )
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role_id": 3},
    )
    status = models.CharField(
        choices=EVENT_STATUS, max_length=64, blank=True, null=True, default=PLANNED
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        db_table = "event"
        # Last created item first
        ordering = ("-created_date",)

    def __str__(self):
        """Readable representation of User object."""
        return f"{self.id}: {self.name} - {self.status}"

    @property
    def client_name(self):
        if self.contract.client:
            return f"{self.contract.client.full_name}"
        else:
            return "No client for the contract."

    @property
    def client_email(self):
        if self.contract.client:
            return f"{self.contract.client.email}"
        else:
            return "No client for the contract."

    @property
    def client_phone(self):
        if self.contract.client and self.contract.client.phone:
            return f"{self.contract.client.phone}"
        elif not self.contract.client.phone:
            return "Data unavailable."
        else:
            return "No client for the contract."
