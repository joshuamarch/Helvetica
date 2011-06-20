from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    player_name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    inventory = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    last_location = models.CharField(max_length=100)
    luck = models.IntegerField()
    strength = models.IntegerField()
    constitution = models.IntegerField()
    speed = models.IntegerField()
    health = models.IntegerField()
    alive = models.BooleanField()
    achievements = models.CharField(max_length=1000)
    
    def __str__(self):
        return '%s from %s' % (self.player_name, self.user)
    
    def add_item(self, item):
        inventory = self.inventory
        listinventory = inventory.split()
        listinventory.append(item)
        stringinventory = " ".join(listinventory)
        self.inventory = stringinventory
    
    def add_achievement(self, achievement):
        achievements = self.achievements
        listachievements = achievements.split()
        listachievements.append(achievement)
        stringachievements = " ".join(listachievements)
        self.achievements = stringachievements
    
    def death(self):
        self.alive = False
        # write a check of this in the main game view
        

# add method to add health which only allows it up to total health!



