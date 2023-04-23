from django.db import models
from django_mysql.models import ListCharField
# Create your models here.

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class User(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=20)

class Songs(models.Model):
    song_id = models.CharField(max_length=50)
    song_name = models.CharField(max_length=100)
    song_url = models.CharField(max_length=100)
    song_image = models.CharField(max_length=100)
    artists_name = ListCharField(
        base_field=models.CharField(max_length=50),
        size=10,
        max_length=(10 * 51),  # 10 * 50 character nominals, plus commas
    )
    popularity = models.IntegerField()
    duration = models.FloatField()
    song_type = models.CharField(max_length=50)

    

    
