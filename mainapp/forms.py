from django import forms
from .models import *

class ShortenerForm(forms.ModelForm):
    
    url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Your URL to shorten"}))
    
    class Meta:
        model = shortcut
        fields = ('url',)