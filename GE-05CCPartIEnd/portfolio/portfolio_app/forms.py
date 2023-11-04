from django.forms import ModelForm
from .models import GolfRound, Notebook, Golfer
from django import forms

#create class for GolfRound form
class GolfRoundForm(ModelForm):
    class Meta:
        model = GolfRound
        fields = ('notebook', 'date', 'score')

#create class for Notebook form
class NotebookForm(ModelForm):
    class Meta:
        model = Notebook
        fields = ('golfer',)

class GolferForm(forms.ModelForm):
    class Meta:
        model = Golfer
        fields = ['name', 'email', 'gender']