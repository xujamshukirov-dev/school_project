from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Maktab

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'rol', 'viloyat', 'tuman', 'maktab_raqam', 'reyting']
    list_filter = ['rol', 'viloyat']
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('rol', 'viloyat', 'tuman', 'maktab_raqam', 'sinf', 'reyting')}),
    )

@admin.register(Maktab)
class MaktabAdmin(admin.ModelAdmin):
    list_display = ['raqam', 'viloyat', 'tuman', 'reyting']
    list_filter = ['viloyat']
