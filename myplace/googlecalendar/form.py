from django import forms
from .models import Calendar

class PostForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ('date','title', 'location', 'attendee', 'response')