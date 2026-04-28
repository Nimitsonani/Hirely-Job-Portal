from django.urls import path
from .views import ManageApplications, ManageJobs, JobApplications, CompanyProfile, CandidateProfile, RejectAll


urlpatterns = [
    path('manage-applications/', ManageApplications.as_view(), name='dashboard-page'),
    path('profile/', CandidateProfile.as_view(), name='candidate-dashboard-profile'),
    path('company/manage-jobs/<int:page_no>', ManageJobs.as_view(), name='company-dashboard-manage-jobs'),
    path('company/profile/', CompanyProfile.as_view(), name='company-dashboard-profile'),
    path('company/job-applications/<uuid:job_id>', JobApplications.as_view(), name='dashboard-job-applications'),
    path('company/job-applications/reject-all/<str:status_to_reject>/<uuid:job_id>', RejectAll.as_view(), name='reject-all'),
]