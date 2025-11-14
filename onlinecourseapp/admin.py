# onlinecourseapp/admin.py

from django.contrib import admin
from .models import CustomUser, Enrollment

# Register your models here
admin.site.register(CustomUser)
admin.site.register(Enrollment)
from django.contrib import admin
from .models import Register

admin.site.register(Register)
