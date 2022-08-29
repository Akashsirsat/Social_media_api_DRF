 
from social_api import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    # path('register/', RegisterAPI.as_view(), name='register'),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',knox_views.LogoutView.as_view()),
    path('followers/',views.followers,name="followers"),
    path('following/',views.following,name="following"),
    path('follow/',views.follow_user,name="follow"),
    path('unfollow/',views.unfollow_user,name="unfollow"),
    path('block_user/',views.block_another_user,name="block_user"),
    path('blocked_list/',views.blocked_user_list,name="blockedlist"),
    path('unblock/',views.unblock,name="unblock"),

]
