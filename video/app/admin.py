from django.contrib import admin

# Register your models here.
from app.model.video import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id','name','video_type','from_to','nationality','info','createdtm','updatedtm']
    ordering = ['id']
    list_per_page = 10
    search_fields = ['name']
    readonly_fields = ['created_time','updated_time']
