from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование события')
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.name


class EventTime(models.Model):
    start = models.TimeField(verbose_name='Время начала')
    end = models.TimeField(verbose_name='Время окончания', blank=True, null=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        ordering = ('start',)
        verbose_name = 'Период события'
        verbose_name_plural = 'Временные интервалы событий'

    def __str__(self):
        return f'{self.start} - {self.end}'


class Teachers(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', db_index=True)
    patronymic = models.CharField(max_length=255, verbose_name='Отчество', blank=True, null=True)
    photo = models.ImageField(verbose_name='Фото', blank=True, null=True)
    bio = models.TextField(verbose_name='О преподавателе', blank=True, null=True)

    class Meta:
        ordering = ('last_name', 'first_name',)
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Groups(models.Model):
    gr_num = models.CharField(max_length=255, verbose_name='Номер группы')
    course = models.ForeignKey('Courses', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(verbose_name='Дата начала группы', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания группы', blank=True, null=True)
    group_status = models.CharField(max_length=10, verbose_name='Статус группы')
    person_cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость обучения 1 человека')
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'{self.gr_num} - {self.course.name}'


class Courses(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование курса')
    duration = models.DecimalField(verbose_name='Длительность курса', max_digits=3, decimal_places=1, blank=True,
                                   null=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Rooms(models.Model):
    room_num = models.CharField(max_length=255, verbose_name='Номер/наименование аудитории')
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'

    def __str__(self):
        return self.room_num


class Schedule(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Группа', blank=True, null=True,
                              default=None)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, verbose_name='Событие')
    event_time = models.ForeignKey(EventTime, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   verbose_name='Время события', related_name='time')
    event_date = models.DateField(verbose_name='Дата события')
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, blank=True, null=True,
                                verbose_name='Преподаватель')
    room = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING, blank=True, null=True,
                             verbose_name='Аудитория')
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        verbose_name = 'Событие в расписании'
        verbose_name_plural = 'Раписание'

    def __str__(self):
        return f'{self.group}, {self.event}, {self.event_time}, {self.event_date}'

    def short_name(self):
        return f'{self.event}, {self.group}, {self.teacher}'
