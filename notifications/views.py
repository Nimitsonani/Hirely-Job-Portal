from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
from django.http import HttpResponse
import math

# Create your views here.
class NotificationView(LoginRequiredMixin, View):
    def get(self, request, page_no):
        user = request.user
        if user:
            end = page_no * 20
            notifications = Notification.objects.filter(
                user = user
            ).order_by('-created_at')[: end]

            notifications_count = Notification.objects.filter(
                user = user
            ).order_by('-created_at').count()
            no_of_loadmore = math.ceil(notifications_count/20)

            if no_of_loadmore >= page_no:
                response = render(request, 'notifications/notification_page.html',
                                            {'notifications':notifications,
                                            'page_no':page_no,
                                            'no_of_loadmore':no_of_loadmore})
                for i in notifications:
                    if not i.is_read:
                        i.is_read = True
                        i.save()
                return response
            return render(request, 'notifications/notification_page.html',
                                            {'notifications':notifications,
                                            'page_no':page_no,
                                            'no_of_loadmore':no_of_loadmore})
        return HttpResponse('Not Allowed', status=403)