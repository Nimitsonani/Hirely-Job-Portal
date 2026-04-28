from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',views.Login.as_view(), name='login-page'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('verify-otp/',views.VerifyOTP.as_view(), name='verify-otp-page'),
    path('resend-otp/',views.ResendOTP.as_view(), name='resend-otp'),
    path('register/',views.Register.as_view(), name='register-page'),
    path('register-company/',views.RegisterCompany.as_view(), name='register-company-page'),
    path('browse-candidates/<int:page_no>',views.BrowseCandidates.as_view(), name='browse-candidates-page'),
    path('browse-companies/<int:page_no>',views.BrowseCompanies.as_view(), name='browse-companies-page'),
    path('edit-candidate-profile/',views.EditCandidateProfile.as_view(), name='edit-candidate-profile-page'),
    path('edit-company-profile/',views.EditCompanyProfile.as_view(), name='edit-company-profile-page'),
    path('search-companies/<int:page_no>', views.SearchCompany.as_view(), name='search-companies'),
    path('search-candidates/<int:page_no>', views.SearchCandidate.as_view(), name='search-candidates'),
]