from django.contrib import admin
from .models import *



@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'year', 'owner', 'status', 'create_time')
    list_display_links = ('model', 'owner', 'status', 'create_time')
    list_editable = ('type', 'year')
    list_per_page = 10



@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_display_links = None
    list_editable = ('name', 'brand')
    list_per_page = 10



@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = None
    list_editable = ('name',)
    list_per_page = 10



@admin.register(Owners)
class OwnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    list_display_links = None
    list_editable = ('name', 'phone_number', 'email')
    list_per_page = 10



@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ('manager', 'client', 'time')
    list_display_links = ('time',)
    list_editable = ('manager', 'client')
    list_per_page = 10



@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_display_links = None
    list_editable = ('first_name', 'last_name')

    

@admin.register(Specialists)
class SpecialistsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'profile', 'image')
    list_display_links = ('first_name', 'last_name')
    list_editable = ('profile',)
    list_per_page = 10



@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'price')
    list_display_links = None
    list_editable = ('name', 'profile', 'price')
    list_per_page = 10
    


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Компьютерный сервис"