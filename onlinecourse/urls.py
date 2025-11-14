from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from onlinecourseapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', views.home, name='home'),
    path('profile/', views.student_profile, name='student_profile'),
    path('download_certificate/', views.download_certificate, name='download_certificate'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url='/reset/done/'  # <-- Add this line
        ),
        name='password_reset_confirm'
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # Dashboard & Enrollment
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('enroll/', views.enroll_view, name='enroll'),

    # Courses & Lessons
    path('course/', views.course_view, name='course'),
    path('lesson/<int:course_id>/', views.lesson_view, name='lesson_view'),
    path('django/<int:course_id>/', views.django, name='django'),
    path('emc/<int:course_id>/', views.emc, name='emc'),
    path("course/<int:course_id>/", views.course_redirect, name="course_redirect"),

    # Payment
    path('course0/', views.course_page, name='course0'),
    path('payment_success/', views.payment_success, name='payment_success'),

    # Notices
    path('notices/', views.notices, name='notices'),
    path('emcfinal_assessment/', views.emc_final_assessment, name='emc_final_assessment'),
path('dsfinal_assessment/', views.ds_final_assessment, name='ds_final_assessment'),
    # Password Reset URLs
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
         name="reset_password"),

    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
         name="password_reset_complete"),
]

# ✅ Static + Media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
