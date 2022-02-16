from django.contrib import admin

from .models import User, Role, Permission

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
