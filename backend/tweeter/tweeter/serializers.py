from django.contrib.auth.models import User, Group
from tweeter.tweeter.models import Tweet, Client
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['url', 'created', 'text', 'creator', 'likes', 'retweets', 'client', 'retweet_to']
        read_only_fields = ['created', 'text', 'creator', 'likes', 'retweets', 'client', 'retweet_to']
