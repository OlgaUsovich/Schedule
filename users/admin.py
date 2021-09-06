from django.contrib import admin

# Register your models here.
from users.models import *

# admin.site.register([User, ProfilePhotos, Contacts, Students])
admin.site.register([User, ProfilePhotos, Contacts])
