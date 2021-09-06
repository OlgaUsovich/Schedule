from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import CreateUserView, view_profile, profile_edit, change_password

app_name = 'users'

urlpatterns = [
    path('reg/', CreateUserView.as_view(), name='registration'),
    path('login/',
         LoginView.as_view(template_name='users/login.html', success_url='{% url "users:profile" %}',
                           redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/change_password/', change_password, name='change_password'),
    path('profile/<int:id>/edit/', profile_edit, name='edit_profile'),
    path('profile/', view_profile, name='profile'),
]

