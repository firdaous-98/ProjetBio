import os
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import CreateUserForm, UserLoginForm, ResumeUpload
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Analysis, Profile
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from zipfile import ZipFile
import subprocess

UserModel = get_user_model()


# Create your views here.

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['username'] = username
        if next:
            return redirect(next)
        return redirect ('/home')

    context = {
        'form' : form,
    }
    return render(request, "login.html", context)


def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            profile = Profile.objects.create(user=user.username,nbr_of_analysis=1)
            profile.save()
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def home_view(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect('/')

def index_view(request):
    return render(request, "index.html")

def upload_view(request):
    return render(request, "upload.html")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def acc_activate(request):
    return render(request, "acc_active_email.html")


def upload_data(request):
    if request.method == "POST":
        username = request.session['username']
        profile = Profile.objects.get(user = username)
        nbr = profile.nbr_of_analysis
        form = ResumeUpload(request.POST, request.FILES)
        files = request.FILES.getlist('fastq_files')
        if form.is_valid():
            for f in files:
                file_instance = Analysis(fastq_files=f)
                file_instance.dateDebut = datetime.now()
                file_instance.user = username
                file_instance.number = nbr
                file_instance.save()
        #process = subprocess.call(['data/test_script.sh'])
        profile.nbr_of_analysis += 1
        profile.save()
        return script_exec(request)
    else:
        form = ResumeUpload()
        return render(request, 'upload.html', {'form': form})

def script_exec(request):
    process = subprocess.call(["data/test_script.sh"])
    return render(request, "temp.html")