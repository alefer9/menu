# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 
# local Django
from .models import *

from delivery_app.models import User 
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =   ('id',
    				  'username',
    				  'password',
    				  'first_name',
    				  'last_name',
    				  'email',
    				  'is_staff',
    				  'is_active',
    				  'is_superuser',
    				  'last_login',
    				  'date_joined')