from django.shortcuts import render, get_object_or_404
from django.views import View
from accounts.models import Candidate, Company

# Create your views here.
class CandidatePublicProfile(View):
    def get(self, request, username):
        candidate = get_object_or_404(Candidate,username=username)
        candidate.skills = candidate.skills.split(',')
        return render(request, 'profiles/candidate_public_profile.html',
                                {'candidate':candidate})


class CompanyPublicProfile(View):
    def get(self, request, username):
        company = get_object_or_404(Company,company_username=username)
        all_jobs = company.job_set.all().order_by('-created_at')
        live_jobs = company.job_set.filter(status='live').order_by('-created_at')
        application_closed_jobs = company.job_set.filter(status='applications_closed').order_by('-created_at')
        closed_jobs = company.job_set.filter(status='closed').order_by('-created_at')
        return render(request, 'profiles/company_public_profile.html',
                                {'company':company,
                                'all_jobs':all_jobs,
                                'live_jobs':live_jobs,
                                'application_closed_jobs':application_closed_jobs,
                                'closed_jobs':closed_jobs})