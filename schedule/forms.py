from django import forms

from schedule.models import Schedule


class TeacherFilter(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Дата", required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated and (user.student_id or user.teacher_id):
            self.fields['group'].queryset = self.fields['group'].queryset.filter(students=user)

    class Meta:
        model = Schedule
        fields = ['teacher', 'room', 'group', 'event_date']


class ScheduleEdit(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Дата")

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get("event_date")
        group = cleaned_data.get("group")
        if event_date > group.end_date or event_date < group.start_date:
            msg = "Дата события не соответствует периоду обучения группы."
            self.add_error('event_date', msg)

    class Meta:
        model = Schedule
        fields = ['event', 'event_date', 'event_time', 'room', 'group', 'teacher', 'note']

