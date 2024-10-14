from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import player_model
from .forms import ProfileForm

@login_required
def update_profile(request):
    profile = player_model.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page or the profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def detail(request, player_model):
    return HttpResponse("You're looking at question %s." % player_model)