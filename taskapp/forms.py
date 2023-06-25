from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your task'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
        }