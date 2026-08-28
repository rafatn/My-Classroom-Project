import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import LessonRecording, UserOTP


def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      code = str(random.randint(100000, 999999))
      UserOTP.objects.update_or_create(user=user, defaults={'otp_code': code})

      # קוד OTP מודפס בקונסולה לבדיקה מקומית
      print(f'\n==============================')
      print(f'🔒 OTP Code for {username}: {code}')
      print(f'==============================\n')

      request.session['pre_otp_user_id'] = user.id
      return redirect('verify_otp')
    else:
      return render(
          request,
          'classroom/login.html',
          {'error': 'שם משתמש או סיסמה שגויים'},
      )

  return render(request, 'classroom/login.html')


def verify_otp_view(request):
  user_id = request.session.get('pre_otp_user_id')
  if not user_id:
    return redirect('login')

  if request.method == 'POST':
    entered_code = request.POST.get('otp_code')
    try:
      otp_record = UserOTP.objects.get(user_id=user_id)
      if otp_record.otp_code == entered_code:
        user = otp_record.user
        login(request, user)
        del request.session['pre_otp_user_id']
        otp_record.delete()
        return redirect('virtual_classroom')
      else:
        return render(
            request,
            'classroom/otp_verify.html',
            {'error': 'קוד OTP שגוי, נסה שוב'},
        )
    except UserOTP.DoesNotExist:
      return redirect('login')

  return render(request, 'classroom/otp_verify.html')


@login_required(login_url='login')
def virtual_classroom_view(request):
  recordings = LessonRecording.objects.all().order_by('-uploaded_at')
  context = {
      'username': request.user.username,
      'is_admin': request.user.is_superuser,
      'recordings': recordings,
  }
  return render(request, 'classroom/room.html', context)
