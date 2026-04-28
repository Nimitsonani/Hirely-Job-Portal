from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home-page'),
    path('contact/',views.ContactUs.as_view(),name='contact-us-page'),
    path('settings/',views.Settings.as_view(),name='settings-page'),
    path('settings/change-password',views.ChangePassword.as_view(),name='change-password-page'),
]