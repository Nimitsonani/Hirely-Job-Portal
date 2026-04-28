from django.db import models
from datetime import timedelta, timezone, datetime
import uuid

# Create your models here.
STATUS_CHOICES = [
    ('live','Live'),
    ('applications_closed','Applications Closed'),
    ('closed', 'Closed')
]
JOB_TYPE_CHOICES = [
    ('full-time','Full Time'),
    ('part-time','Part Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ('office', 'Office'),
]

CATEGORY_CHOICES = [
    ('frontend', 'Frontend Developer'),
    ('backend', 'Backend Developer'),
    ('fullstack', 'Full Stack Developer'),
    ('mobile_android', 'Android Developer'),
    ('mobile_ios', 'iOS Developer'),
    ('mobile_cross', 'Cross Platform Developer'),
    ('data_science', 'Data Scientist'),
    ('data_analyst', 'Data Analyst'),
    ('ml_engineer', 'Machine Learning Engineer'),
    ('ai_engineer', 'AI Engineer'),
    ('devops', 'DevOps Engineer'),
    ('cloud', 'Cloud Engineer'),
    ('sre', 'Site Reliability Engineer'),
    ('cybersecurity', 'Cybersecurity Specialist'),
    ('network', 'Network Engineer'),
    ('database', 'Database Administrator'),
    ('bigdata', 'Big Data Engineer'),
    ('uiux', 'UI/UX Designer'),
    ('product_designer', 'Product Designer'),
    ('qa_manual', 'QA Engineer (Manual)'),
    ('qa_automation', 'QA Engineer (Automation)'),
    ('embedded', 'Embedded Systems Engineer'),
    ('iot', 'IoT Developer'),
    ('game_dev', 'Game Developer'),
    ('ar_vr', 'AR/VR Developer'),
    ('blockchain', 'Blockchain Developer'),
    ('web3', 'Web3 Developer'),
    ('system_admin', 'System Administrator'),
    ('it_support', 'IT Support Engineer'),
    ('erp', 'ERP/CRM Developer'),
    ('sap', 'SAP Consultant'),
    ('technical_writer', 'Technical Writer'),
    ('business_analyst', 'Business Analyst'),
    ('project_manager', 'Project Manager'),
    ('product_manager', 'Product Manager'),
    ('other', 'Other'),
]

def default_job_expiry():
    return (datetime.now(timezone.utc) + timedelta(days=40)).date()

def default_deadline():
    return (datetime.now(timezone.utc) + timedelta(days=30)).date()

class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=120)
    job_description = models.TextField()
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, editable=False)
    location = models.CharField(max_length=20)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    application_deadline = models.DateField(default = default_deadline, blank=True)
    applications_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    terminate_at = models.DateField(default = default_job_expiry, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    terminated = models.BooleanField(default=False, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, editable=False, default='live')
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    vacancy = models.IntegerField(default=1)
    experience = models.CharField(max_length=400, blank=True)
    skills = models.CharField(max_length=300, blank=True)
    map_url = models.URLField(blank=True)