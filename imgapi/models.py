from django.conf import settings
from django.db import models


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100, blank=True, null=True)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    @property
    def likes_count(self):
        return self.likes.count()


class Follower(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'
