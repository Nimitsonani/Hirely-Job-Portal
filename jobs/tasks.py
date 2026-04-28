from celery import shared_task
from .models import Job
import datetime
from notifications.task import send_notification
from notifications.models import Notification

@shared_task
def terminate_jobs():
    now = datetime.datetime.now()
    all_jobs = Job.objects.filter(status='applications_closed',
                                    terminate_at__lt=now)
    for job in all_jobs:
        job.status = 'closed'
        job.terminated = True
        job.save()

        Notification.objects.create(
                user = job.company.user,
                title = 'Job Expired',
                message = f'Your Job for {job.title} Expired.',
            )

        all_applications = job.application_set.all()
        for i in all_applications:
            i.status = 'rejected'
            i.rejection_reason = 'Job Closed'
            i.save()
            title = 'Application Status Update'
            message = (
                f'Your application for "{job.title}" at '
                f'{job.company.company_display_name} has been rejected '
                f'because the position is now closed.'
            )
            Notification.objects.create(
                user = i.candidate.user,
                title = title,
                message = message,
            )
            send_notification.delay(user_email = i.candidate.user.email ,title = title, message = message)

@shared_task
def close_applications():
    now = datetime.datetime.now()
    all_jobs = Job.objects.filter(status='live',
                                    application_deadline__lt=now)
    for job in all_jobs:
        job.status = 'applications_closed'
        job.applications_closed = True
        job.save()

        title = 'Applications Closed'
        message = (
            f'The application period for your job posting "{job.title}" '
            f'has ended.'
        )

        Notification.objects.create(
                user = job.company.user,
                title = title,
                message = message,
            )

        send_notification.delay(user_email = job.company.user.email ,title = title, message = message)