from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
# Create your models here.

class Songs(models.Model):
    song_id = models.CharField(max_length=50)
    song_name = models.CharField(max_length=100)
    song_url = models.CharField(max_length=100)
    song_image = models.CharField(max_length=100)
    artists_name = models.CharField(max_length=100)
    popularity = models.IntegerField()
    duration = models.FloatField()
    song_type = models.CharField(max_length=50)

class mp3Tracks(models.Model):
    track_id=models.CharField(max_length=50)
    track_mp3=models.BinaryField(max_length=2147483647)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        
class Listen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    elapsed_time = models.PositiveIntegerField()
    
class PastListenSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    date_listened = models.DateTimeField(auto_now_add=True)
  
    


    

    
