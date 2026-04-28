from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from jobs.models import Job
from applications.models import Application
from django.http import HttpResponse
import math
from .forms import InterViewForm
from notifications.task import send_notification
from django.urls import reverse

# Create your views here.
def get_context(job, form, form_is_valid):
    interview_form = form
    all_applications = Application.objects.filter(job=job).order_by('-applied_at')
    total_applicants = all_applications.count()
    pending_applications = all_applications.filter(status='applied')
    rejected_applications = all_applications.filter(status='rejected')
    shortlisted_applications = all_applications.filter(status='shortlisted')
    interview_scheduled_applications = all_applications.filter(status='interview_scheduled')
    interviewed_applications = all_applications.filter(status='interviewed')
    offered_applications = all_applications.filter(status='offered')
    return {"job":job,
            'form_is_valid':form_is_valid,
            "total_applicants":total_applicants,
            'all_applications':all_applications,
            'pending_applications':pending_applications,
            'rejected_applications':rejected_applications,
            'shortlisted_applications':shortlisted_applications,
            'interview_scheduled_applications':interview_scheduled_applications,
            'interviewed_applications':interviewed_applications,
            'offered_applications':offered_applications,
            'interview_form':interview_form,}

def get_title_and_message(status, company_name, job_title, rejection_reason=None, interview_time=None, interview_notes=None):
    
    if status == 'rejected' and rejection_reason:
        title = 'Application Update'
        message = (
            f'Your application for "{job_title}" at {company_name} has been rejected. '
            f'Reason: {rejection_reason}.'
        )

    elif status == 'interview_scheduled':
        title = 'Interview Scheduled'
        message = (
            f'Your application for "{job_title}" at {company_name} has been shortlisted. '
            f'Interview Date & Time: {interview_time}. '
        )
        if interview_notes:
            message += f'Notes from the company: {interview_notes}.'

    else:
        title = 'Application Update'
        message = (
            f'Your application for "{job_title}" at {company_name} is now marked as "{status}".'
        )

    return title, message

