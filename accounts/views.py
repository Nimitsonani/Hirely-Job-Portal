from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User, Candidate, Company
from .forms import RegisterCandidateForm, RegisterCompanyForm, LogInForm, VerifyOTPForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from jobs.models import Job
from django.core.cache import cache
import math
from random import randint
from accounts.task import send_email_otp, send_sms, delete_user
from django_redis import get_redis_connection
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse


class Login(View):
    def get(self, request):
        form = LogInForm()
        return render(request, 'accounts/login.html', {'login_form': form})

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                if user.user_type == 'candidate' and user.candidate.is_verified:
                    login(request, user)
                    return redirect('home-page')
                elif user.user_type == 'company' and user.company.otp_verified:
                    login(request, user)
                    return redirect('home-page')

        form.add_error(None, 'Invalid Login Credentials.')
        return render(request, 'accounts/login.html', {
            'login_form': form
        })


class Register(View):
    def get(self, request):
        form = RegisterCandidateForm()
        return render(
            request,
            "accounts/register.html",
            {"form": form, "not_company": True},
        )

    def post(self, request):
        form = RegisterCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate_data = form.save(commit=False)
            try:
                user = User.objects.create_user(phone_no=form.cleaned_data['phone_no'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                username = form.cleaned_data['email'],
                                                user_type='candidate',
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'])
            except Exception as e:
                if 'phone_no' in str(e):
                    form.add_error('phone_no','This Phone Number is Already Registered with another Account.')
                elif 'username' in str(e):
                    form.add_error('email','This Email is Already Registered with another Account.')
                else:
                    form.add_error(None,e)
            else:
                candidate_data.user = user
                candidate_data.save()
                email = form.cleaned_data['email']
                phone_no = str(form.cleaned_data['phone_no'])
                request.session['email'] = email
                request.session['phone_no'] = phone_no
                OTP_email = randint(100001,999999)
                OTP_phone = randint(100001,999999)
                cache.set(f'{email}_OTP',OTP_email, timeout=180)
                cache.set(f'{phone_no}_OTP',OTP_phone, timeout=180)
                cache.set(f'{email}_OTP_resend','anything', timeout=45)
                send_email_otp.delay(OTP_email, email)
                send_sms.delay(OTP_phone, phone_no)
                delete_user.apply_async(args=[email, phone_no], countdown=180)
                return HttpResponseRedirect(reverse("verify-otp-page"))

        return render(
            request,
            "accounts/register.html",
            {"form": form, "not_company": True},
        )


class RegisterCompany(View):
    def get(self, request):
        form = RegisterCompanyForm()
        return render(
            request,
            "accounts/register.html",
            {"form": form, "not_company": False},
        )

    def post(self, request):
        form = RegisterCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company_data = form.save(commit=False)
            try:
                user = User.objects.create_user(phone_no=form.cleaned_data['phone_no'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                username = form.cleaned_data['email'],
                                                user_type='company')
            except Exception as e:
                if 'phone_no' in str(e):
                    form.add_error('phone_no','This Phone Number is Already Registered with another Account.')
                elif 'username' in str(e):
                    form.add_error('email','This Email is Already Registered with another Account.')
                else:
                    form.add_error(None,e)
            else:
                company_data.user = user
                company_data.save()
                email = form.cleaned_data['email']
                phone_no = str(form.cleaned_data['phone_no'])
                request.session['email'] = email
                request.session['phone_no'] = phone_no
                OTP_email = randint(100001,999999)
                OTP_phone = randint(100001,999999)
                cache.set(f'{email}_OTP',OTP_email, timeout=180)
                cache.set(f'{phone_no}_OTP',OTP_phone, timeout=180)
                cache.set(f'{email}_OTP_resend','anything', timeout=45)
                send_email_otp.delay(OTP_email,email)
                send_sms.delay(OTP_phone, phone_no)
                delete_user.apply_async(args=[email, phone_no], countdown=180)
                return redirect('verify-otp-page')

        return render(
            request,
            "accounts/register.html",
            {"form": form, "not_company": False},
        )

class BrowseCandidates(View):
    def get(self, request, page_no):
        total_pages = math.ceil(Candidate.objects.count()/12)
        end = page_no * 12
        start = end - 12

        location_filter = request.GET.get('location')
        exp_filter = request.GET.get('exp')

        if location_filter and exp_filter:
            candidates = Candidate.objects.all().filter(location = location_filter,experience_level = exp_filter).order_by('-user__created_at')[start:end]
        elif location_filter:
            candidates = Candidate.objects.all().filter(location = location_filter).order_by('-user__created_at')[start:end]
        elif exp_filter:
            candidates = Candidate.objects.all().filter(experience_level = exp_filter).order_by('-user__created_at')[start:end]
        else:
            candidates = Candidate.objects.all().order_by('-user__created_at')[start:end]
        
        for candidate in candidates:
            if candidate.skills:
                candidate.skills = candidate.skills.split(',')
        return render(request, 'browse_candidates.html',
                        {'candidates':candidates,
                        'total_pages':total_pages,
                        'page_range':range(1,total_pages+1),
                        'page_no':page_no})


class BrowseCompanies(View):
    def get(self, request, page_no):
        total_pages = math.ceil(Company.objects.count()/12)
        end = page_no * 12
        start = end - 12
        location_filter = request.GET.get('location')

        if location_filter:
            companies = Company.objects.filter(is_verified=True).filter(location=location_filter).order_by('-user__created_at')[start:end]
        else:
            companies = Company.objects.filter(is_verified=True).order_by('-user__created_at')[start:end]
        for company in companies:
            company.no_of_jobs = Job.objects.filter(company=company).count()
        return render(request, 'browse_companies.html',
                        {'companies':companies,
                        'total_pages':total_pages,
                        'page_range':range(1,total_pages+1),
                        'page_no':page_no})


class EditCandidateProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        candidate = get_object_or_404(Candidate, username= user.candidate.username)
        if user:
            form = RegisterCandidateForm(instance=candidate,
                                            initial={
                                                'first_name':user.first_name,
                                                'last_name': user.last_name,
                                            })
            return render(
                request,
                "accounts/register.html",
            {"form": form, "not_company": True, 'edit_profile':True, 'user':user},
        )
    
    def post(self, request):
        user = request.user
        candidate = get_object_or_404(Candidate, username= user.candidate.username)
        if user:
            form = RegisterCandidateForm(request.POST, request.FILES, edit_mode=True, instance=candidate)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                form.save()
                return redirect('candidate-dashboard-profile')
            return render(request,"accounts/register.html",
                            {"form": form, 
                            "not_company": True, 
                            'edit_profile':True, 
                            'user':user})

class EditCompanyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        company = get_object_or_404(Company, company_username = user.company.company_username)
        if user:
            form = RegisterCompanyForm(instance=company)
            return render(
                request,
                "accounts/register.html",
            {"form": form, "not_company": False, 'edit_profile':True, 'user':user},
        )
    
    def post(self, request):
        user = request.user
        company = get_object_or_404(Company, company_username = user.company.company_username)
        if user:
            form = RegisterCompanyForm(request.POST, request.FILES, edit_mode=True, instance=company)
            if form.is_valid():
                form.save()
                return redirect('company-dashboard-profile')
            return render(request,"accounts/register.html",
                            {"form": form, 
                            "not_company": False, 
                            'edit_profile':True, 
                            'user':user})
                

class VerifyOTP(View):
    def get(self, request):
        form = VerifyOTPForm()
        redis_conn = get_redis_connection("default")
        email = request.session.get('email')
        email_otp_key = cache.make_key(f'{email}_OTP')
        email_otp_resend_key = cache.make_key(f'{email}_OTP_resend')
        ttl = redis_conn.ttl(email_otp_key)
        ttl_resend = redis_conn.ttl(email_otp_resend_key)
        return render(request, 'verify_otp.html', {'form':form, 'ttl':ttl, 'ttl_resend':ttl_resend})
    
    def post(self, request):
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            email = request.session.get('email')
            phone_no = request.session.get('phone_no')
            email_otp = cache.get(f'{email}_OTP')
            phone_no_otp = cache.get(f'{phone_no}_OTP')
            if int(form.cleaned_data['email_OTP']) == email_otp and int(form.cleaned_data['phone_no_OTP']) == phone_no_otp:
                user = get_object_or_404(User, email=email, phone_no=phone_no)
                if user.user_type == 'candidate':
                    user.candidate.is_verified = True
                    user.candidate.save()
                else:
                    user.company.otp_verified = True
                    user.company.save()
                return redirect('login-page')
            form.add_error(None, 'Invalid OTP.')
        return render(request, 'verify_otp.html', {'form':form})
            

class ResendOTP(View):
    def get(self, request):
        email = request.session.get('email')
        phone_no = request.session.get('phone_no')

        redis_conn = get_redis_connection("default")
        email_otp_key = cache.make_key(f'{email}_OTP')
        ttl = redis_conn.ttl(email_otp_key)
        ttl_resend = cache.get(f'{email}_OTP_resend')
        print(ttl_resend)
        if ttl<180 and not ttl_resend:
            OTP_email = randint(100001,999999)
            OTP_phone = randint(100001,999999)
            cache.set(f'{email}_OTP',OTP_email, timeout=120)
            cache.set(f'{phone_no}_OTP',OTP_phone, timeout=120)
            cache.set(f'{email}_OTP_resend','anything', timeout=45)
            
            send_email_otp.delay(OTP_email,email)
            send_sms.delay(OTP_phone, phone_no)
            return redirect('verify-otp-page')
        return HttpResponse('Your OTP Expired.')


class SearchCompany(View):
    def get(self, request, page_no):
        query = request.GET.get('query')
        result = Company.objects.annotate(
            search = SearchVector('company_display_name','location')
        ).filter(search=query, is_verified=True, otp_verified=True).order_by('-search')
        end = page_no * 12
        start = end - 12
        companies = result[start: end]
        total_pages = math.ceil(len(result)/12)
        return render(request, 'browse_companies.html',
                        {'companies':companies,
                        'total_pages':total_pages,
                        'page_range':range(1,total_pages+1),
                        'page_no':page_no,
                        'query':query})

class SearchCandidate(View):
    def get(self, request, page_no):
        query = request.GET.get('query')
        result = Candidate.objects.annotate(
            search = SearchVector('username','job_title','user__first_name','user__last_name','skills','location')
        ).filter(search=query, is_verified=True).order_by('-search')
        total_pages = math.ceil(len(result)/12)
        end = page_no * 12
        start = end - 12
        candidates = result[start:end]
        for candidate in candidates:
            if candidate.skills:
                candidate.skills = candidate.skills.split(',')
        return render(request, 'browse_candidates.html',
                        {'candidates':candidates,
                        'total_pages':total_pages,
                        'page_range':range(1,total_pages+1),
                        'page_no':page_no,
                        'query':query})