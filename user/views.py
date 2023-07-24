from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserRegistrationForm, UserLoginForm, verifyForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import user
from django.core.mail import send_mail
from django.conf import settings
import random


def home_view(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        username = request.session.get('username')
        user_obj = user.objects.get(username=username)
        context = {
            'username': username.capitalize(),
        }
        if user_obj.isVerify:
            return render(request, 'home.html', context)
        else:
            return redirect('verify')
    else:
        return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data['first_name']
            lsatName = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            input_password = form.cleaned_data['password']
            hashed_password = make_password(input_password)
            fromemail = form.cleaned_data['email']
            doB = form.cleaned_data['dob']
            verify_code_generate = code()

            new_user = user(
                first_name= firstName,
                last_name=lsatName,
                username=username,
                email=fromemail,
                password=hashed_password,
                dob=doB,
                isActive=False,
                isVerify=False,
                verify_code=verify_code_generate,
            )
            # Save the user to the database
            new_user.save()
            user_obj = user.objects.get(username=username)
            request.session['user_id'] = user_obj.id
            request.session['username'] = user_obj.username

            subject = 'Welcome to Our DjProject'

            message = f'Hi {firstName} {lsatName},\n\nEnter the 6-digit code below to verify your identity and regain access to your Django Project account.! \n\n {verify_code_generate} \n\n Thanks for helping us keep your account secure. The Django eShikhon Team'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [fromemail,]

            send_mail(subject, message, from_email,
                      recipient_list)

            return redirect('verify')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user_obj = user.objects.get(username=username)
                request.session['user_id'] = user_obj.id
                request.session['username'] = user_obj.username

                if check_password(password, user_obj.password):
                    if user_obj.isVerify:
                        return redirect('home')
                    else:
                        return redirect('verify')
                else:
                    messages.error(request, 'passwor not matched')
                    return redirect('login')
            except user.DoesNotExist:
                messages.error(request, 'username not found')
                return redirect('login')

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    request.session.clear()
    return redirect('home')


def code():
    code = random.randint(100000, 999999)
    return code


def verify(request):
    if request.method == 'POST':
        form = verifyForm(request.POST)
        user_id = request.session.get('user_id')
        username = request.session.get('username')
        if form.is_valid():
            user_obj = user.objects.get(username=username)
            code = form.cleaned_data['verify_code']
            if user_obj.verify_code == code:
                user_obj.isVerify = True
                user_obj.save()
                messages.success(request, 'verification successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid verification code.')
                return redirect('verify')
    else:
        username = request.session.get('username')
        context = {
            'username': username.capitalize(),
            'form': verifyForm()
        }
    return render(request, 'verify.html', context)
