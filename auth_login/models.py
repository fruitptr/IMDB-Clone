from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from datetime import datetime as dt
from datetime import timedelta
import zoneinfo


USER_CHOICE = [
    ('normal', 'normal'),   # left->DB, right->django-admin
    ('critic', 'critic'),
    ('producer', 'producer'),
]

GENDER_CHOICE = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Prefer not to say', 'Prefer not to say')
]

RATING_CHOICE = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


# Create your models here.
class User(AbstractUser):
    user_type = models.TextField(choices=USER_CHOICE, default='normal', null=False)
    profile_picture = models.ImageField(upload_to='user_profile_picture/')


class NormalUser(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    favourite_list = ArrayField(models.IntegerField(), default=list)
    movies_rated = ArrayField(models.IntegerField(), default=list)


class Producer(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.TextField(null=False)
    movies_posted = ArrayField(models.IntegerField(), default=list)


class Critic(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    critic_organization = models.TextField(null=False)
    movies_rated = ArrayField(models.IntegerField(), default=list)
    # review_url = models.URLField(null=False)


class Comment(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    movie_id = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    comment_text = models.TextField(null=False, blank=False)
    rating = models.FloatField(null=False)
