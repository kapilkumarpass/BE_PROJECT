from django.views.decorators import gzip
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.http import FileResponse
from django.http import StreamingHttpResponse
from keras.models import load_model
from tensorflow.keras.models import model_from_json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import ast
from itertools import chain
from .models import PastListenSong
from django.db.models import Subquery, OuterRef
from .models import Listen
from django.db import connections
from django.core.management import call_command
import numpy as np
from django.utils import timezone
from datetime import timedelta
import cv2
from datetime import datetime
import io
from pydub import AudioSegment
import os
from django.conf import settings
import base64
from django.shortcuts import get_object_or_404
import cv2
import json
import csv
from temp.models import Songs
from temp.detect import *
from statistics import mode
from .forms import loginForm
# from .models import User
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import SignUpForm,LogInForm
from django.views.decorators.csrf import csrf_exempt
from .models import mp3Tracks
import random
from django.views import View
from .models import Like

songs_path = os.path.join(settings.STATICFILES_DIRS[0], 'songs')
emotion="Neutral"

def landing(request):
    return render(request,'newsdetail.html') 

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


def home(request):
    with open('C:\\Users\\kapil\\Downloads\\song_database.csv', mode ='r',encoding="utf8")as file:
        csvFile = csv.reader(file)
        firstRun = True
        for lines in csvFile:
            
            if firstRun:
                firstRun = False
                continue
            
            song = Songs(
                song_id = lines[1],
                song_name = lines[2],
                song_url = lines[3],
                song_image = lines[4],
                artists_name = lines[6],
                popularity = int(lines[7]),
                duration = float(lines[8]),
                song_type = lines[9]
            )
            song.save()
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
    emoti=cam.emotionlist
    # neutral=[x for x in emoti if x == 'Neutral']
    other_emoti=[x for x in emoti if x != 'Neutral']
    ratio=0
    count_other=0
    if len(other_emoti)>0:
        other=mode(other_emoti)
        count_other=other_emoti.count(other)
    all_frames=len(emoti)
    ratio=count_other/all_frames
    if ratio>=0.25:
        emotion=other
    else:
        emotion=mode(emoti)
    # print(other," ",count_other)
    # emotion=mode(cam.emotionlist)
    print("User is: ",emotion)
    cam.video.release()
    del(cam)
    
    # total_rows = Songs.objects.count()

    # indices = random.sample(range(total_rows), 10)
    # songs = list(Songs.objects.values_list('song_id','song_url','song_name','artists_name').filter(song_type=emotion).order_by('-popularity').distinct()[0:10])
    songIdList= list(Songs.objects.values_list('song_id').filter(song_type=emotion)[0:120])
    # songIdList=[]
    # for i in songs:
    #     songIdList.append(i[0])
    # print(songIdList)
    # total_rows = list(mp3Tracks.objects.values_list('id').filter(track_id__in=songIdList))
    # # no_of_rows = len(total_rows)
    
    total_rows = [t[0] for t in songIdList]
    random.shuffle(total_rows)
    track_list_id = list(mp3Tracks.objects.values_list('track_id').filter(track_id__in=total_rows))
    random.shuffle(track_list_id)
    random_song_id = [t[0] for t in track_list_id]
    songs_details = list(Songs.objects.values_list('song_id','song_name','song_image').filter(song_id__in=random_song_id).distinct())
    random.shuffle(songs_details)
    # s=len(random_mp3_blobs)
    # final_mp3_blob = [t[1] for t in track_list_id]
    song_id_list=[t[0] for t in songs_details]
    songs_name = [t[1] for t in songs_details]
    song_image = [t[2] for t in songs_details]
    # songs_image = [t[1] for t in songs_details]
    
    
    # print("----------------------------------------------------")
    # print(random_song_id)
    # print("-----------------------------------------------------")
    # print(songs_name)
    # print("----------------------------------------------------")
    # return
    # merged_list = [(x, y) for x, y in zip(final_mp3_blob, songs_name)]
    # for filename in os.listdir(songs_path):
    #     file_path = os.path.join(songs_path, filename)
    #     try:
    #         if os.path.isfile(file_path):
    #             os.unlink(file_path)
    #     except Exception as e:
    #         print(f"Error deleting file: {file_path}\n{e}")
            
    # call_command('collectstatic', interactive=False)
    # count=0
    # s=len(songs_name)
    # song_static_list=[]
    # for i in range(0,s):
    #     blob=final_mp3_blob[i]
        
    #     file_path = os.path.join(songs_path, f"track{i}.mp3")
    #     song_static_list.append(f"track{i}.mp3")
    #     decoded_data = base64.b64decode(blob)

    #     # # Convert bytes back to audio data
    #     decoded_io = io.BytesIO(decoded_data)
    #     decoded_audio = AudioSegment.from_file(decoded_io, format='mp3')

    #     # # Save audio data as MP3 file
    #     decoded_audio.export(file_path, format='mp3')
        
    # call_command('collectstatic', interactive=False)
    # merged_list = [(x, y) for x, y in zip(song_id_list, songs_name)]
    # merged_list = [(x, y) for x, y in zip(merged_list, song_image)]
    merged_list = []
    for i in range(20):
        obj={"song_id":song_id_list[i],
             "song_name":songs_name[i],
             "song_image":song_image[i]}
        
        merged_list.append(obj)
    random.shuffle(merged_list)
    # data=json.dumps(merged_list)
    return render(request,"songs.html",{"songs_details":merged_list,"emotion":emotion})

