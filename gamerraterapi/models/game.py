from django.db import models
from .review import Review

class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_play_time = models.IntegerField()
    age_rec = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Review.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating