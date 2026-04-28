from django.urls import path
from .views import CreateJob, BrowseJobs, JobDetails, EditJob, SearchJob

urlpatterns = [
    path('post-job/', CreateJob.as_view(), name='post-job-page'),
    path('browse-jobs/<int:page_no>/', BrowseJobs.as_view(), name='browse-jobs-page'),
    path('job-details/<uuid:job_id>', JobDetails.as_view(), name='job-details-page'),
    path('edit-job/<uuid:job_id>', EditJob.as_view(), name='edit-job-page'),
    path('search-jobs/<int:page_no>', SearchJob.as_view(), name='search-jobs'),
]