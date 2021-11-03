from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User

# Create your models here.
class Globaltag(models.Model):
    name = models.CharField( max_length=150, null=False, blank=False)

class Thought(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Globaltag, related_name='Global_tags', blank=True)
    created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Thought = models.ForeignKey(Thought,on_delete=models.CASCADE)


class Replycomment(models.Model):
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Comment = models.ForeignKey(Comment,on_delete=models.CASCADE)

class Likethought(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Thought = models.ForeignKey(Thought,on_delete=models.CASCADE)


class Likecomment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Comment = models.ForeignKey(Comment,on_delete=models.CASCADE)




