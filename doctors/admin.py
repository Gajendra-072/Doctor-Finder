from django.contrib import admin
from django.utils.html import format_html
from .models import Organ, Doctor

@admin.register(Organ)
class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'description')
    search_fields = ('name', 'description')
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_photo', 'specialization', 'experience', 'clinic_address')
    list_filter = ('specialization', 'experience')
    search_fields = ('name', 'clinic_address', 'description')
    
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center;"><i class="fas fa-user-md"></i></div>')
    display_photo.short_description = 'Photo'
