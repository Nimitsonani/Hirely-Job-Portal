from .models import Candidate, Company
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class LogInForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "example@gmail.com",
            "id": "email"
        })
    )

    password = forms.CharField(
        max_length=18,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password",
            "id": "password"
        })
    )


class RegisterCandidateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)

        if self.edit_mode:
            self.fields['email'].required = False
            self.fields['phone_no'].required = False
            self.fields['password'].required = False

    first_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First name",
        "id": "candidate-first-name"
    }))

    last_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last name",
        "id": "candidate-last-name"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email",
        "id": "candidate-email"
    }))

    phone_no = PhoneNumberField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your phone number",
        "id": "candidate-phone"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Create a password",
        "id": "candidate-password"
    }))

    class Meta:
        model = Candidate
        fields = [
            'username', 'job_title', 'bio', 'location', 'profile_picture', 
            'skills', 'experience_level', 'experience_description', 'resume', 
            'degree', 'college_name', 'university_name', 'field_of_study', 
            'projects', 'school_name', 'github_link', 'linkedin_link'
        ]
        
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username",
                "id": "candidate-username"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write a short bio...",
                "id": "candidate-bio",
                "rows": 4
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City, Country",
                "id": "candidate-location"
            }),
            "skills": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Python, Django, SQL",
                "id": "candidate-skills"
            }),
            "experience_level": forms.Select(attrs={
                "class": "form-control select",
                "id": "candidate-exp-level"
            }),
            "experience_description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe your experience...",
                "id": "candidate-exp-desc",
                "rows": 4
            }),
            "profile_picture": forms.FileInput(attrs={
                "class": "form-control",
                "id": "candidate-profile-pic"
            }),
            "resume": forms.FileInput(attrs={
                "class": "form-control",
                "id": "candidate-resume"
            }),
            "job_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Full-Stack Python Dev",
                "id": "candidate-job-title"
            }),
            "degree": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. B.Tech",
                "id": "candidate-degree"
            }),
            "field_of_study": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Computer Engineering",
                "id": "candidate-field"
            }),
            "college_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your college name",
                "id": "candidate-college"
            }),
            "university_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your university name",
                "id": "candidate-university"
            }),
            "school_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your school name",
                "id": "candidate-school"
            }),
            "projects": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe your projects...",
                "id": "candidate-projects",
                "rows": 4
            }),
            "github_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://github.com/yourusername",
                "id": "candidate-github"
            }),
            "linkedin_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://linkedin.com/in/yourusername",
                "id": "candidate-linkedin"
            }),
        }

class RegisterCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.edit_mode = kwargs.pop('edit_mode',False)
        super().__init__(*args, **kwargs)

        if self.edit_mode:
            self.fields['email'].required = False
            self.fields['phone_no'].required = False
            self.fields['password'].required = False


    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter company email",
        "id": "company-email"
    }))

    phone_no = PhoneNumberField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter phone number",
        "id": "company-phone"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Create a password",
        "id": "company-password"
    }))

    class Meta:
        model = Company
        fields = [
            'company_username',
            'company_display_name',
            'contact_email',
            'contact_mobile_no',
            'description',
            'website',
            'location',
            'profile_picture',
        ]
        widgets = {
            "company_username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username",
                "id": "company-username"
            }),
            "company_display_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your company name",
                "id": "company-name"
            }),
            "contact_email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Public contact email",
                "id": "company-contact-email"
            }),
            "contact_mobile_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Public contact phone (optional)",
                "id": "company-contact-phone"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe your company...",
                "id": "company-description"
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://yourcompany.com",
                "id": "company-website"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City, Country",
                "id": "company-location"
            }),
            "profile_picture": forms.FileInput(attrs={
                "class": "form-control",
                "id": "company-logo"
            }),
        }

class VerifyOTPForm(forms.Form):
    email_OTP = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control text-center otp-input",  # Added otp-input here
            "placeholder": "Enter Email OTP",
            "id": "email-otp",
            "maxlength": "6"
        })
    )
    
    phone_no_OTP = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control text-center otp-input",  # Added otp-input here
            "placeholder": "Enter Phone OTP",
            "id": "phone-otp",
            "maxlength": "6"
        })
    )

class ChangeCandidateUsernameForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new username'
            })
        }


class ChangeCompanyUsernameForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_username']
        widgets = {
            'company_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new company username'
            })
        }
