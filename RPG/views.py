from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .models import player_model, Item, Inventory, goblin
from .forms import ProfileForm, RegistrationForm

def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def main_page(request):
    # Get the player's profile data from the player_model
    try:
        profile = player_model.objects.get(user=request.user)
    except player_model.DoesNotExist:
        return redirect('index')  # Redirect if no profile is found
    
    # Pass the profile data to the template
    context = {
        'player_model': profile
    }
    return render(request, 'main.html', context)

def loginpage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/main/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logoutpage(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('/main/')

@login_required(login_url='/login/')
def update_profile(request):
    profile = player_model.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main')  # Redirect to a success page or the profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def inventory_view(request):
    character = get_object_or_404(player_model, user=request.user)

 # Check if the inventory exists, if not create it
    inventory, created = Inventory.objects.get_or_create(player=character)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = get_object_or_404(Item, id=item_id)

        print(f"Trying to equip item: {item.name} (ID: {item.id}, Type: {item.item_type})")

        # Equip or unequip the item
        if action == 'equip':
            if item.is_armor():
                character.equipped_armor = item
            elif item.is_weapon():
                character.equipped_weapon = item
            character.save()

        elif action == 'unequip':
            if item.is_armor() and character.equipped_armor == item:
                character.equipped_armor = None
            elif item.is_weapon() and character.equipped_weapon == item:
                character.equipped_weapon = None
            character.save()

        return redirect('inventory')

    return render(request, 'inventory.html', {'inventory': character.inventory, 'character': character})

#Shop
def shop(request):
    player = request.user.player_model  # Get the player's model
    inventory = player.inventory  # Get the player's inventory

    # Get all items in the shop
    all_items = Item.objects.all()

    # Items the player can buy (not in their inventory)
    items_to_buy = all_items.exclude(id__in=inventory.items.all())

    # Items the player can sell (items they own)
    items_to_sell = []
    for item in inventory.items.all():
        item.sell_price = item.price // 2  # Calculate sell price
        items_to_sell.append(item)

    return render(request, 'shop.html', {
        'items_to_buy': items_to_buy,
        'items_to_sell': items_to_sell,
        'player': player,
    })

def purchase_item(request, item_id):
    player = get_object_or_404(player_model, user=request.user)
    item = Item.objects.get(id=item_id)
    if player.coins >= item.price:  # Check if the player has enough coins
        player.coins -= item.price  # Deduct the price from player's coins
        player.inventory.items.add(item)  # Add the item to the player's inventory
        player.save()
        return redirect('shop')  # Redirect to shop after purchase
    else:
        return render(request, 'shop.html', {'items': Item.objects.all(), 'error': 'Not enough coins!'})

def sell_item(request, item_id):
    player = get_object_or_404(player_model, user=request.user)
    item = Item.objects.get(id=item_id)

    # Check if the item is equipped and unequip it
    if player.equipped_armor == item:
        player.equipped_armor = None
    elif player.equipped_weapon == item:
        player.equipped_weapon = None

    # Save the player after unequipping
    player.save()

    if request.method == 'POST':
        # Check if the item is in the player's inventory
        if player.inventory.items.filter(id=item.id).exists():
            # Assuming the item has a 'price' attribute for selling
            player.coins += item.price // 2  # Give half the price back (or whatever logic you want)
            player.save()  # Save the player's coins
            player.inventory.items.remove(item)  # Remove the item from inventory
            return redirect('shop')  # Redirect back to shop or another page
        else:
            return render(request, 'shop.html', {'error': 'You do not have this item in your inventory.'})
    return render(request, 'sell_item.html', {'item': item})

def signuppage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            p1 = player_model(user=user)
            p1.save()
            login(request, user)
            return redirect('/main/')
    else:
        form = RegistrationForm()
    return render(request, "signup.html", {"form": form})

def start_battle(request):
    player = player_model.objects.get(user=request.user)  # Get the player's character
    monster = goblin.objects.order_by('?').first()  # Randomly select a monster for the fight

    # Initialize the battle state in the session
    request.session['battle'] = {
        'player_id': player.id,
        'monster_id': monster.id,
        'player_hp': player.HP,
        'monster_hp': monster.HP,
        'monster_name': monster.name,
        'player_turn': True  # Player always starts first
    }

    return redirect('battle')  # Redirect to the battle page

def battle_simulator(request):
    # Retrieve battle info from the session
    battle_state = request.session.get('battle')
    if not battle_state:
        return redirect('start_battle')  # No battle in session, start a new one

    player = get_object_or_404(player_model, pk=battle_state['player_id'])
    monster = get_object_or_404(goblin, pk=battle_state['monster_id'])

    # Initial setup for variables
    player_diceroll = None
    player_damage = None
    monster_diceroll = None
    monster_damage = None
    message = ""

    # Ensure player HP and monster HP are initialized in battle_state
    if 'player_hp' not in battle_state:
        battle_state['player_hp'] = player.HP
    if 'monster_hp' not in battle_state:
        battle_state['monster_hp'] = monster.HP

    if request.method == "POST":
        action = request.POST.get('action')

        # Player's attack turn
        if action == "attack" and battle_state['player_turn']:
            player_damage, player_diceroll = player.attack(monster)
            battle_state['monster_hp'] -= player_damage
            message = f"You dealt {player_damage} damage to {monster.name}!"

            # Check if the monster is defeated
            if battle_state['monster_hp'] <= 0:
                message += f" You defeated {monster.name}!"
                battle_state['player_turn'] = False  # End the player's turn
                del request.session['battle']  # End the battle      
            else:
                battle_state['player_turn'] = False  # Monster's turn

        # Monster's attack turn
        if not battle_state['player_turn'] and 'monster_hp' in battle_state and battle_state['monster_hp'] > 0:
            monster_damage, monster_diceroll = monster.attack(player)
            battle_state['player_hp'] -= monster_damage
            message += f" {monster.name} dealt {monster_damage} damage to you! {monster_diceroll}"

            # Check if the player is defeated
            if battle_state['player_hp'] <= 0:
                message += " You were defeated!"
                del request.session['battle']  # End the battle
            else:
                battle_state['player_turn'] = True  # Player's turn again

        # Update the session with the new state
        request.session['battle'] = battle_state

    context = {
        'player': player,
        'monster': monster,
        'player_hp': battle_state['player_hp'],  # Use the HP stored in the session
        'monster_hp': battle_state['monster_hp'],  # Use the HP stored in the session
        'player_diceroll': player_diceroll,
        'player_damage': player_damage,
        'monster_diceroll': monster_diceroll,
        'monster_damage': monster_damage,
        'message': message,
        'player_turn': battle_state['player_turn']  # Use the player's turn status from the session
    }

    return render(request, "battle.html", context)
