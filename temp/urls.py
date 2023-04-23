from django.urls import path
from . import views
from . import check
urlpatterns = [
    path('h1',views.home,name='home'),
    path('h2',views.showuser,name='showuser'),
    path('get_songs',views.get_songs,name="getSongs"),
    path('emotion_detector',views.liveStreaming,name='emotion_detector'),
    path('end_streaming',views.endStreming,name='end_streaming'),
    path('login',views.get_user_details,name="user_login"),
    path("check",views.privateFunction,name="check"),
    path('signup', views.signup, name ='signup'),
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('books', views.books, name="books"),
    path('userhome',views.userhome,name="userhome"),
    
]
