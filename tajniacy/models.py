from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Game(models.Model):
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20)

class Word(models.Model):
    uses = models.IntegerField(default=0)
    word = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.word

class Card(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    visible = models.BooleanField(default=False)
    status = models.CharField(max_length=10)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ManyToManyField(User, related_name="players")
    leader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)





