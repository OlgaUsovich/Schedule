import calendar
import datetime

from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import TeacherFilter
from .models import Schedule, EventTime


def display_schedule(request):
    schedule_lines = Schedule.objects.all()
    return render(request, 'schedule/schedule_form.html', {'schedule_lines': schedule_lines})


def show_calendar(request):
    today = datetime.date.today()
    days = list(calendar.Calendar(firstweekday=0).itermonthdates(today.year, today.month))
    schedule_dates = [i[0] for i in list(Schedule.objects.values_list('event_date'))]
    return render(request, 'schedule/calender.html', locals())


def week_schedule(request):
    form = TeacherFilter(request.GET)
    today = datetime.datetime.today()
    week_num = request.GET.get('week', default=today.isocalendar()[1])
    d = f'{today.year}-{week_num}'
    dates_of_week = [datetime.datetime.strptime(f'{d}-{i}', '%G-%V-%u').date() for i in range(1, 8)]
    schedule_lines = Schedule.objects.filter(event_date__in=dates_of_week)

    if form.is_valid():
        schedule_lines = schedule_lines.filter(**{k: v for k, v in form.cleaned_data.items() if v})

    times = EventTime.objects.filter(id__in=schedule_lines.values_list('event_time', flat=True))
    time_dict = {str(time): {k: schedule_lines.filter(event_time=time, event_date__iso_week_day=k) for k in range(1, 8)}
                 for time in times}
    return render(request, 'schedule/week_schedule.html', locals())


def show_detail(request, pk):
    info = get_object_or_404(Schedule, id=pk)
    return render(request, 'schedule/schedule_detail.html', locals())
