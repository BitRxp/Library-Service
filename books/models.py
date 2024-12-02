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
        return f"{self.user} borrowed {self.book} on {self.borrow_date}"

