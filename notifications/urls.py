from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('/<int:page_no>', NotificationView.as_view(), name='notifications-page'),
]