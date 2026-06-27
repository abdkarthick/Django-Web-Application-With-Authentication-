from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    
    path('reset-password/', 
         auth_views.PasswordResetView.as_view(template_name='reset_password.html'), 
         name='reset_password'),
    
    path('reset-password-sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), 
         name='reset_password_sent'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_form.html'), 
         name='reset_password_confirm'),
    
    path('reset-password-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_done.html'), 
         name='reset_password_complete'),
]