from django.shortcuts import render, HttpResponse, redirect
from login.models import *
from .models import *
from datetime import datetime, timedelta, timezone



# Create your views here.
def index(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['userid']),
        'messages' : Message.objects.all().order_by('-created_at'),
        'comments' : Comment.objects.all().order_by('created_at'),
        'now' : datetime.now(timezone.utc)-timedelta(minutes=30),
    }        
    return render(request,'wall_app/index.html', context)

def post_message(request):
    if request.method == 'POST':
        if request.POST['message'] != '':
            user = User.objects.get(id=request.session['userid'])
            Message.objects.create(user=user,message=request.POST['message'])
    return redirect('/wall')

def post_comment(request, userid, msgid):
    if request.method == 'POST':
        if request.POST['comment'] != '':
            # create comment with each part sepearted out
            # comment_user = User.objects.get(id=request.session['userid'])
            # msg_user = User.objects.get(id=userid)
            # message_obj = msg_user.messages.get(id=msgid)
            # Comment.objects.create(user=comment_user,message=message_obj, comment = request.POST['comment'])
            Comment.objects.create(user=User.objects.get(id=request.session['userid']), message=User.objects.get(id=userid).messages.get(id=msgid), comment = request.POST['comment'])
    return redirect('/wall')

def logout(request):
    request.session.flush()
    return redirect('/')