
from django.contrib import admin
from social_api.models import User,Follower,BlockUnblockUser

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display=['user_name','user_follower','user_following']


@admin.register(BlockUnblockUser)
class BlockUnblockUser(admin.ModelAdmin):
    list_display=['blocked_by_user','blocked_user']
         