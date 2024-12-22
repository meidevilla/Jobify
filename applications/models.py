from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.utils import timezone
from django.utils.timezone import now


class JobApplication(models.Model):
    STATUS_CHOICES = [('Applied', 'Applied'), ('Interviewing', 'Interviewing'), ('Offer Received', 'Offer Received'), ('Rejected', 'Rejected'),]
    WORK_SETUP_CHOICES = [('Full FTF', 'Full FTF'), ('Hybrid', 'Hybrid'), ('Remote', 'Remote')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    work_setup = models.CharField(max_length=50, choices=WORK_SETUP_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    date_applied = models.DateField(default=timezone.now)
    interview_schedule = models.DateTimeField(blank=True, null=True)
    job_posting_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    @classmethod
    def applications_this_week(cls, user):
        start_of_week = date.today() - timedelta(days=date.today().weekday())
        return cls.objects.filter(user=user, date_applied__gte=start_of_week).count()

    @classmethod
    def weekly_progress(cls, user, target=20):
        applications_count = cls.applications_this_week(user)
        progress_percentage = (applications_count / target) * 100
        return applications_count, progress_percentage

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg')
    current_streak = models.PositiveIntegerField(default=0)
    last_application_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def update_streak(self):
        today = timezone.now().date()
        if self.last_application_date is None:
            self.current_streak = 1
        elif self.last_application_date == today - timedelta(days=1):
            self.current_streak += 1
        elif self.last_application_date < today - timedelta(days=1):
            self.current_streak = 0
        self.last_application_date = today
        self.save()

class Reminders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    reminder_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



