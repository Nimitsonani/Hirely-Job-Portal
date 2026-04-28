from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateJobForm
from django.http import HttpResponse
from jobs.models import Job
import math
from applications.models import Application
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from django.http import HttpResponseRedirect

# Create your views here.
class CreateJob(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.user_type == 'company' and request.user.company.is_verified:
            form = CreateJobForm()
            return render(request, 'jobs/post_job.html', {'form':form})
        return HttpResponse("Non Company Users and Unverified Company can't Post Jobs.", status=403)

    def post(self, request):
        if request.user.user_type == 'company' and request.user.company.is_verified:
            form = CreateJobForm(request.POST)
            if form.is_valid():
                new_job_data = form.save(commit=False)
                new_job_data.company = request.user.company
                new_job_data.save()
                return redirect('company-dashboard-manage-jobs',1)
            return render(request, 'jobs/post_job.html', {'form':form})
        return HttpResponse("Non Company Users and Unverified Company can't Post Jobs.", status=403)


class BrowseJobs(View):
    def get(self, request, page_no):
        ending_no_of_job = page_no * 8
        starting_no_of_job = ending_no_of_job - 8
        current_page_jobs = Job.objects.filter(status='live').order_by('-created_at')[starting_no_of_job : ending_no_of_job]
        no_of_pages = math.ceil((Job.objects.filter(status='live').count())/8)
        return render(request, 'jobs/browse_jobs.html', {'page_range':range(1,no_of_pages+1),
                                                            'jobs':current_page_jobs,
                                                            'page_no':page_no,
                                                            'no_of_pages':no_of_pages})

class JobDetails(LoginRequiredMixin, View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, job_id=job_id)
        user = request.user
        if user.user_type == 'candidate':
            if len(Application.objects.filter(candidate=user.candidate,job=job)) < 1:
                return render(request, 'jobs/job_details.html',
                                {'job':job,
                                'already_applied':False})
            return render(request, 'jobs/job_details.html',
                                {'job':job,
                                'already_applied':True})
        else:
            return render(request, 'jobs/job_details.html',
                                {'job':job,
                                'company':True})

    def post(self,request, job_id):
        user = request.user
        if user:
            if user.user_type=='candidate':
                if user.candidate.resume:
                    job = get_object_or_404(Job, job_id=job_id)
                    if len(Application.objects.filter(candidate=user.candidate,job=job)) < 1:
                        if job.status == 'live':
                            Application.objects.create(candidate=user.candidate, job=job)
                            return redirect('browse-jobs-page',page_no=1)
                        return HttpResponse('You Cant Apply for this job.')
                    return HttpResponse('You have Already Applied for this job.')
                return HttpResponse('Upload Your Resume First from Accounts --> Profiles --> Edit Profile', status=403)
            return HttpResponse('Only Candidates can Apply.', status=403)
        return HttpResponse('Login First.', status=401)


class EditJob(LoginRequiredMixin, View):
    def get(self, request, job_id):
        user = request.user
        if user.user_type == 'company' and user.company.is_verified:
            job = get_object_or_404(Job, job_id=job_id, company = user.company)
            form = CreateJobForm(instance=job)
            return render(request, 'jobs/post_job.html', {'form':form,
                                                            'job_id':job.job_id,
                                                            'edit_job':True})
        return HttpResponse('Not allowed', status=403)
    
    def post(self, request, job_id):
        user = request.user
        if user.user_type == 'company' and user.company.is_verified:
            job = get_object_or_404(Job, job_id=job_id, company = user.company)
            form = CreateJobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                return redirect('company-dashboard-manage-jobs',1)
            return render(request, 'jobs/post_job.html', {'form': form,
                                                            'job_id': job.job_id,
                                                            'edit_job': True
                                                        })
        return HttpResponse('Not allowed', status=403)

class SearchJob(View):
    def get(self, request, page_no):
        ending_no_of_job = page_no * 8
        starting_no_of_job = ending_no_of_job - 8
        
        # query = SearchQuery(request.GET.get('query'),search_type='websearch')


        # vector = (
        #     SearchVector('title',weight='A')*4+
        #     SearchVector('company__company_display_name',weight='A')+
        #     SearchVector('skills', weight='B')+
        #     SearchVector('location', weight='B')+
        #     SearchVector('job_type',weight='B')
        # )
        # result = Job.objects.annotate(
        #     rank = SearchRank(vector, query)
        # ).filter(rank__gt=0.00000000000001).order_by('-rank')
        # for job in result:
        #     print(job.title, job.rank)
        keyword = request.GET.get('keyword')
        location = request.GET.get('location')

        if keyword and location:
            result = Job.objects.annotate(
                keyword_search = SearchVector('title', 'job_description', 'company__company_display_name', 'job_type', 'requirements', 'skills'),
                location_search = SearchVector('location')
            ).filter(keyword_search = keyword,
                    location_search = location).order_by('-keyword_search')

            query = f'{keyword},{location}'

        else:
            query = request.GET.get('query')
            result = Job.objects.annotate(
                search = SearchVector('title', 'job_description', 'company__company_display_name', 'location', 'job_type', 'requirements', 'skills')
            ).filter(search=query).order_by('-search')

        jobs = result[starting_no_of_job : ending_no_of_job]
        no_of_pages = math.ceil(len(result)/8)
        return render(request, 'jobs/browse_jobs.html', {'jobs':jobs,
                                                            'page_range':range(1, no_of_pages+1),
                                                            'page_no':page_no,
                                                            'no_of_pages':no_of_pages,
                                                            'query':query,
                                                            'keyword':keyword,
                                                            'location':location})