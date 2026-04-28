from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from jobs.models import Job
from .tasks import send_email
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from accounts.forms import ChangeCandidateUsernameForm, ChangeCompanyUsernameForm

# Create your views here.

class HomePageView(View):
    def get(self, request):
        jobs = Job.objects.filter(status='live').order_by('created_at')[:8]
        return render(request, 'core/home.html', {'jobs':jobs})
        
class ContactUs(View):
    def get(self, request):
        return render(request, 'core/contact_us.html')
    
    def post(self,request):
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone')
        message = request.POST.get('message')
        if name and subject and email and phone_no and message:
            message_body = f"""
                            You have received a new message from your website contact form.

                            --- Sender Details ---
                            Name: {name}
                            Email: {email}
                            Phone: {phone_no}

                            --- Subject ---
                            {subject}

                            --- Message ---
                            {message}
                            """
            send_email.delay(message_body)
            return redirect('home-page')
        return HttpResponse('Fill all teh Details.')



class Settings(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.user_type == 'candidate':
            form = ChangeCandidateUsernameForm()
            current_username = user.candidate.username
        else:
            form = ChangeCompanyUsernameForm()
            current_username = user.company.company_username
        return render(request, 'core/settings.html', {'form':form, 'current_username':current_username})
    
    def post(self, request):
        user = request.user
        if user.user_type == 'candidate':
            form = ChangeCandidateUsernameForm(request.POST, instance=request.user.candidate)
            current_username = user.candidate.username
        else:
            form = ChangeCompanyUsernameForm(request.POST, instance=request.user.company)
            current_username = user.company.company_username

        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.add_error(None,'Username is Already Taken.')
            else:
                return redirect('home-page')
        return render(request, 'core/settings.html', {'form':form, 'current_username':current_username})


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/settings.html',{'change_password':True})
    
    def post(self, request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                return redirect('home-page')
            return render(request, 'core/settings.html',{'change_password':True,
                                                        'error':'Wrong Password'})
        return render(request, 'core/settings.html',{'change_password':True,
                                                        'error':'Both Passwords Do not Match.'})