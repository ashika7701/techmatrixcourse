from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

# -------------------------------
# Custom User Model
# -------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    # Store device tokens for OTP-free login on trusted devices
    trusted_devices = models.JSONField(default=list)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True
    )

    def __str__(self):
        return self.email or self.username


# -------------------------------
# Course Model
# -------------------------------
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="A comprehensive course.")
    image = models.ImageField(upload_to='course_images/', default='course_images/default.png')
    duration = models.CharField(max_length=100, default="Self-paced")
    level = models.CharField(max_length=50, default="Beginner")
    language = models.CharField(max_length=50, default="English")
    community_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# -------------------------------
# Lesson Model
# -------------------------------
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    youtube_video_id = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.order}. {self.title}"


# -------------------------------
# Enrollment Model
# -------------------------------
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=50, default="Enrolled")
    course_image = models.ImageField(upload_to='enrollment_images/', blank=True, null=True)

    final_exam_score = models.FloatField(default=0)
    final_exam_passed = models.BooleanField(default=False)

    # Payment fields
    payment_status = models.CharField(max_length=10, default="No")  # Yes / No
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    # Track enroll button metadata
    course_id_str = models.CharField(max_length=100, blank=True, null=True)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} enrolled in {self.course.name}"

    class Meta:
        unique_together = ('user', 'course')


# -------------------------------
# Profile Model
# -------------------------------
class Profile(models.Model):
    WORK_STATUS_CHOICES = [
        ('Student', 'Student'),
        ('Working', 'Working'),
        ('Housewife', 'Housewife'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='Student')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True, null=True)
    completion_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------------
# Course Payment Model
# -------------------------------
class CoursePayment(models.Model):
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} - ₹{self.amount}"
class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    status = models.CharField(max_length=20)
    notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
