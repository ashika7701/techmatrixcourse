from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from onlinecourseapp import views
from django.contrib.auth import views as auth_views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

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

    # ✅ Password Reset using Custom Views
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Dashboard & Enrollment
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('enroll/', views.enroll_view, name='enroll'),

    # Courses & Lessons
    path('course/', views.course_view, name='course'),
    path('lesson/<int:course_id>/', views.lesson_view, name='lesson_view'),
    path('django/<int:course_id>/', views.django, name='django'),
    path('emc/<int:course_id>/', views.emc, name='emc'),
    path('course/<int:course_id>/', views.course_redirect, name='course_redirect'),

    # Payment
    path('course0/', views.course_page, name='course0'),
    path('payment_success/', views.payment_success, name='payment_success'),

    # Notices
    path('notices/', views.notices, name='notices'),
    path('emcfinal_assessment/', views.emc_final_assessment, name='emc_final_assessment'),
    path('dsfinal_assessment/', views.ds_final_assessment, name='ds_final_assessment'),
]

# ✅ Static + Media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
