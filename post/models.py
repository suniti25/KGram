from django.db import models
from datetime import datetime

# Create your models here.
class PostModel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    content = models.TextField(max_length=3200, blank=True)
    image = models.CharField(max_length=255, blank=True)
    posted_by = models.ForeignKey("user.UserModel", on_delete=models.CASCADE, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp','-id']

class PostLikeModel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, blank=False)
    liked_by = models.ForeignKey("user.UserModel", on_delete=models.CASCADE, blank=False)

    class Meta:
        app_label = 'post'

class CommentModel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, blank=False)
    comment = models.TextField()
    commented_by = models.ForeignKey("user.UserModel", on_delete=models.CASCADE, blank=False)
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        app_label = 'post'