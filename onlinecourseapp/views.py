import random
import hashlib
import razorpay

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm
from .models import Enrollment, Course

# ✅ Use custom user model
User = get_user_model()

# ✅ OTP temporary storage
otp_storage = {}

# ✅ Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# ---------------------- HOME & COURSE VIEWS ----------------------
def home(request):
    return render(request, 'home.html')


def course_view(request):
    course_type = request.GET.get('type', 'unknown')
    return render(request, 'course.html', {'course_type': course_type})


def course_page(request):
    return render(request, 'course0.html')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Course, Enrollment
import razorpay
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Course, Enrollment
from django.conf import settings
import razorpay

User = get_user_model()

# Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# ---------------------- COURSE IMAGE MAPPING ----------------------
COURSE_IMAGES = {
    "Data Science & AI": "images/data_science.jpeg",
    "Python & Django": "images/python.jpg",
    "Embedded Systems": "images/embedded.jpg",
    "C++ & Unreal Engine": "images/unreal_engine.jpg",
    # Add more courses as needed
}

# ---------------------- DASHBOARD / COURSE SHOWCASE ----------------------
@login_required
def dashboard_view(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    context = {
        "enrollments": enrollments,
        "course_images": COURSE_IMAGES
    }
    return render(request, "dashboard.html", context)


from django.shortcuts import render, redirect
from django.conf import settings
from .models import Course, Enrollment
from django.contrib.auth.models import User

# Assuming you have a Razorpay client object already: `client`
# And COURSE_IMAGES dict defined somewhere
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Course, Enrollment
from django.conf import settings
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


COURSE_IMAGES = {
    "Python & Django": "images/python_django.jpg",
    "Data Science & AI": "images/data_science.jpg",
    "C Embedded Systems": "images/c_embedded.jpg",
    "C++ & Unreal Engine": "images/unreal_engine.jpg",}
 
def enroll_view(request):
    course_id = request.GET.get("course_id")
    course_name = request.GET.get("course_name", "").strip()
    amount = request.GET.get("amount")

    if not course_name:
        return redirect('dashboard')

    course_image = COURSE_IMAGES.get(course_name, "images/default.png")

    # Already enrolled check
    if request.user.is_authenticated:
        course = Course.objects.filter(name=course_name).first()
        if course and Enrollment.objects.filter(user=request.user, course=course).exists():
            return render(request, 'enroll.html', {
                'error': '⚠️ You are already enrolled in this course!',
                'course_id': course_id,
                'course_name': course_name,
                'course_image': course_image,
                'amount': amount,
                'skip_password': True
            })

    if request.method == 'POST':

        # -------------------------------
        # LOGGED-IN USER
        # -------------------------------
        if request.user.is_authenticated:

            # ⭐ Correct Name (NO MORE Gmail stored)
            if request.user.first_name:
                name = request.user.first_name
            elif request.user.last_name:
                name = request.user.last_name
            else:
                name = request.user.username  # fallback

            # ⭐ Read phone from form so it wont become NULL
            phone = request.POST.get('phone') or "0000000000"

            status = request.POST.get('status', '').strip() or 'student'
            email = request.user.email
            password = None  # skip password creation

        # -------------------------------
        # NEW USER
        # -------------------------------
        else:
            name = request.POST.get('name', '').strip()
            status = request.POST.get('status', '').strip() or 'student'
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            # Validation
            if not (name and phone and email and password and confirm_password):
                return render(request, 'enroll.html', {
                    'error': '⚠️ All fields are required!',
                    'course_id': course_id,
                    'course_name': course_name,
                    'course_image': course_image,
                    'amount': amount
                })

            if password != confirm_password:
                return render(request, 'enroll.html', {
                    'error': '⚠️ Passwords do not match!',
                    'course_id': course_id,
                    'course_name': course_name,
                    'course_image': course_image,
                    'amount': amount
                })

            if User.objects.filter(email=email).exists():
                return render(request, 'enroll.html', {
                    'error': '⚠️ Email already registered! Please log in.',
                    'course_id': course_id,
                    'course_name': course_name,
                    'course_image': course_image,
                    'amount': amount
                })

        # -------------------------------
        # SAVE SESSION DATA
        # -------------------------------
        request.session['enrollment_data'] = {
            'name': name,
            'status': status,
            'phone': phone,
            'email': email,
            'password': password,
            'course_name': course_name,
            'course_image': course_image,
            'course_id': course_id,
            'amount': amount,
        }

        # Razorpay: convert amount to paise
        razorpay_amount = int(float(amount) * 100)

        payment = client.order.create({
            'amount': razorpay_amount,
            'currency': 'INR',
            'payment_capture': 1
        })

        return render(request, "payment.html", {
            "payment": payment,
            "key_id": settings.RAZORPAY_KEY_ID,
            "course_id": course_id,
            "course_name": course_name,
            "course_image": course_image,
            "amount": amount
        })

    # -------------------------------
    # GET Request
    # -------------------------------
    return render(request, 'enroll.html', {
        'course_id': course_id,
        'course_name': course_name,
        'course_image': course_image,
        'amount': amount,
        'skip_password': request.user.is_authenticated,
    })

def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        if not razorpay_payment_id:
            return render(request, 'payment_success.html', {
                'message': '⚠️ No payment info received.'
            })

        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)

            # Capture payment details
            payment = client.payment.fetch(razorpay_payment_id)

            if payment.get('status') == 'captured':
                enrollment_data = request.session.get('enrollment_data')

                if enrollment_data:

                    # Create OR get the user
                    user, created = User.objects.get_or_create(
                        email=enrollment_data['email'],
                        defaults={'username': enrollment_data['email']}
                    )

                    if created and enrollment_data.get('password'):
                        user.set_password(enrollment_data['password'])
                        user.save()

                    # Find or create course
                    course, _ = Course.objects.get_or_create(
                        name=enrollment_data['course_name'],
                        defaults={'image': enrollment_data['course_image']}
                    )

                    # If already enrolled
                    if Enrollment.objects.filter(user=user, course=course).exists():
                        request.session.pop('enrollment_data', None)
                        return render(request, 'payment_success.html', {
                            'message': '⚠️ You are already enrolled in this course.'
                        })

                    # Create Enrollment
                    enrollment = Enrollment.objects.create(
                        user=user,
                        course=course,
                        name=enrollment_data['name'],
                        status=enrollment_data['status'],
                        phone=enrollment_data['phone'],
                        email=enrollment_data['email'],
                        payment_status="Yes",
                        transaction_id=razorpay_payment_id
                    )

                    # ⭐ Add extra required values
                    enrollment.course_id_str = enrollment_data.get('course_id')
                    enrollment.course_name = enrollment_data.get('course_name')
                    enrollment.amount = enrollment_data.get('amount')
                    enrollment.save()

                    # Clear session
                    request.session.pop('enrollment_data', None)

                return render(request, 'payment_success.html', {
                    'message': f'✅ Payment Successful!<br>🧾 Transaction ID: {razorpay_payment_id}'
                })

            else:
                return render(request, 'payment_success.html', {
                    'message': '❌ Payment failed.'
                })

        except Exception as e:
            return render(request, 'payment_success.html', {
                'message': f'⚠️ Error verifying payment: {str(e)}'
            })

    return render(request, 'payment_success.html', {
        'message': '⚠️ Invalid request method.'
    })

