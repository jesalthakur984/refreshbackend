from django.shortcuts import render
import email_validator
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Interest, Skill, UserProfile, User
from .seralizers import InterestSerializer, SkillSerializer, TokenSerializer, UserForPostSerializer, CountSerializer, UserprofileSerializer, UserSerializer, UserwithtokenSerializer
from email_validator import validate_email, EmailNotValidError
from rest_framework.views import APIView
from rest_framework import permissions, status
import re
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

# Create your views here.

def email_checked(email):
    try:
        validate_email_data = validate_email(email)
        email_add = validate_email_data['email']
        return email_add
    except EmailNotValidError as e:
        return str(e)

class Registerview(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self,request):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        check_email = email_checked(email)
        messages = {'errors':[]}
        if username == None:
            messages['errors'].append('EMPTY_USERNAME')

        if email == None:
            messages['errors'].append('EMPTY_EMAIL')

        if password == None:
            messages['errors'].append('EMPTY_PASSWORD')

        if not check_email == email:
            messages['errors'].append('INVALID_EMAIL')
        
        if len(password)<8 or re.search('[0-9]',password) is None or len(password) > 20 or re.search('[0-9]',password) is None or re.search("[_@$]", password) is None:
            messages['errors'].append('INVALID_PASSWORD')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages['errors'].append('ALREADY_EXISTS')

        if len(messages['errors']):
            return Response({"details":messages['errors']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user=User.objects.create(username=username, email=email, password=make_password(password))
            serializer=UserwithtokenSerializer(user,many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({"details":f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = TokenSerializer
