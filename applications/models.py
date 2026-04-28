from django.db import models
import uuid

# Create your models here.
STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('shortlisted', 'ShortListed'),
    ('rejected', 'Rejected'),
    ('interview_scheduled', 'Interview Scheduled'),
    ('interviewed', 'Interviewed'),
    ('offered', 'Offered')
]

INTERVIEW_STATUS_CHOICE = [
    ('pending','Pending'),
    ('accept', 'Accept'),
    ('reject','Reject'),
]

class Application(models.Model):
    application_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    candidate = models.ForeignKey('accounts.Candidate', on_delete=models.CASCADE, editable=False)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, editable=False)
    cover_letter = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    rejection_reason = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_note = models.TextField(max_length=300, null=True, blank=True)
    interview_response_status = models.CharField(max_length=10, choices=INTERVIEW_STATUS_CHOICE, null=True, blank=True)