from django import forms
from django.forms import ModelForm
from .models import Discarded

class DiscardedForm(ModelForm):
    class Meta:
        model = Discarded
        fields = '__all__'
