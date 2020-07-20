from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=256)


class Tweet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280, default='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User)
    retweets = models.ManyToManyField(User)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    retweet_to = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
