# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from delivery_app.models import User  
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =   ('id','username','password','first_name','last_name',
'email','is_staff','is_active','is_superuser',
'last_login','date_joined')