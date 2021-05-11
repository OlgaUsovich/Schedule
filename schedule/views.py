import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import TeacherFilter, ScheduleEdit
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


@login_required
def edit_schedule(request, pk):
    schedule_info = get_object_or_404(Schedule, id=pk)
    if request.method == "POST":
        form = ScheduleEdit(request.POST, instance=schedule_info)
        if form.is_valid():
            schedule_info = form.save()
            return redirect('schedule:event_detail', pk=pk)
    else:
        form = ScheduleEdit(instance=schedule_info)
    return render(request, 'schedule/edit_schedule.html', locals())

def show_events_ofday(request, date):
    schedule_info = Schedule.objects.filter(event_date=date)
    return render(request, 'schedule/day_list.html', locals())


@login_required
def add_schedule_line(request):
    if request.method == 'POST':
        form = ScheduleEdit(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Schedule.objects.create(group=cleaned_data['group'],
                                    event=cleaned_data['event'],
                                    event_time=cleaned_data['event_time'],
                                    event_date=cleaned_data['event_date'],
                                    teacher=cleaned_data['teacher'],
                                    room=cleaned_data['room'],
                                    note=cleaned_data['note'])
            return redirect('http://127.0.0.1:8000/calendar/')
    form = ScheduleEdit()
    return render(request, 'schedule/add_line.html', locals())
