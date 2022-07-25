from curses import keyname
from dataclasses import field
import requests
from tokenize import Token
from urllib import response
from django.shortcuts import render
from django.contrib.auth.models import User
from mainapp.models import shortcut
from mainapp.serializers import DeleteShortcutSerializer, FilterShortcutSerializer, ListShortcutSerializer, LoginSerializer, RegisterSerializer
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import *
from rest_framework import generics, permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
#from django.http import request
from django.http import HttpResponse
from .forms import *
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
#@permission_classes([AllowAny,])
def signup(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create_user(username,email,password)
            token = Token.objects.get(user=user)
            data = {
                "response":"User Created",
                "token":token.key
            }
            return Response(data,status=200)
        else:
            return Response(serializer.errors,status=406)
    else:
        return Response(status=404)


@api_view(['POST'])
@permission_classes([])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                token = Token.objects.get(user=user)
                data = {
                    "response":"Login success",
                    "token":token.key
                }
                return Response(data,status=200)
            else:
                data = {
                    "response" : "Invalid credentials"
                }
                return Response(data,status=400)
        else:
            return Response(serializer.errors,status=406)
    else:
        return Response(status=404)


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def logout(request):
    request.user.auth_token.delete()
    logout(request)
    return response("User logged out successfully",status=200)





        
# def redirect_url_view(request, shortened_part):
#     try:
#         shortener = shortcut.objects.get(shortlink=shortened_part)      
#         shortener.save()
#         return HttpResponseRedirect(shortcut.url)
#     except:
#         raise Http404('Sorry this link is broken :(')


# def home_view(request):

#     template = 'urlshortener/home.html'
#     context = {}
#     context['form'] = ShortenerForm()

#     if request.method == 'GET':
#         return render(request, template, context)
    
#     elif request.method == 'POST':
#         used_form = ShortenerForm(request.POST)
#         if used_form.is_valid():
#             shortened_object = used_form.save()


# def redirect_url_view(request, shortened_part):

#     try:
#         shortener = shortcut.objects.get(shortlink=shortened_part)     
#         shortener.save()
#         return HttpResponseRedirect(shortener.long_url)
#     except:
#         raise Http404('Sorry this link is broken :(')


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def listshortcuts(request):
    if request.method == 'GET':
        try:
            obj = shortcut.objects.filter(user=request.user)
            serializer = ListShortcutSerializer(obj,many=True)
            return Response(serializer.data)
        except:
            data = {}
            data ["Error"] = "No data found"
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def deleteshortcuts(request):
    if request.method == 'POST':
        serializer = DeleteShortcutSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data['id']
            obj = shortcut.objects.get(id=id)
            obj.delete()
            return Response("Shortcut deleted")


@api_view(['POST'])
def filtershortcuts(request):
    if request.method == 'POST':
        serializer = FilterShortcutSerializer(data=request.data)
        if serializer.is_valid():
            short = serializer.validated_data['shortlinkstring']
            desc = serializer.validated_data['description']
            tags = serializer.validated_data['tags']
            if shortcut.objects.filter(shortlink=short).exists() and shortcut.objects.filter(description=desc).exists() and shortcut.objects.filter(tags=tags).exists():
                data = {
                    "shorturl" : short,
                    "description" : desc,
                    "tags" : tags
                }
                return Response(data)
            else:
                return Response("Query does not exists")