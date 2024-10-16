from django.db import models
from django.contrib.auth.models import User
from random import randint


# Base Item model
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=50, choices=[
        ('armor', 'Armor'),
        ('weapon', 'Weapon'),
        ('potion', 'Potion'),
        # Add more item types here
    ])
    defense = models.IntegerField(null=True, blank=True)  # Optional defense stat
    attack = models.IntegerField(null=True, blank=True)   # Optional attack stat

    def __str__(self):
        return self.name
    
        # Method to check if an item is armor
    def is_armor(self):
        return self.item_type == 'armor'

    # Method to check if an item is a weapon
    def is_weapon(self):
        return self.item_type == 'weapon'
    
# The main player model
class player_model(models.Model):
    Strength = models.IntegerField(default=0)
    Weight = models.IntegerField(default=0)
    AC = models.IntegerField(default=10)  # Armor Class
    HP = models.IntegerField(default=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    
    # New fields for equipped items
    equipped_armor = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL, related_name='equipped_armor', limit_choices_to={'item_type': 'armor'})
    equipped_weapon = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL, related_name='equipped_weapon', limit_choices_to={'item_type': 'weapon'})

    def __str__(self):
        return f"{self.user.username}'s Character"

# Inventory model for managing player's items
class Inventory(models.Model):
    player = models.OneToOneField(player_model, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return f"{self.player.user.username}'s Inventory"

class goblin(models.Model):
    Strengthlvl = models.IntegerField(default=8)
    HP = models.IntegerField(default=7)
    AC = models.IntegerField(default=15)
