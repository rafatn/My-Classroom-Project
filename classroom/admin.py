from django.contrib import admin
from .models import LessonRecording, UserOTP

admin.site.register(UserOTP)


@admin.register(LessonRecording)
class LessonRecordingAdmin(admin.ModelAdmin):
  list_display = ('title', 'uploaded_at', 'uploaded_by')
  search_fields = ('title',)
