from django.contrib.auth.models import User
from django.db import models


class UserOTP(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  otp_code = models.CharField(max_length=6)
  created_at = models.DateTimeField(auto_now=True)


class LessonRecording(models.Model):
  title = models.CharField(max_length=255, verbose_name='שם השיעור')
  video_file = models.FileField(
      upload_to='recordings/', verbose_name='קובץ הקלטה'
  )
  uploaded_at = models.DateTimeField(
      auto_now_add=True, verbose_name='תאריך העלאה'
  )
  uploaded_by = models.ForeignKey(
      User, on_delete=models.SET_NULL, null=True, verbose_name='הועלה על ידי'
  )

  def __str__(self):
    return self.title
