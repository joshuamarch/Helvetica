from django import forms
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput()
    )
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class NewPlayerForm(forms.Form):
    player_name = forms.CharField(label='player_name', max_length=200)
    
    def clean_player_name(self):
        player_name = self.cleaned_data['player_name']
        if not re.search(r'^\w+$', player_name):
            raise forms.ValidationError('Player name can only contain alphanumeric characters and the underscore.')
        else:
            return player_name

class GameForm(forms.Form):
    
    prompt = forms.CharField(label='prompt', max_length=200)
    
    def clean_prompt(self):
        prompt = self.cleaned_data['prompt']
        # should add some checking here
        return prompt
    
    
    
    
    
    