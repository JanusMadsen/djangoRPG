from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .models import player_model, Item, Inventory
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