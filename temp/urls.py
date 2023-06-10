from django.urls import path
from . import views
from . import check
urlpatterns = [
    path('h1',views.home,name='home'),
    path('h2',views.showuser,name='showuser'),
    path('emotion_detector',views.liveStreaming,name='emotion_detector'),
    path('end_streaming',views.endStreming,name='end_streaming'),
    path('login',views.get_user_details,name="user_login"),
    path("check",views.privateFunction,name="check"),
    path('signup', views.signup, name ='signup'),
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('userhome',views.userhome,name="userhome"),
    path('api/audio/<str:id>/',views.streamSong.as_view(),name="streamSong"),
    path('likesong/<str:song_id>/',views.likesong,name="likesong"),
    path('issongliked/<str:song_id>/',views.isSongLiked,name="issongliked"),
    # path('start_listening',views.start_listening,name="start_listening"),
    # path('stop_listening',views.stop_listening,name="stop_listening"),
    path('listenedSong/<str:song_id>/',views.listenedSong,name="listenedSong"),
    path("getpastlistensong",views.get_past_listened_songs,name="getpastsongs"),
    path('getlikedsongs',views.get_liked_songs,name="getlikedsongs"),
    path("landingpage",views.landing,name="landing")
    
    
    # path('temp',views.temp,name="temp"),
    
]
