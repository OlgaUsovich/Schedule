from django.urls import path

from schedule import views

app_name = 'schedule'

urlpatterns = [
    path('', views.display_schedule, name='schedule'),
    path('calendar/', views.show_calendar),
    path('week/', views.week_schedule),
]