class streamSong(View):
    def get(self,request,id):
        song_id=id
        file_path = f'songs/{song_id}.mp3'
        # song = get_object_or_404(mp3Tracks, track_id=song_id)
        # final_mp3_blob = song.track_mp3
        # # random_mp3_blob = list(mp3Tracks.objects.values_list('track_mp3').order_by('?').filter(track_id=song_id))
        # # final_mp3_blob = [t[0] for t in random_mp3_blob]
        # file_path = f'songs/{song_id}.mp3'
        # print("song found")
        # decoded_data = base64.b64decode(final_mp3_blob)

        # # # Convert bytes back to audio data
        # decoded_io = io.BytesIO(decoded_data)
        # decoded_audio = AudioSegment.from_file(decoded_io, format='mp3')
        # print("decoding complete")
        # # # Save audio data as MP3 file
        # decoded_audio.export(file_path, format='mp3')
        # print("file exported")
        # # call_command('collectstatic', interactive=False)
        return FileResponse(open(file_path,'rb'),content_type='audio/mpeg')

def index(request, *args, **kwargs):
    return render(request, 'index.html')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # print(request.body)
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
            return redirect('userhome')
        else:
            form = LogInForm()
            return render(request,'signin.html',{'form':form})
    else:
        form = LogInForm()
        return render(request, 'signin.html', {'form':form})
 
def signout(request):
    logout(request)
    return redirect('signin')

def get_popular_songs(user):
    song_ids = list(mp3Tracks.objects.values_list('track_id'))
    song_ids = [t[0] for t in song_ids]
    songs = list(Songs.objects.values_list('song_id','song_name','song_image','artists_name').filter(song_id__in=song_ids).order_by('-popularity').distinct()[0:18])
    popular_songs = []
    for i in songs:
        artist1=ast.literal_eval(i[3])
        obj1={"song_id":i[0],
             "song_name":i[1],
             "song_image":i[2],
             "artists_name":artist1}
        popular_songs.append(obj1)
    random.shuffle(popular_songs)
    return popular_songs

@login_required(login_url="signin",redirect_field_name="signin")
def userhome(request):
    user=request.user
    popularsongs=get_popular_songs(user)
    likedsongs=get_liked_songs(user)
    pastlistensongs=get_past_listened_songs(user)
    getSongsFromOtherUsers=get_likeSongs_from_allUsers(user)
    
    return render(request,"userhome.html",{'popular_songs':popularsongs,
                                           'liked_songs':likedsongs,
                                           'past_listen_songs':pastlistensongs,
                                            'other_users_songs':getSongsFromOtherUsers})


