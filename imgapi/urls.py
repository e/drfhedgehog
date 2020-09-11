from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static

# from rest_framework import routers
from rest_framework.authtoken import views as authtokenviews
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# router = routers.DefaultRouter()
# router.register(r'images', views.ImageViewSet)
# router.register(r'followers', views.FollowerViewSet)

urlpatterns = format_suffix_patterns([
    path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', authtokenviews.obtain_auth_token, name='api-token-auth'),
    path('api/', include([
    	path('', views.api_root),
        path('posts/',
            views.PostList.as_view(),
            name='post-list'),
        path('images/like/<int:pk>/',
            views.LikeImage.as_view(),
            name='like-image'),
        path('images/',
            views.ImageList.as_view(),
            name='image-list'),
        path('userimages/',
            views.UserImages.as_view(),
            name='userimages'),
	    path('users/',
	        views.UserList.as_view(),
        	name='user-list'),
        path('users/<int:pk>/',
            views.UserDetail.as_view(),
            name='user-detail'),
        path('register/',
            views.Register.as_view(),
            name='register'),
        re_path('(?P<action>follow|unfollow)/(?P<pk>[0-9]+)/',
            views.FollowUnfollowView.as_view(),
            name='followunfollow'),
    ])),
]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
