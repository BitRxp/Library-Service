from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hard"
        SOFT = "SOFT", "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=255,
        choices=CoverType.choices,
        default=CoverType.HARD
    )
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="The number of this specific book available in the library"
    )
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator("0.01")],
        help_text="Daily fee in $USD"
    )

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return = models.DateField()
    actual_return = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def __str__(self):
        return (
            f"{self.user}"
            f" borrowed {self.book}"
            f" on {self.borrow_date}"
        )


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        choices=Status.choices,
        default=Status.PENDING,
        max_length=7,
    )
    type = models.CharField(
        choices=Type.choices,
        default=Type.PAYMENT,
        max_length=7,
    )
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    Session_url = models.URLField(
        help_text="URL to Stripe payment session"
    )

    session_id = models.CharField(
        max_length=255,
        help_text="ID of Stripe payment session"
    )
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Calculated borrowing total price in $USD"
    )

    def __str__(self):
        return (
            f"Payment for Borrowing ID"
            f" {self.borrowing.id}: {self.status}"
            f" ({self.type})"
        )
