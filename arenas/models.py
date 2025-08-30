from django.core.validators import MinValueValidator
from django.db import models

from fighters.models import Fighter


class Arena(models.Model):
    location = models.CharField(
        max_length=100, unique=True, help_text="The location of the arena"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description",
        help_text="Detailed description of the arena",
    )

    def __str__(self):
        return str(self.location)

    class Meta:
        verbose_name = "Arena"
        verbose_name_plural = "Arenas"


class Match(models.Model):
    title = models.CharField(max_length=100, help_text="The title of the match")
    arena = models.ForeignKey(
        Arena,
        on_delete=models.CASCADE,
        related_name="matches",
        help_text="Arena where this match takes place",
    )
    fighters = models.ManyToManyField(
        Fighter, related_name="matches", help_text="Fighters in this match"
    )
    max_number_of_rounds = models.PositiveIntegerField(
        default=3, help_text="Max number of rounds in the match"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the match was created", editable=False
    )

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.title} - {' vs '.join(str(fighter) for fighter in self.fighters.all())}"

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"


class MatchResult(models.Model):
    OUTCOME_CHOICES = [
        ("win", "Win"),
        ("draw", "Draw"),
    ]

    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="result",
        help_text="The match this result belongs to",
    )
    outcome = models.CharField(
        max_length=20,
        choices=OUTCOME_CHOICES,
        help_text="The outcome of the match",
    )
    winner = models.ForeignKey(
        Fighter,
        on_delete=models.CASCADE,
        related_name="won_matches",
        null=True,
        blank=True,
        help_text="The fighter who won the match",
    )
    description = models.TextField(help_text="Description of the match result")

    def __str__(self):
        return f"{self.match} - Winner: {self.winner}"

    class Meta:
        verbose_name = "Match Result"
        verbose_name_plural = "Match Results"


class Round(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="rounds",
        help_text="The match this round belongs to",
    )
    round_number = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        help_text="The number of this round in the match",
    )
    winner = models.ForeignKey(
        Fighter,
        on_delete=models.CASCADE,
        related_name="won_rounds",
        null=True,
        blank=True,
        help_text="The fighter who won this round (null for draw rounds)",
    )
    description = models.TextField(
        verbose_name="description", help_text="What happened in this round."
    )

    def __str__(self):
        return f"Round {self.round_number}"

    class Meta:
        verbose_name = "Round"
        verbose_name_plural = "Rounds"
        unique_together = ["match", "round_number"]
