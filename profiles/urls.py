from django.urls import path
from .views import CandidatePublicProfile, CompanyPublicProfile

urlpatterns = [
    path('<slug:username>/',CandidatePublicProfile.as_view(), name='candidate-public-profile-page'),
    path('company/<slug:username>/',CompanyPublicProfile.as_view(), name='company-public-profile-page'),
]