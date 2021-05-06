from django.urls import path

from schedule import views

app_name = 'schedule'

urlpatterns = [
    path('', views.display_schedule, name='schedule'),
    path('calendar/', views.show_calendar, name='calendar'),
    path('week/<int:pk>', views.show_detail, name='event_detail'),
    path('week/', views.week_schedule, name='week_schedule'),
]
