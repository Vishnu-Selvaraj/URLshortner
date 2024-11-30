from django import forms
from .models import Urlshortner


class urlForm(forms.ModelForm):
    class Meta:
        model = Urlshortner
        fields = ['title','original_url']
