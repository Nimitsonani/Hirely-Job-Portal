from django import forms
from applications.models import Application

class InterViewForm(forms.ModelForm):
    interview_date = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    interview_note = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Add meeting link, Meeting Address, agenda, or instructions...'
        })
    )

    class Meta:
        model = Application
        fields = ['interview_date','interview_note']