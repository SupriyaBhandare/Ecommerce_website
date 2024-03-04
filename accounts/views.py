from django.shortcuts import render, HttpResponseRedirect,redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UpdateUserProfileForm


def user_profileupdate(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(request,"Profile updated successfully")
                form.save()
                # return redirect('index')
        else:
            form = UpdateUserProfileForm(instance=request.user)
        return render(request, 'accounts/profileupdate.html', {'name':request.user,'form': form})
    else:
        return redirect('login')

# Views function for user authentication
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm
            messages.success(request, "Account Created Successfully")
    else:
        form = UserCreationForm
    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def Userchangepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request,"Password Changed successfully")
                # To maintain session of user after changing password otherwise it will redirect to homepage without login
                update_session_auth_hash(request,form.user)
                return redirect('index')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/changepass.html' ,{'form':form})
    else:
        return redirect('login')