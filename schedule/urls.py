from django.urls import path

from schedule import views

app_name = 'schedule'

urlpatterns = [
    path('', views.display_schedule, name='schedule'),
    path('calendar/', views.show_calendar, name='calendar'),
    path('week/<int:pk>', views.show_detail, name='event_detail'),
    path('week/', views.week_schedule, name='week_schedule'),
    path('scheduleedit/<int:pk>', views.edit_schedule, name='edit_schedule'),
    path('daylist/<str:date>', views.show_events_ofday, name='day_events'),
    path('schedule_add/', views.add_schedule_line, name='schedule_add'),
    path('schedule_delete/<int:pk>', views.delete_schedule_line, name='delete_schedule_line'),
]
