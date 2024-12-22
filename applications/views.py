from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication, UserProfile, Reminders
from .forms import JobApplicationForm, RegisterForm, LoginForm, RemindersForm, UserProfileForm, UserChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash

def landing_page(request):
    return render(request, 'landing_page.html')

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='login') 
    else:
        form = RegisterForm() 
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the username and password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(3600 * 24 * 30)  # 30 days
                else:
                    request.session.set_expiry(0)
                # messages.success(request, 'Successfully logged in!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'registration/login.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm() 
    return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('landing_page') 

@login_required
def dashboard(request):
    applications = JobApplication.objects.filter(user=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    current_streak = user_profile.current_streak

    total_applications = applications.count()
    applied_applications = applications.filter(status="Applied").count()
    total_interviews = applications.filter(status="Interviewing").count()
    applications_in_progress = applications.filter(status__in=["Applied", "Interviewing"]).count()
    total_offers = applications.filter(status="Offer Received").count()
    total_rejections = applications.filter(status="Rejected").count()
    form = JobApplicationForm()

    start_of_week = date.today() - timedelta(days=date.today().weekday())
    applications_this_week = applications.filter(date_applied__gte=start_of_week)
    applications_submitted = applications_this_week.count()
    progress_percentage = (applications_submitted / 20) * 100
    progress_percentage = int(progress_percentage)

    monthly_applications = (
        applications.annotate(month=ExtractMonth('date_applied'), year=ExtractYear('date_applied')).values('month', 'year').annotate(total=Count('id')).order_by('year', 'month'))
    labels = [datetime(year=data['year'], month=data['month'], day=1).strftime("%B %Y") for data in monthly_applications]
    totals = [data['total'] for data in monthly_applications]

    upcoming_interviews = applications.filter(interview_schedule__gte=timezone.now()).order_by('interview_schedule')[:3]
    reminders = Reminders.objects.filter(user=request.user)
    response_received = applications.filter(status__in=["Interviewing", "Offer Received", "Rejected"]).count()
    if total_applications > 0:
        response_rate = round((response_received / total_applications) * 100, 2)
    else:
        response_received = 0
        response_rate = 0
    context = {
        'total_applications': total_applications,
        'applied_applications': applied_applications,
        'total_interviews': total_interviews,
        'applications_in_progress': applications_in_progress,
        'total_offers': total_offers,
        'total_rejections': total_rejections,
        'form': form,
        'applications_submitted': applications_submitted,
        'progress_percentage': progress_percentage,
        'target': 20,
        'monthly_applications' : monthly_applications,
        'labels': labels,
        'totals': totals,
        'no_data': len(labels) == 0,
        'upcoming_interviews' : upcoming_interviews,
        'current_streak': current_streak,
        'response_received' : response_received,
        'response_rate' : response_rate,
        'reminders' : reminders,
    }
    return render(request, 'dashboard.html', context)

def applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    
    if search_query:
        applications = applications.filter(company_name__icontains=search_query) | applications.filter(position__icontains=search_query)
    all_applications = applications.all()
    
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.update_streak()
            return redirect('applications')
    else:
        form = JobApplicationForm()

    context = {
        'all_applications': all_applications,
        'form': form,
        'search_query': search_query,
    }
    return render(request, 'applications.html', context)

def edit_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('applications')
    else:
        form = JobApplicationForm(instance=application)
    return render(request, 'applications.html', {'form': form, 'application': application})

def delete_application (request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        application.delete()
        return redirect('applications')
    return render(request, 'applications.html', {'application': application})

def reminders(request):
    reminders = Reminders.objects.filter(user=request.user)
    if request.method == "POST":
        form = RemindersForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, "Reminder added successfully!")
            return redirect('dashboard')
    else:
        form = RemindersForm()
    context = {
        'reminders': reminders,
        'form': form,
    }
    return render(request, 'dashboard.html', context)

def calendar(request):
    # Get the current user's job applications and reminders
    user = request.user
    job_applications = JobApplication.objects.filter(user=user).exclude(interview_schedule__isnull=True)
    reminders = Reminders.objects.filter(user=user)

    # Prepare data to pass to the template
    interview_data = []
    for job in job_applications:
        interview_data.append({
            'title': f"Interview for {job.position} at {job.company_name}",
            'start': job.interview_schedule.strftime('%Y-%m-%dT%H:%M:%S'),  # Proper format
            'end': (job.interview_schedule + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),  # Assuming interview lasts 1 hour
            'description': job.location,
        })

    reminder_data = []
    for reminder in reminders:
        reminder_data.append({
            'title': reminder.title,
            'start': reminder.reminder_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Proper format
            'end': (reminder.reminder_time + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),  # Assuming reminder lasts 1 hour
            'description': reminder.description,
        })

    # Combine both interview and reminder data for the calendar
    events = interview_data + reminder_data

    return render(request, 'calendar.html', {'events': events})

def settings(request):
    
    return render(request, 'settings.html')

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        form2 = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()  # Save profile changes (avatar, etc.)
        else:
            print("UserProfileForm Errors:", form.errors)  # Debugging form errors

        if form2.is_valid():
            form2.save()  # Save user details (first_name, last_name, etc.)
        else:
            print("UserChangeForm Errors:", form2.errors)  # Debugging form errors

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('settings')
    else:
        form = UserProfileForm(instance=user_profile)
        form2 = UserChangeForm(instance=request.user)

    context = {
        "form": form,
        "form2": form2,
    }
    return render(request, 'settings.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep user logged in
            messages.success(request, "Your password has been successfully changed!")
            return redirect('settings')  # Redirect to settings page or any other desired page
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'settings.html', {'form': form})
    
@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        user = request.user
        user.delete()
        # Log the user out after deletion
        logout(request)
        # # Redirect to a page confirming account deletion
        # return redirect('account_deleted')
    # If not a POST request, show a confirmation page (Optional)
    return render(request, 'delete_account_confirm.html')
