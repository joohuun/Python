from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token