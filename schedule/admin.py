from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([Events, EventTime, Teachers, Groups, Courses, Rooms, Schedule])

