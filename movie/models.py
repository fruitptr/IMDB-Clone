from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from datetime import datetime as dt
from datetime import timedelta
import zoneinfo
from auth_login.models import Comment
from django.db.models import Avg

GENRE_CHOICE = [
    ('action', 'action'),
    ('adventure', 'adventure'),
    ('comedy', 'comedy'),
    ('romance', 'romance'),
    ('horror', 'horror'),
    ('sci-fi', 'sci-fi'),
    ('animation', 'animation'),
    ('crime', 'crime'),
    ('TBD', 'TBD'),
]


# Create your models here.
class Movie(models.Model):
    movie_name = models.TextField(default='TBD', null=False, blank=False)
    description = models.TextField(default='TBD', null=False, blank=False)
    budget = models.TextField(null=True)
    genre = models.TextField(choices=GENRE_CHOICE, default='TBD', null=False)
    year_released = models.DateField(null=True)
    movie_trailer_url = models.URLField(null=True)
    director = models.TextField(null=True)
    cast = ArrayField(models.IntegerField())
    runtime = models.DurationField(null=True)
    cover_art = models.ImageField(upload_to='cover_art/')
    producer_name = models.ForeignKey('auth_login.Producer', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    user_avg_rating = models.FloatField(default=None, null=True)
    critic_avg_rating = models.FloatField(default=None, null=True)

    def calc_user_rating(self):
        # comments = Comment.objects.filter(movie_id=self.id).aggregate(avg_rating=Avg(''))
        pass

    def calc_critic_rating(self):
        pass


class Actor(models.Model): # DON'T FORGET TO MIGRATE (COUNTRY NEW)
    name = models.TextField(null=False, blank=False)
    description = models.TextField(default='TBD', null=False, blank=False)
    gender = models.TextField(choices=GENRE_CHOICE, null=False, default='Prefer not to say')
    date_of_birth = models.DateField(null=True)
    actor_profile_picture = models.ImageField(upload_to='actor_profile_picture/')
    country = models.TextField(default='Unknown')
    view_count = models.IntegerField(default=0)

    def get_age(self):
        current_date = dt.now(tz=zoneinfo.ZoneInfo('UTC')).date()
        age = current_date.year - self.date_of_birth.year - ((current_date.month, current_date.day)<(self.date_of_birth.month, self.date_of_birth.day))
        print(type(age), age)
        return age
