import re

from rest_framework import serializers

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=50)
    password2 = serializers.CharField(max_length=50)
    
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'date_of_birth',
        ]
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")

        if len(data['password1']) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters")

        if re.search(r'\d', data['password1']) == None:
            raise serializers.ValidationError("Password should have at least 1 digit")

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
        )
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    # token = serializers.CharField(
    #     label=_("Token"),
    #     read_only=True
    # )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
