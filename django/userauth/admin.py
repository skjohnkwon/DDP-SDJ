from django.contrib import admin
from phase_two.admin import CommentInline, ItemInLine
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.admin.sites import NotRegistered

# Register your models here.

class CustomUserAdmin(UserAdmin):
    inlines = [CommentInline, ItemInLine]
try:
    admin.site.unregister(User)
except NotRegistered:
    pass 

admin.site.register(User, CustomUserAdmin)