# ---------------------- AUTHENTICATION ----------------------
def register(request):
    return render(request, "accounts/register.html")


def generate_hashed_otp():
    otp = random.randint(100000, 999999)
    hashed_otp = hashlib.sha256(str(otp).encode()).hexdigest()
    return otp, hashed_otp
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import hashlib

otp_storage = {}  # Make sure this is global or use cache
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
import resend

User = get_user_model()

# Temporary OTP storage (Keep your original dict)
otp_storage = {}

# -------------------------------
# Function to send OTP via RESEND
# -------------------------------
def send_otp_email(email, otp):
    try:
        resend.Emails.send(
            {
                "from": "TechMatrix <onboarding@resend.dev>",
                "to": email,
                "subject": "Your Login OTP",
                "html": f"<p>Your OTP is: <strong>{otp}</strong></p>",
            }
        )
    except Exception as e:
        print("Resend Email Error:", e)


# -------------------------------
# LOGIN VIEW (updated with Resend OTP)
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = authenticate(request, username=email, password=password)

        if user_obj:
            # 1. Device token read from cookie
            device_token = request.COOKIES.get('device_token')

            # 2. If trusted device → instant login
            if device_token and device_token in user_obj.trusted_devices:
                login(request, user_obj)
                messages.success(request, "Login successful!")
                return redirect('dashboard')

            # 3. New device → OTP verification
            otp, hashed_otp = generate_hashed_otp()
            otp_storage[email] = hashed_otp

            # Send OTP email using Resend
            send_otp_email(email, otp)

            request.session['pending_email'] = email
            return redirect('verify_otp')

        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


