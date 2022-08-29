
from django.contrib.auth.models import User
from rest_framework import serializers, validators

from social_api.models import BlockUnblockUser, Follower


# Serializer for APIS
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['user_name','user_follower','user_following']

    

class Follow(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['user_name']


class BlockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockUnblockUser
        fields = ['blocked_by_user','blocked_user']

class Block_name(serializers.ModelSerializer):
    class Meta:
        model = BlockUnblockUser
        fields = ['blocked_user']       

    


#SERILIZERS FOR LOGIN AND SIGNUP

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        return user