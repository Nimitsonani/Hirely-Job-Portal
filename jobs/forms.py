from .models import Job
from django import forms

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python Developer'
            }),

            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write job description...'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, remote, or hybrid job location.'
            }),

            'job_type': forms.Select(attrs={
                'class': 'form-control select'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control select'
            }),

            'min_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum salary'
            }),

            'max_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum salary'
            }),

            'application_deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'terminate_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
            'responsibilities': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'List job responsibilities...'
            }),

            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List job requirements...'
            }),

            'benefits': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List job benefits...'
            }),

            'vacancy': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of openings'
            }),

            'experience': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2-3 years'
            }),

            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Django, REST (comma separated)'
            }),

            'map_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paste Google Maps embed URL'
            }),
    }