# -------------------------------
# VERIFY OTP
# -------------------------------
def verify_otp(request):
    email = request.session.get('pending_email')

    if not email:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if email in otp_storage:
            entered_hash = hashlib.sha256(str(entered_otp).encode()).hexdigest()

            if otp_storage[email] == entered_hash:
                # OTP OK → Login user
                user = get_object_or_404(User, email=email)
                login(request, user)

                # Create device token
                device_token = generate_device_token()

                # Add to trusted devices
                user.trusted_devices.append(device_token)
                user.save()

                # Clear session OTP
                request.session.pop('pending_email', None)
                otp_storage.pop(email, None)

                # Set device cookie
                response = redirect('dashboard')
                response.set_cookie(
                    'device_token',
                    device_token,
                    max_age=365 * 24 * 60 * 60,  # 1 year
                    httponly=True,
                    secure=True,   # IMPORTANT: Set True in production
                    samesite="None"
                )

                messages.success(request, "Login successful!")
                return response

            else:
                messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "OTP expired. Please login again.")
            return redirect('login')

    return render(request, 'verify_otp.html')


# -------------------------------
# RESEND OTP
# -------------------------------
def resend_otp(request):
    email = request.session.get('pending_email')

    if not email:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    try:
        otp, hashed_otp = generate_hashed_otp()
        otp_storage[email] = hashed_otp

        # Send resend OTP via Resend API
        send_otp_email(email, otp)

        messages.success(request, "OTP has been resent to your email.")

    except Exception as e:
        messages.error(request, f"Error resending OTP: {str(e)}")

    return redirect('verify_otp')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages

@login_required
def student_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        work_status = request.POST.get('work_status')
        profile_picture = request.FILES.get('profile_picture')

        if work_status:
            profile.work_status = work_status
        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')

    return render(request, 'student_profile.html', {'profile': profile})

from django.http import HttpResponse

