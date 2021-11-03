from os import read
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from.models import Skill, Interest, UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


        
    


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '_all_'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields ='_all_'

class UserForPostSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','firstname','lastname','username','profile']

    def get_profile(self, obj):
        profilemain = obj.userprofile
        try:
            pic = profilemain.profile_pic.url
        except:
            pic = None
        return pic

class CountSerializer(serializers.ModelSerializer):
    followercount = serializers.SerializerMethodField(read_only=True)
    followingcount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['followerscount','followingcount']
    
    def get_followercount(self,obj):
        try:
            followers = obj.followers.all().count()
        except:
            followers = 0
        return followers

    def get_followingcount(self,obj):
        try:
            following = obj.following.all().count()
        except:
            following = 0
        return following


class UserprofileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(read_only=True)
    skills = SkillSerializer(read_only=True)
    interest = InterestSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '_all_'

    def get_profile_pic(self, obj):
        
        try:
            pic = obj.profile_pic.url
        except:
            pic = None
        return pic


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstname','lastname','username', 'profile', 'count']

    def get_profile(self,obj):
        proflie = obj.userprofile
        serializer = UserprofileSerializer(proflie,many=False)
        return serializer.data


    def get_count(self,obj):
        proflie = obj.userprofile
        serializer = CountSerializer(proflie,many=False)
        return serializer.data

class UserwithtokenSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude=['password']

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        token['username'] = obj.username
        token['first_name'] = obj.first_name
        token['last_name'] = obj.last_name
        # token['profile_pic'] = obj.userprofile.profile_pic.url
        token['id'] = obj.id
        return str(token.access_token)
    
    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)
        


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # token['profile_pic'] = user.userprofile.profile_pic.url
        token['id'] = user.id
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserwithtokenSerializer(self.user).data
        for k ,v in serializer.items():
            data[k] = v
        return data