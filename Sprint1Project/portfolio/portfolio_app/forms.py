from django.forms import ModelForm
from .models import GolfRound, Notebook, Golfer
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# create class for GolfRound form
class GolfRoundForm(ModelForm):
    class Meta:
        model = GolfRound
        fields = ('notebook', 'date', 'score')

# create class for Notebook form
class NotebookForm(ModelForm):
    class Meta:
        model = Notebook
        fields = ('golfer', 'image','video')

class GolferForm(forms.ModelForm):
    class Meta:
        model = Golfer
        fields = [ 'gender']  # email field removed in accordance with model change

# create UserRegisterForm extending UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Optional: Customize to add email field in form

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

# create UserLoginForm extending AuthenticationForm
class UserLoginForm(AuthenticationForm):
    pass  