@login_required(login_url="signin",redirect_field_name="signin")    
def likesong(request, song_id):
    user = request.user
    
    song = list(Songs.objects.values_list('id').filter(song_id=song_id).distinct()[:1])
    song_id = [t[0] for t in song]

    user = User.objects.get(username=user)
    user_id = user.id
    if Like.objects.filter(user_id=user_id, song_id=song_id[0]).exists():
        Like.objects.filter(user_id=user_id, song_id=song_id[0]).delete()
        song_to_update = Songs.objects.get(id=song_id[0])  # Retrieve the object with id 
        
        song_to_update.popularity -= 1  # Decrease the value by 1
        song_to_update.save()
        liked = False
    else:
        Like.objects.create(user_id=user_id, song_id=song_id[0])
        song_to_update = Songs.objects.get(id=song_id[0])  #  Retrieve the object with id 
        
        song_to_update.popularity += 1  # Increase the value by 1
        song_to_update.save()
        liked = True
    total_likes = Like.objects.filter(song_id=song_id[0]).count()
    data = {'message': liked, 'total_likes': total_likes}
    return JsonResponse(data)


@login_required(login_url="signin",redirect_field_name="signin")    
def isSongLiked(request, song_id):
    user = request.user
    song = list(Songs.objects.values_list('id').filter(song_id=song_id).distinct()[:1])
    song_id = [t[0] for t in song]
    user = User.objects.get(username=user)
    user_id = user.id
    if Like.objects.filter(user_id=user_id, song_id=song_id[0]).exists():
        liked = True
    else:
        liked = False
    return JsonResponse(liked, safe=False)

# def start_listening(request, song_id):
#     user = request.user
#     song = list(Songs.objects.values_list('id').filter(song_id=song_id).distinct()[:1])
#     song_id = [t[0] for t in song]
#     user = User.objects.get(username=user)
#     user_id = user.id
#     listen = Listen.objects.create(user_id=user_id, song_id=song_id, start_time=datetime.now())

#     request.session['listen_id'] = listen.id

#     return redirect('play_song', song_id=song_id)


# def stop_listening(request, song_id):
#     user = request.user
#     song = list(Songs.objects.values_list('id').filter(song_id=song_id).distinct()[:1])
#     user = User.objects.get(username=user)
#     user_id = user.id
#     listen_id = request.session.get('listen_id')
#     listen = get_object_or_404(Listen, id=listen_id, user_id=user_id, song_id=song_id)

#     end_time = datetime.now()
#     elapsed_time = (end_time - listen.start_time).seconds
#     listen.end_time = end_time
#     listen.elapsed_time = elapsed_time
#     listen.save()

#     return redirect('past_listened_songs')

def listenedSong(request,song_id):
    user = request.user
    song = list(Songs.objects.values_list('id').filter(song_id=song_id).distinct()[:1])
    song_id = [t[0] for t in song]
    user = User.objects.get(username=user)
    user_id = user.id
    createnew= PastListenSong(user_id=user_id, song_id=song_id[0])
    createnew.save()
    return JsonResponse({"status":200})

def get_past_listened_songs(user):
    user = User.objects.get(username=user)
    user_id = user.id
    twelve_hours_ago = datetime.now() - timedelta(hours=12)
    past_listened_songs = list(PastListenSong.objects.values_list('song_id').filter(user_id=user_id, date_listened__lte=twelve_hours_ago).order_by('-date_listened'))
    past_listened_songs=[t[0] for t in past_listened_songs]
    song = list(Songs.objects.values_list('song_id','song_name','song_image','artists_name').filter(id__in=past_listened_songs).distinct())
    past_songs=[]
    # print(song)
    for i in song:
        artist2=ast.literal_eval(i[3])
        obj2={"song_id":i[0],
             "song_name":i[1],
             "song_image":i[2],
             "artists_name":artist2}
        past_songs.append(obj2)
    random.shuffle(past_songs)
    return past_songs

