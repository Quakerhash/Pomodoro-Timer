from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm
from .utils import generate_otp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm
import time

otp_storage = {}

def login_register(request):
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()

    if request.method == "POST":
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect('home')
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                email = register_form.cleaned_data['email']
                email_otp = generate_otp()
                otp_storage[email] = email_otp

                send_mail(
                    'Email Verification OTP',
                    f'Your OTP for email verification is: {email_otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                request.session['pending_user'] = {
                    'username': user.username,
                    'email': email,
                    'password': request.POST['password1']
                }
                request.session['last_otp_sent'] = time.time()
                return redirect('otp')
    
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'login.html', context)

def otp(request):
    if request.method == 'POST':
        email_otp = request.POST['otp']
        pending_user = request.session.get('pending_user')

        if not pending_user:
            return redirect('login_register')

        email = pending_user['email']
        stored_otp = otp_storage.get(email)

        if stored_otp and stored_otp == email_otp:
            user = User.objects.create_user(
                username=pending_user['username'],
                email=email,
                password=pending_user['password']
            )
            del otp_storage[email]
            del request.session['pending_user']
            if 'last_otp_sent' in request.session:
                del request.session['last_otp_sent']

            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'otp.html', {'error': 'Invalid OTP'})

    cooldown_remaining = 0
    last_sent = request.session.get('last_otp_sent')
    if last_sent:
        elapsed = time.time() - last_sent
        if elapsed < 30:
            cooldown_remaining = int(30 - elapsed)

    return render(request, 'otp.html', {'cooldown': cooldown_remaining})

def resend_otp(request):
    pending_user = request.session.get('pending_user')

    if not pending_user:
        return redirect('login_register')

    last_sent = request.session.get('last_otp_sent')
    if last_sent:
        elapsed = time.time() - last_sent
        if elapsed < 30:
            remaining = int(30 - elapsed)
            return render(request, 'otp.html', {
                'error': f'Please wait {remaining} seconds before requesting another OTP.',
                'cooldown': remaining
            })

    email = pending_user['email']
    new_otp = generate_otp()

    otp_storage[email] = new_otp

    send_mail(
        'Resend OTP - Email Verification',
        f'Your new OTP is: {new_otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    request.session['last_otp_sent'] = time.time()

    return render(request, 'otp.html', {
        'message': 'A new OTP has been sent to your email.',
        'cooldown': 30
    })
