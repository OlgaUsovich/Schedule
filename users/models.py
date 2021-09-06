from django.contrib.auth.models import AbstractUser
from django.db import models

from schedule.models import Teachers, Groups


class User(AbstractUser):
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('Students', on_delete=models.DO_NOTHING, blank=True, null=True)
    profile_photos = models.ForeignKey('ProfilePhotos', on_delete=models.CASCADE, verbose_name='Фото профиля',
                                       blank=True, null=True)
    age = models.CharField(max_length=3, blank=True, null=True, verbose_name='Возраст')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    city = models.CharField(max_length=100, verbose_name='Город')
    status_message = models.CharField(max_length=100, verbose_name='Статус')
    contacts = models.CharField('Номер телефона', max_length=255) #сделать связь
    address = models.TextField('Адрес', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class ProfilePhotos(models.Model):
    profile_photo = models.ImageField(upload_to=f'profile_avatars/')

    class Meta:
        verbose_name = 'Фото профиля'
        verbose_name_plural = 'Фото профиля'


class Contacts(models.Model):
    phone = models.CharField('Номер телефона', max_length=255)
    email = models.EmailField('Электронная почта')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = 'Контакты пользователей'


class Students(models.Model):
    name = models.CharField('Имя', max_length=255)
    surname = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчестсво', max_length=255, null=True, blank=True)
    group = models.ManyToManyField(Groups, related_name='group')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
