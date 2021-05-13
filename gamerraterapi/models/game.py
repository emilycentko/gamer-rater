from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_play_time = models.IntegerField()
    age_rec = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")
    