class ManageApplications(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user and user.user_type == 'candidate':
            all_applications = Application.objects.filter(candidate=user.candidate).order_by('-applied_at')
            return render(request, 'dashboards/candidate_dashboard.html',
                        {'user':user,
                        'all_applications':all_applications,
                        'manage_applications':True})


class CandidateProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user and user.user_type == 'candidate':
            skills_list = user.candidate.skills.split(',')
            return render(request, 'dashboards/candidate_dashboard.html',
                            {'candidate_profile':True,
                            'skills_list':skills_list})


class CompanyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user and user.user_type == 'company':
            return render(request, 'dashboards/company_dashboard.html',
                            {'company_profile':True})

class ManageJobs(LoginRequiredMixin, View):
    def get(self, request, page_no):
        user = request.user
        if user and user.user_type == 'company':
            total_jobs = Job.objects.filter(company=user.company).count()
            total_pages = math.ceil(total_jobs/6)
            
            end_idnex = page_no * 6
            start_index = end_idnex - 6
            jobs = Job.objects.filter(company=user.company).order_by('-created_at')[start_index : end_idnex]
            return render(request, 'dashboards/company_dashboard.html',
                            {'total_jobs':total_jobs,
                            'no_of_pages':total_pages,
                            'jobs':jobs,
                            'manage_jobs':True,
                            'page_no':page_no,
                            'page_range':range(1,total_pages+1)})
        return HttpResponse('Not Allowed', status=401)

class JobApplications(LoginRequiredMixin, View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, job_id=job_id)
        user = request.user
        if user:
            if job.company == user.company:
                interview_form = InterViewForm()
                context = get_context(job, interview_form, True)
                return render(request, 'dashboards/job_applications.html',
                                context)
            return HttpResponse('You are not allowed to view this job.', status=403)
        return HttpResponse('Login Required', status=401)
    
    def post(self, request, job_id):
        job = get_object_or_404(Job, job_id=job_id)
        user = request.user
        if user:
            if job.company == user.company:
                application = get_object_or_404(Application, application_id=request.POST['application_id'])
                updated_status = request.POST.get('updated_status')
                if updated_status:
                    rejection_reason = request.POST.get('rejection_reason')
                    
                    if updated_status=='rejected' and rejection_reason and application.status in ['applied','shortlisted','interview_scheduled','interviewed']:
                        application.status = updated_status
                        application.rejection_reason = rejection_reason
                    elif application.status=='applied' and updated_status in ['shortlisted','rejected','interview_scheduled','offered']:
                        application.status = updated_status
                    elif application.status=='shortlisted' and updated_status in ['rejected','interview_scheduled','offered']:
                        application.status = updated_status
                    elif application.status=='interview_scheduled' and updated_status in ['rejected','interviewed','offered']:
                        application.status = updated_status
                    elif application.status=='interviewed' and updated_status in ['rejected','offered']:
                        application.status = updated_status
                    else:
                        return HttpResponse('This status Change is not Allowed.', status=403)
                    application.save()
                    if application.rejection_reason:
                        title,message = get_title_and_message(updated_status, user.company.company_display_name, job.title, application.rejection_reason)
                    else:
                        title,message = get_title_and_message(updated_status, user.company.company_display_name, job.title)
                    send_notification.delay(user_email = application.candidate.user.email ,title = title, message = message)
                    url = reverse('dashboard-job-applications',kwargs={'job_id':job_id})
                    return redirect(f'{url}?tab={request.GET.get("tab")}')
                elif not updated_status:
                    form = InterViewForm(request.POST)
                    if form.is_valid():
                        application.interview_date = form.cleaned_data.get('interview_date')
                        application.interview_note = form.cleaned_data.get('interview_note')
                        application.status = 'interview_scheduled'
                        application.save()
                        if application.interview_note:
                            title,message = get_title_and_message('interview_scheduled', user.company.company_display_name, job.title, None, application.interview_date, application.interview_note)
                        else:
                            title,message = get_title_and_message('interview_scheduled', user.company.company_display_name, job.title, None, application.interview_date, None)
                        send_notification.delay(user_email = application.candidate.user.email ,title = title, message = message)
                        url = reverse('dashboard-job-applications',kwargs={'job_id':job_id})
                        return redirect(f'{url}?tab={request.GET.get("tab")}')
                    context = get_context(job, form, False)
                    return render(request, 'dashboards/job_applications.html',
                                context)
                return HttpResponse('Status not allowed.', status=403)
            return HttpResponse('You are not allowed to view this job.', status=403)
        return HttpResponse('Login Required', status=401)

class RejectAll(LoginRequiredMixin, View):
    def post(self, request, status_to_reject, job_id):
        user = request.user
        job = get_object_or_404(Job, job_id=job_id)
        rejection_reason = request.POST.get('rejection_reason')

        if user:
            if job.company == user.company:
                if status_to_reject in ['applied','shortlisted','interviewed','interview_scheduled']:
                    
                    print('hi')
                    all_applications = Application.objects.filter(
                        job=job, status=status_to_reject,
                    )
                    if rejection_reason:
                        title,message = get_title_and_message('rejected', user.company.company_display_name, job.title, rejection_reason, None, None)
                        for application in all_applications:
                            application.status = 'rejected'
                            application.rejection_reason = rejection_reason
                            application.save()
                            send_notification.delay(user_email = application.candidate.user.email ,title = title, message = message)
                    else:
                        title,message = get_title_and_message('rejected', user.company.company_display_name, job.title, None, None, None)
                        for application in all_applications:
                            application.status = 'rejected'
                            application.save()
                            send_notification.delay(user_email = application.candidate.user.email ,title = title, message = message)
                
                    url = reverse('dashboard-job-applications',kwargs={'job_id':job_id})
                    return redirect(f'{url}?tab={request.GET.get("tab")}')
        return HttpResponse('Not Allowed', status=403)