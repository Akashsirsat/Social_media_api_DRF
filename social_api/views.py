from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes
from rest_framework import status
from social_api.models import BlockUnblockUser, Follower
from .serializers import Follow, FollowerSerializer, RegisterSerializer,Block_name
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#for returning usrname after registration
def serialize_user(user):
    return {
        "username": user.username,
    }

def get_followers(qs):
    followers_list={i.user_follower for i in qs}
    return str(followers_list)
 
def get_following(qs):
    followers_list={i.user_following for i in qs}
    return str(followers_list)

def get_blockedlist(qs):
    blocked_list={i.blocked_user for i in qs}
    return str(blocked_list)    

#post method for login
@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'token': token
    })
        

#post method for logout
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "User Registered Successfully": serialize_user(user),
            "token": token
        })


#APIS FOllow UNFOLLOW

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def followers(request):
    if request.method== 'GET':
        user=request.user
        qs=Follower.objects.filter(user_name=user)
        return Response({
            "Followers": get_followers(qs),
        })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def following(request):
    if request.method== 'GET':
        user=request.user
        qs=Follower.objects.filter(user_name=user)
        return Response({
            "user Following": get_following(qs),
        })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_user(request):
    if request.method== 'POST':
            py_obj=Follow(data=request.data)
            username= py_obj.initial_data['username']
            if username and User.objects.filter(username=username):
                Follower.objects.create(user_name=request.user,user_follower=User.objects.get(username=username),user_following=User.objects.get(username=username))
                return Response({'msg':"following"},status=status.HTTP_201_CREATED)
            else:return Response(status=status.HTTP_204_NO_CONTENT)
           
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    if request.method== 'POST':
            py_obj=Follow(data=request.data)
            username= py_obj.initial_data['username']
            if username and User.objects.filter(username=username):
                obj=Follower.objects.filter(user_follower=User.objects.get(username=username))
                obj.delete()
                return Response({'msg':"Unfollowed"},status=status.HTTP_200_OK)
            else:return Response(status=status.HTTP_204_NO_CONTENT)              
             


#APIS FOR BLOCK /UNBLOCK

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def blocked_user_list(request):
    if request.method== 'GET':
        user=request.user
        qs=BlockUnblockUser.objects.filter(blocked_by_user=user)
        return Response({
            "Followers": get_blockedlist(qs),
        })     

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def block_another_user(request):
    if request.method== 'POST':
            py_obj=Block_name(data=request.data)
            username= py_obj.initial_data.get('username')
            requested_user=request.user
            if username and User.objects.filter(username=username):
                BlockUnblockUser.objects.create(blocked_user=User.objects.get(username=username),blocked_by_user=User.objects.get(username=requested_user))
                Follower.objects.filter(user_follower=User.objects.get(username=username)).delete()
                
                return Response({'msg':"User Blocked"},status=status.HTTP_200_OK)
            else:return Response(status=status.HTTP_204_NO_CONTENT) 

         
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unblock(request):
    if request.method== 'POST':
            py_obj=Block_name(data=request.data)
            username= py_obj.initial_data.get('username')
            if username and User.objects.filter(username=username):
                BlockUnblockUser.objects.filter(blocked_by_user=User.objects.get(username=username)).delete()
                return Response({'msg':"Unblocked"},status=status.HTTP_200_OK)
            else:return Response(status=status.HTTP_204_NO_CONTENT)            