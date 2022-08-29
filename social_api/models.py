
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Follower(models.Model):
    user_name=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='user_name')
    user_following=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='following')
    user_follower=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='follower')


class BlockUnblockUser(models.Model):
    blocked_by_user=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='blocked_by_user')
    blocked_user=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='blocked_user')    





    
