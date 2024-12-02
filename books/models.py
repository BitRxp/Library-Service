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
