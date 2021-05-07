from django import forms

from schedule.models import Schedule


class TeacherFilter(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['teacher', 'room', 'group']


class ScheduleEdit(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['event', 'event_date', 'event_time', 'room', 'group', 'teacher', 'note']


