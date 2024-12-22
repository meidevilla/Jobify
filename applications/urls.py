from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.register_user, name='signup'), 
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.applications, name='applications'),
    path('applications/edit_application/<int:pk>/', views.edit_application, name='edit_application'),
    path('applications/delete_application/<int:pk>/', views.delete_application, name='delete_application'),
    path('reminders/', views.reminders, name='reminders'),
    path('calendar/', views.calendar, name='calendar'),
    path('settings/', views.settings, name='settings'),
    path('settings/edit_profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