def get_liked_songs(user):
    
    user = User.objects.get(username=user)
    user_id = user.id
    
    get_liked_songs = Like.objects.values_list('song_id').filter(user_id=user_id).order_by('-created_at')
    
    get_liked_songs=[t[0] for t in get_liked_songs]
    get_song_details = list(Songs.objects.values_list('song_id','song_name','song_image','artists_name').filter(id__in=get_liked_songs).distinct())
    liked_songs=[]
    for i in get_song_details:
        artist2=ast.literal_eval(i[3])
        obj2={"song_id":i[0],
             "song_name":i[1],
             "song_image":i[2],
             "artists_name":artist2}
        liked_songs.append(obj2)
    random.shuffle(liked_songs)
    return liked_songs
   
def get_likeSongs_from_allUsers(user):
    user = User.objects.get(username=user)
    user_id = user.id
    all_users = list(User.objects.values_list('id').all())
    all_users=[t[0] for t in all_users]
    all_songs = list(Songs.objects.values_list('id').all())
    all_songs=[t[0] for t in all_songs]
    target_user = user_id
    data = dict()
    for user in all_users:
        user_liked = list(Like.objects.values_list('song_id').filter(user_id=user))
        user_liked=[t[0] for t in user_liked]
        data[user]=user_liked

    liked_songs=pd.DataFrame(0,index=all_songs,columns=all_users)
    for keys,values in data.items():
        for col in values:
            liked_songs.at[col,keys]=1
    # print(liked_songs.loc[8,13])
    user_similarity = cosine_similarity(liked_songs.T)
    
    nearest_neighbors = user_similarity[liked_songs.columns.get_loc(target_user)].argsort()[::-1][1:6]
    recommendations = set()
    for neighbor_index in nearest_neighbors:
        neighbor_user = liked_songs.columns[neighbor_index]
        neighbor_items = liked_songs[neighbor_user]
        recommendations.update(neighbor_items[neighbor_items == 1].index)
    
    user_ids=[]
    for ind in nearest_neighbors:
        column_name = liked_songs.columns[ind]
        user_ids.append(column_name)
    
    final_list_of_users_liked_songs=[]
    for id in user_ids:
        final_list_of_users_liked_songs.append(data[id])
    final_list_of_users_liked_songs = list(chain(*final_list_of_users_liked_songs))
    
    final_list_of_users_liked_songs = [x for i, x in enumerate(final_list_of_users_liked_songs) if x not in final_list_of_users_liked_songs[:i]]
    random.shuffle(final_list_of_users_liked_songs)
    get_song_details = list(Songs.objects.values_list('song_id','song_name','song_image','artists_name').filter(id__in=final_list_of_users_liked_songs).distinct())
    featured_liked_songs=[]
    for i in get_song_details:
        artist2=ast.literal_eval(i[3])
        obj2={"song_id":i[0],
             "song_name":i[1],
             "song_image":i[2],
             "artists_name":artist2}
        featured_liked_songs.append(obj2)
    random.shuffle(featured_liked_songs)
    return featured_liked_songs
   
    
    
# get_likeSongs_from_allUsers()

# def get_recommended_songs(request):
   
#     user_item_matrix = pd.DataFrame({
#         'User1': [1, 0, 1, 0, 0],
#         'User2': [0, 1, 1, 1, 0],
#         'User3': [1, 1, 0, 0, 1],
#         'User4': [0, 1, 1, 0, 1],
#         'User5': [1, 0, 0, 1, 0]
#     }, index=['Song1', 'Song2', 'Song3', 'Song4', 'Song5'])

#     user_similarity = cosine_similarity(user_item_matrix.T)

#     target_user = 'User1'

#     # Find nearest neighbors
#     nearest_neighbors = user_similarity[user_item_matrix.columns.get_loc(target_user)].argsort()[::-1][1:]

#     # Generate recommendations based on nearest neighbors
#     recommendations = set()
#     for neighbor_index in nearest_neighbors:
#         neighbor_user = user_item_matrix.columns[neighbor_index]
#         neighbor_items = user_item_matrix[neighbor_user]
#         recommendations.update(neighbor_items[neighbor_items == 1].index)

#     # Print recommendations
#     print(f"Recommendations for {target_user}:")
#     print(recommendations)
        
        
        