import string
import random

from django.db import models


class GameType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GameMove(models.Model):
    """
    This class defines the behavior of the game, assuming is always a two vs two game
    """
    name = models.CharField(max_length=100)
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    wins_to = models.ForeignKey(
        "GameMove",
        related_name="wins",
        null=True,
        on_delete=models.CASCADE
    )
    loses_to = models.ForeignKey(
        "GameMove",
        related_name="loses",
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Game(models.Model):
    player1 = models.ForeignKey(
        Player,
        related_name="player_1",
        on_delete=models.CASCADE
    )
    player2 = models.ForeignKey(
        Player,
        related_name="player_2",
        null=True,
        on_delete=models.CASCADE
    )
    slug = models.SlugField(null=True)
    current_round = models.IntegerField(default=0)
    winner = models.ForeignKey(
        Player,
        related_name="winner",
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    @staticmethod
    def generate_random_slug():
        return "".join(random.choices(string.ascii_lowercase, k=10))

    def __str__(self):
        return f"Game {self.id}: {self.player1} vs {self.player2}"



class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    player1_move = models.ForeignKey(
        GameMove,
        related_name="p1_move",
        on_delete=models.CASCADE
    )
    player2_move = models.ForeignKey(
        GameMove,
        related_name="p2_move",
        on_delete=models.CASCADE
    )