@login_required
def download_certificate(request):
    # You can later replace this with a dynamically generated certificate PDF
    response = HttpResponse("Certificate download feature coming soon!", content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="certificate.txt"'
    return response

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Enrollment

# ---------------------- DASHBOARD ----------------------
# views.py or wherever you define COURSE_IMAGES
COURSE_IMAGES = {
    "Data Science & AI": "images/data_science.jpeg",
    "Python & Django": "images/python.jpg",
    "Embedded Systems": "images/embedded.jpg",
    "C++ & Unreal Engine": "images/unreal_engine.jpg",
    # Add more courses as needed
}

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy  # Use reverse_lazy instead of reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
import resend

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')  # ✅ use reverse_lazy
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = form.get_users(email)

        for user in users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = self.request.build_absolute_uri(
                reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            body = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            try:
                resend.emails.send(
                    from_email="TechMatrix <onboarding@resend.dev>",
                    to=[email],  # Must be a list
                    subject="Password Reset Request",
                    html=body
                )
            except Exception as e:
                # Log the error
                print("Resend API error:", e)
                form.add_error(None, "Failed to send reset email. Try again later.")
                return self.form_invalid(form)

        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')  # ✅ correct


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

# ---------------------- OTHER STATIC VIEWS ----------------------
def lesson_view(request, course_id): 
    # Optional: Retrieve the course object here if you need to use it
    # course = get_object_or_404(Course, id=course_id)
    
    # For now, just ensure it runs:
    return render(request, 'lesson_view.html', {'course_id': course_id})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Course  # adjust import according to your project

@login_required
def django(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    context = {
        'course': course,
        'user_name': request.user.get_full_name() or request.user.username,
    }
    
    return render(request, 'django.html', context)

def emc(request, course_id):
    return render(request, 'emc.html', {'course_id': course_id})
from django.contrib.auth.decorators import login_required
from .models import Enrollment, Course
# views.py
@login_required(login_url='/login/')
def emc_final_assessment(request):
    enrollment = Enrollment.objects.filter(user=request.user).first()
    if not enrollment:
        return redirect('dashboard')

    # If already passed, skip quiz and go straight to certificate
    if enrollment.final_exam_passed:
        return render(request, 'emcfinal_assessment.html', {'full_name': enrollment.name, 'passed': True})

    if request.method == 'POST':
        score = float(request.POST.get('score', 0))
        enrollment.final_exam_score = score
        if score >= 50:
            enrollment.final_exam_passed = True
        enrollment.save()

        return render(request, 'emcfinal_assessment.html', {
            'full_name': enrollment.name,
            'passed': enrollment.final_exam_passed,
            'score': score
        })

    return render(request, 'emcfinal_assessment.html', {'full_name': enrollment.name,"course_name": enrollment.course.name})
@login_required(login_url='/login/')
def ds_final_assessment(request):
    enrollment = Enrollment.objects.filter(user=request.user).first()
    if not enrollment:
        return redirect('dashboard')

    # Skip if already passed
    if enrollment.final_exam_passed:
        return render(request, 'dsfinal_assessment.html', {
            'full_name': enrollment.name,
            'passed': True
        })

    if request.method == 'POST':
        score = float(request.POST.get('score', 0))
        enrollment.final_exam_score = score

        if score >= 50:
            enrollment.final_exam_passed = True

        enrollment.save()

        return render(request, 'dsfinal_assessment.html', {
            'full_name': enrollment.name,
            'passed': enrollment.final_exam_passed,
            'score': score
        })

    return render(request, 'dsfinal_assessment.html', {
        'full_name': enrollment.name,
        "course_name": enrollment.course.name
    })

import uuid

def generate_device_token():
    return str(uuid.uuid4())

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required

@login_required
def course_redirect(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    name = course.name.lower().replace(" ", "").replace("&", "")

    if "datascienceai" in name:
        return render(request, "datascience.html", {"course": course})

    if "pythondjango" in name:
        return render(request, "django.html", {"course": course})

    if "embedded" in name:
        return render(request, "emc.html", {"course": course})

    if "unreal" in name:
        return render(request, "lesson_view.html", {"course": course})

    return redirect("dashboard")  # instead of default_course.html
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register


def register_details(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        status = request.POST.get("status")
        notify = request.POST.get("notify") == "Yes"

        UserDetails.objects.create(
            name=name,
            email=email,
            phone=phone,
            dob=dob,
            status=status,
            notify=notify
        )

        messages.success(request, "Your details have been submitted successfully!")
        return redirect("register_details")

    return render(request, "accounts/register.html")

def notices(request):
    return render(request, 'notices.html')