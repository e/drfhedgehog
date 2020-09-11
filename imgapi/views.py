from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .serializers import ImageSerializer, UserSerializer
from .models import Image, Follower


def index(request):
    return HttpResponse("You're at the imgapi index.")

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'images': reverse('image-list', request=request, format=format),
        'all posts': reverse('post-list', request=request, format=format),
    })


class ImageList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        users = [f.following for f in request.user.following.all()]
        images = Image.objects.filter(user__in=users)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class UserImages(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        images = request.user.images.all().order_by('-created_at')
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data =request.data.copy()
        data.update(user=request.user.id)
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class Register(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PostList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        images = sorted(Image.objects.all(), key=lambda img: img.likes_count, reverse=True)
        serializer_context = {
            'request': request,
        }
        serializer = ImageSerializer(images, many=True, context=serializer_context)
        return Response(serializer.data)


class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_target_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, action, pk):
        target_user = self.get_target_user(pk)
        follower_qs = Follower.objects.filter(
            follower=request.user,
            following=target_user)
        if action == 'follow':
            if follower_qs:
                return Response({'Message': f'You are already following {target_user.username}'})
            Follower.objects.create(
                follower=request.user,
                following=target_user)
            return Response({'Message': f'You are now following {target_user.username}'})
        else:
            if not follower_qs:
                return Response({'Message': f'You were not following {target_user.username}'})
            follower_qs[0].delete()
            return Response({'Message': f'You are no longer following {target_user.username}'})


class LikeImage(APIView):
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        image = self.get_object(pk)
        if request.user in image.likes.all():
            return Response({'Message': f'You already like image with id {image.id}'})
        image.likes.add(request.user)
        return Response({'Message': f'Now you like image with id {image.id}'})