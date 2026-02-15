from django import forms
from .models import Event, Participant, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 '
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),

        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
