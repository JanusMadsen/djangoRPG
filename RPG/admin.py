from django.contrib import admin

from .models import player_model, Item, Inventory, goblin



# Register your models here.

admin.site.register(player_model)
admin.site.register(goblin)
admin.site.register(Item)
admin.site.register(Inventory)