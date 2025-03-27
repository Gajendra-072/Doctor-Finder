from django.contrib import admin
from .models import Organ, Doctor

@admin.register(Organ)
class OrganAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'clinic_address')
    list_filter = ('specialization', 'experience')
    search_fields = ('name', 'clinic_address', 'description')
