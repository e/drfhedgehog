from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Image, Follower


class ImageSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Image
        fields = ('id', 'title', 'caption', 'image', 'user', 'likes_count', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'followers', 'following')
