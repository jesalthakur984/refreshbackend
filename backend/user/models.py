from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    name = models.CharField( max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name

class Skill(models.Model):
     name = models.CharField( max_length=150, null=False, blank=False)


     def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True,upload_to='', default='default_profile.png')
    cover_pic = models.ImageField(blank=True, null=True,upload_to='', default='default_cover.jpg')
    bio = models.TextField(null=True)
    Skill = models.ManyToManyField(Skill, related_name='personal_skills', blank=True)
    Interest = models.ManyToManyField(Interest, related_name='topic_interests', blank=True)
    followers = models.ManyToManyField(User, related_name='follower', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    email_verified = models.BooleanField(default=False)