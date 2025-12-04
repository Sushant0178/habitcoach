from django import forms
from .models import Mood

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-select form-control-lg'}),
        }