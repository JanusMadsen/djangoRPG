from django.db import models
from django.contrib.auth.models import User
from RPG.functions import dice_roll


# Base Item model
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100,  default="Placeholder")
    Strength = models.IntegerField(default=10)
    Dexterity = models.IntegerField(default=10)
    AC = models.IntegerField(default=10)  # Armor Class
    HP = models.IntegerField(default=10)
    coins = models.IntegerField(default=10)
    is_in_combat = models.BooleanField(default=False)  # Track combat status
    
    # New fields for equipped items
    equipped_armor = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL, related_name='equipped_armor', limit_choices_to={'item_type': 'armor'})
    equipped_weapon = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL, related_name='equipped_weapon', limit_choices_to={'item_type': 'weapon'})

    def __str__(self):
        return f"{self.user.username}'s Character"

    def attack(self, target):
        # Basic attack logic
        dice_roll_value = dice_roll(20)
        if  dice_roll_value >= target.AC:  # Simulate dice roll
            damage_dealt = 2
            target.HP -= damage_dealt
            return (damage_dealt, dice_roll_value)
        return (0, dice_roll_value)  # Always return a tuple: (damage, dice_roll)

# Inventory model for managing player's items
class Inventory(models.Model):
    player = models.OneToOneField(player_model, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return f"{self.player.user.username}'s Inventory"

class Shop(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

class goblin(models.Model):
    name = models.CharField(max_length=100, default="goblin")

    HP = models.IntegerField(default=7)
    AC = models.IntegerField(default=15)
    Strength = models.IntegerField(default=8)
    Dexterity = models.IntegerField(default=14)

    def __str__(self):
        return self.name

    def attack(self, target):
        # Basic attack logic
        dice_roll_value = dice_roll(20)
        if  dice_roll_value >= target.AC:  # Simulate dice roll
            damage_dealt = 2
            target.HP -= damage_dealt
            return (damage_dealt, dice_roll_value)
        return (0, dice_roll_value)  # Always return a tuple: (damage, dice_roll)