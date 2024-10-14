from django import forms
from .models import player_model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = player_model
        fields = ['Weight', 'Strength']  # List of fields that users can update
