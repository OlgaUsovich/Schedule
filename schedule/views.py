import calendar
import datetime

from django.shortcuts import render

# Create your views here.
from .models import Schedule


def display_schedule(request):
    schedule_lines = Schedule.objects.all()
    return render(request, 'schedule/schedule_form.html', {'schedule_lines': schedule_lines})


def show_calendar(request):
    today = datetime.date.today()
    days = calendar.Calendar(firstweekday=0).itermonthdates(today.year, today.month)
    return render(request, 'schedule/calender.html', locals())


def week_schedule(request):
    schedule_lines = Schedule.objects.all()
    days = range(1, 8)
    return render(request, 'schedule/week_schedule.html', locals())
