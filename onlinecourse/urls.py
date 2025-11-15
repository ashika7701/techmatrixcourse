from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from onlinecourseapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('profile/', views.student_profile, name='student_profile'),
    path('download_certificate/', views.download_certificate, name='download_certificate'),

    path('login/', views.login_view, name='login'),
   # path('verify-otp/', views.verify_otp, name='verify_otp'),
   # path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('enroll/', views.enroll_view, name='enroll'),

    path('course/', views.course_view, name='course'),
    path('lesson/<int:course_id>/', views.lesson_view, name='lesson_view'),
    path('django/<int:course_id>/', views.django_course, name='django_course'),
    path('emc/<int:course_id>/', views.emc, name='emc'),
    path('course/<int:course_id>/', views.course_redirect, name='course_redirect'),

    path('course0/', views.course_page, name='course0'),
    path('payment_success/', views.payment_success, name='payment_success'),

    path('notices/', views.notices, name='notices'),
    path('emcfinal_assessment/', views.emc_final_assessment, name='emc_final_assessment'),
    path('dsfinal_assessment/', views.ds_final_assessment, name='ds_final_assessment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
