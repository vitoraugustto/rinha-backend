from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Trait"
        verbose_name_plural = "Traits"


class Occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"


class Fighter(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(verbose_name="Biography")
    age = models.PositiveIntegerField(
        verbose_name="Age",
        validators=[MinValueValidator(0), MaxValueValidator(120)],
    )
    height = models.PositiveIntegerField(
        verbose_name="Height (cm)",
        validators=[MinValueValidator(50), MaxValueValidator(300)],
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Weight (kg)",
        validators=[MinValueValidator(10), MaxValueValidator(500)],
    )
    traits = models.ManyToManyField(Trait, related_name="fighters", blank=True)
    occupation = models.ForeignKey(
        Occupation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fighters",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Fighter"
        verbose_name_plural = "Fighters"
