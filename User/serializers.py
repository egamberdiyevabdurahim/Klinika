from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User, Bemor


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        data['refresh'] = attrs['refresh']
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = User.objects.get(username=self.user.username)
        data['status'] = user.status
        data['id'] = user.id
        return data


class UserSer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'status')

    def create(self, validated_data):
        user = super().create(self.validated_data)
        user.set_password(validated_data.pop('password', None))
        user.save()
        return user

    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class BemorSer(serializers.ModelSerializer):
    class Meta:
        model = Bemor
        fields = ('id', 'first_name', 'last_name', 'dad_name', 'phone', 'address', 'date', 'created_at')

