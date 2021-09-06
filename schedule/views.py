import calendar
import datetime

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max, Min
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TeacherFilter, ScheduleEdit
from .models import Schedule, EventTime, Groups, Rooms


def display_schedule(request):
    form = TeacherFilter(request.user, request.GET)
    schedule_lines = Schedule.objects.all()
    if not schedule_lines:
        return render(request, 'schedule/empty_schedule_form.html')
    # отображаются для студента и преподавателя даты только их групп, для менеджера, директора и администратора -
    # все возможные даты всех групп
    if request.user.is_authenticated:
        if request.user.student_id:
            # aggregate выбирает данные напрямую из БД без формирования queryset
            start_end = Groups.objects.filter(students=request.user).aggregate(Max('end_date'), Min('start_date'))
            dates = [single_date for single_date in
                     pd.date_range(start_end.get('start_date__min'), start_end.get('end_date__max'))]
            schedule_lines = Schedule.objects.filter(
                event_date__range=(start_end.get('start_date__min'), start_end.get('end_date__max')),
                group__in=Groups.objects.filter(students=request.user))
        elif request.user.teacher_id:
            start_end = Groups.objects.filter(teacher=request.user).aggregate(Max('end_date'), Min('start_date'))
            dates = [single_date for single_date in
                     pd.date_range(start_end.get('start_date__min'), start_end.get('end_date__max'))]
            schedule_lines = Schedule.objects.filter(
                event_date__range=(start_end.get('start_date__min'), start_end.get('end_date__max')),
                group__in=Groups.objects.filter(teacher=request.user))
        else:
            start_end = Groups.objects.all().aggregate(Max('end_date'), Min('start_date'))
            dates = [single_date for single_date in
                     pd.date_range(start_end.get('start_date__min'), start_end.get('end_date__max'))]
    else:
        start_end = schedule_lines.aggregate(Max('event_date'), Min('event_date'))
        dates = [single_date for single_date in
                 pd.date_range(start_end.get('event_date__min'), start_end.get('event_date__max'))]

    if form.is_valid():
        schedule_lines = schedule_lines.filter(**{k: v for k, v in form.cleaned_data.items() if v})
        if request.GET.get('event_date'):
            dates = [datetime.datetime.strptime(request.GET.get('event_date'), '%Y-%m-%d').date()]
        elif request.GET:
            start_end = schedule_lines.aggregate(Max('event_date'), Min('event_date'))
            dates = [single_date for single_date in
                     pd.date_range(start_end.get('event_date__min'), start_end.get('event_date__max'))]

    if request.user.is_authenticated and not (request.user.student_id or request.user.teacher_id):
        times = EventTime.objects.all()
        if request.GET.get('room'):
            rooms = Rooms.objects.filter(id__in=schedule_lines.values_list('room', flat=True))
        else:
            rooms = Rooms.objects.all()
    else:
        times = EventTime.objects.filter(id__in=schedule_lines.values_list('event_time', flat=True))
        rooms = Rooms.objects.filter(id__in=schedule_lines.values_list('room', flat=True))
    time_dict = {
        room: {
            time: {
                k: schedule_lines.filter(event_time=time, event_date=k, room=room) for k in dates
            } for time in times
        } for room in rooms
    }
    return render(request, 'schedule/schedule_form.html', locals())


def show_calendar(request):
    today = datetime.date.today()
    days = list(calendar.Calendar(firstweekday=0).itermonthdates(today.year, today.month))
    schedule_dates = [i[0] for i in list(Schedule.objects.values_list('event_date'))]
    return render(request, 'schedule/calender.html', locals())


def week_schedule(request):
    form = TeacherFilter(request.user, request.GET)
    today = datetime.datetime.today()
    week_num = request.GET.get('week', default=today.isocalendar()[1])
    d = f'{today.year}-{week_num}'
    dates_of_week = [datetime.datetime.strptime(f'{d}-{i}', '%G-%V-%u').date() for i in range(1, 8)]
    schedule_lines = Schedule.objects.filter(event_date__in=dates_of_week)

    if form.is_valid():
        schedule_lines = schedule_lines.filter(**{k: v for k, v in form.cleaned_data.items() if v})
        if request.GET.get('event_date'):
            dates = [datetime.datetime.strptime(request.GET.get('event_date'), '%Y-%m-%d').date()]

    times = EventTime.objects.filter(id__in=schedule_lines.values_list('event_time', flat=True))
    rooms = Rooms.objects.filter(id__in=schedule_lines.values_list('room', flat=True))
    time_dict = {
        room: {time: {k: schedule_lines.filter(event_time=time, event_date__iso_week_day=k, room=room) for k in
                      range(1, 8)}
               for time in times} for room in rooms}
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
@permission_required('add_schedule', raise_exception=True)
def add_schedule_line(request):
    if request.GET:
        form = ScheduleEdit(initial={'event_date': request.GET.get('date'), 'event_time': request.GET.get('time'),
                                     'room': request.GET.get('room')})
    else:
        form = ScheduleEdit()
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
            return redirect('schedule:schedule')
    return render(request, 'schedule/add_line.html', locals())


def book_room(request):
    rooms = Schedule.objects.all()
    return render(request, 'schedule/book_room.html', locals())


@login_required
def delete_schedule_line(request, pk):
    schedule_line = get_object_or_404(Schedule, pk=pk)
    schedule_line.delete()
    messages.add_message(request, messages.SUCCESS, 'Запись удалена')
    return redirect('schedule:schedule')
