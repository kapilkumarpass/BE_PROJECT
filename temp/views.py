from django.views.decorators import gzip
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.http import StreamingHttpResponse
from keras.models import load_model
from tensorflow.keras.models import model_from_json
from temp.models import Musician
from django.db import connections
import numpy as np
import cv2
import cv2
import json
import csv
from temp.models import Songs
from temp.detect import *
from statistics import mode
from .forms import loginForm
from .models import User
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import SignUpForm,LogInForm
from django.views.decorators.csrf import csrf_exempt


@login_required
def privateFunction(request):
    return JsonResponse({"status":200})

def get_user_details(request):

    if request.method == "POST":
 
        form = loginForm(request.POST)
      
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            User.objects.get(email=email,password=password)
            return HttpResponse("kjdjnsv")
    else:
        form = loginForm()

    user = authenticate(username="john", password="johnpassword")
    if user is not None:
        return redirect('/home/h1')
    else:
        return render(request,"login.html",{"form":form})
    
        
    # return render(request, "login.html", {"form": form})

def home(request):
    # return render(request,'home.html',{'name':'kapil'}) 
    # return HttpResponse({'name':'skngfksa'}, content_type="application/json")
    # global cam 
    
    # with open('C:\\Users\\kapil\\Downloads\\song_database.csv', mode ='r',encoding="utf8")as file:
    #     csvFile = csv.reader(file)
    #     firstRun = True
    #     for lines in csvFile:
            
    #         if firstRun:
    #             firstRun = False
    #             continue
            
    #         song = Songs(
    #             song_id = lines[1],
    #             song_name = lines[2],
    #             song_url = lines[3],
    #             song_image = lines[4],
    #             artists_name = lines[6],
    #             popularity = int(lines[7]),
    #             duration = float(lines[8]),
    #             song_type = lines[9]
    #         )
    #         song.save()
    # print(request.GET.get('answer'))
    return render(request,'cam.html') 

@login_required(login_url="signin",redirect_field_name="signin")
def showuser(request):
    return render(request,'home.html') 

@login_required(login_url="signin",redirect_field_name="signin")
def liveStreaming(request):
    try:
        global cam 
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass
    
def endStreming(request):
    global cam
    print(cam.emotionlist)
    print("User is: ",mode(cam.emotionlist))
    cam.video.release()
    del(cam)
    return HttpResponse('')


def index(request, *args, **kwargs):
    return render(request, 'index.html')
@login_required(login_url="signin",redirect_field_name="signin")
def get_songs(request):
    songs = list(Songs.objects.values_list('song_url','song_name','artists_name').order_by('-popularity')[0:10])
    
    # return JsonResponse(
    #     {
    #         'statusCode':200,
    #         'body':{
    #             'songs':songs
    #         }
    #     })
    # print(type(songs[0]))
    return render(request,"songs.html",{'songs':songs})
    

@csrf_exempt
def signup(request):
    print("hello")
    # if request.user.is_authenticated:
    #     return redirect('books')
     
    if request.method == 'POST':
        print(request.body)
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('userhome')
         
        else:
            return render(request,'signup.html',{'form':form})
     
    else:
        form = SignUpForm()
        return render(request,'signup.html',{'form':form})
    
@login_required(login_url="signin",redirect_field_name="signin")
def books(request):
    # if request.user.is_authenticated:
    return render(request, 'books.html')
    # else:
    #     return redirect('signin')
 
def signin(request):
 
    if request.user.is_authenticated:
        return redirect('userhome')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            print("signin done")
            login(request,user)
            return render(request,'userHome.html')
        else:
            form = LogInForm()
            return render(request,'signin.html',{'form':form})
     
    else:
        form = LogInForm()
        return render(request, 'signin.html', {'form':form})
 
 
def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url="signin",redirect_field_name="signin")
def userhome(request):
    songs = list(Songs.objects.values_list('song_url','song_name','artists_name').order_by('-popularity')[0:10])

    return render(request,"userhome.html",{'songs':songs})
    