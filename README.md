# Hirely – Django Job Portal

A Django-based job portal that focuses on real backend systems like task scheduling, async processing, OTP verification, application workflows, and rate limiting.

---

## 🚀 Live Demo

https://your-live-link.onrender.com/

---

## 🛠 Tech Stack

### Backend
- Django
- PostgreSQL
- Celery
- Redis

### Frontend
- Django Templates
- HTML / CSS / JavaScript

### External Services
- Twilio (SMS)
- SMTP (Email)

---

## ⚡ Core Features

### 🔹 Scheduled Tasks (Celery Beat)
- Runs automatically every 24 hours
- Handles job lifecycle:
  - Closes applications after the deadline (no new applications allowed)
  - Later marks the job as closed and updates remaining applications
- Keeps the system consistent without manual work

---

### 🔹 Async Processing (Celery + Redis)
- Handles tasks in the background:
  - Sending emails
  - Sending OTPs
  - Updating application status
- Keeps the app fast and responsive

---

### 🔹 Rate Limiting Middleware (Redis)
- Custom middleware using Redis
- Limits how many requests a user can make
- Prevents spam and abuse
- Works using time windows

---

### 🔹 Search & Filtering
- Full-text search (FTS) using PostgreSQL
- Website supports filtering for better job discovery

---

### 🔹 OTP Verification
- Email OTP (SMTP)
- SMS OTP (Twilio)
- OTP expires after some time
- Unverified users are removed automatically

---

### 🔹 Notifications
- Sent when:
  - Application status changes
  - Interview is scheduled
  - Job is closed
- Processed in background using Celery

---

### 🔹 Job & Application Flow
- Application stages:
  - Applied → Shortlisted → Interview → Offered / Rejected
- Separate stages for:
  - Application deadline (stop applying)
  - Final job closure (after interviews)
- Prevents duplicate applications
- Supports bulk actions

---

### 🔹 Dashboards
- Candidate dashboard:
  - View applications and status

- Company dashboard:
  - Manage jobs and applicants
  - Update application status

---

## 📸 Screenshots

### Homepage
![Homepage](https://github.com/user-attachments/assets/2e375234-2c7b-4587-83a8-047833e2d485)

### Browse Jobs
![Browse Jobs](https://github.com/user-attachments/assets/a074bc9d-b9ee-4d2f-bbe1-174fa24bda3a)

### Job Details
![Job Details](https://github.com/user-attachments/assets/137a9208-2d47-4adc-b105-29cf76915f65)

### Candidate Dashboard
![Candidate Dashboard](https://github.com/user-attachments/assets/1310be09-f76b-4397-81f4-47467125edde)

### Company Dashboard
![Company Dashboard](https://github.com/user-attachments/assets/18c5a9f4-0720-4bef-9a22-af5cdb553d37)

### Job Applications (Company View)
![Job Applications](https://github.com/user-attachments/assets/7c78fc13-4568-4816-9a55-358511b33ff6)

---

## 🧠 How It Works

### Application Flow

1. Candidate applies to a job  
2. Application is saved  
3. Company updates status  
4. Notification task runs  
5. Candidate gets update  

---

### Background Task Flow

1. Action triggers a task  
2. Task goes to Redis queue  
3. Celery processes it  
4. Email/SMS is sent  

---

### Scheduled Task Flow

1. Runs every 24 hours  
2. Closes applications after deadline  
3. Later closes the job and updates applications  

---

## ⚙️ Setup

### Install dependencies
```bash
pip install -r requirements.txt
```
### Start Server
```bash
python manage.py runserver
```

### Start Celery Worker
```bash
celery -A Hirely worker -l info --pool=solo
```

### Start Celery Beat
```bash
celery -A Hirely beat -l info
```
