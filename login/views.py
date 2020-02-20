from django.shortcuts import render, redirect
from .models import User
from datetime import datetime
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash,birthday=request.POST['birthday'])
            request.session['userid'] = User.objects.last().id
            return redirect('/wall')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            logged_user = user[0]
            request.session['userid'] = logged_user.id
            return redirect('/wall')
    return redirect('/')
            
def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['userid'])
        return render(request,'success.html',{'user':user})

def logout(request):
    request.session.flush()
    return redirect('/')