from django import forms

from schedule.models import Schedule


class TeacherFilter(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['teacher', 'room']


