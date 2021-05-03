import calendar
import datetime

from django.shortcuts import render

# Create your views here.
from .models import Schedule, EventTime


def display_schedule(request):
    schedule_lines = Schedule.objects.all()
    return render(request, 'schedule/schedule_form.html', {'schedule_lines': schedule_lines})


def show_calendar(request):
    today = datetime.date.today()
    days = calendar.Calendar(firstweekday=0).itermonthdates(today.year, today.month)
    return render(request, 'schedule/calender.html', locals())


def week_schedule(request):
    schedule_lines = Schedule.objects.all()
    times = EventTime.objects.filter(id__in=schedule_lines.values_list('event_time', flat=True))
    time_dict = {str(time): {k: schedule_lines.filter(event_time=time, event_date__iso_week_day=k) for k in range(1, 8)}
                 for time in times}
    return render(request, 'schedule/week_schedule.html', locals())
