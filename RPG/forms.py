from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import player_model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = player_model
        fields = ['name', 'Strength', 'HP']  # List of fields that users can update


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='*Required')
    username = forms.CharField(help_text='*Required')


    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user