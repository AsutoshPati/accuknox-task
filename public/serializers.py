from datetime import datetime
import re

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers

from accuknox.utils import make_password
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = ['']
        # exclude = ['uid']
        fields = '__all__'

    def validate(self, data):
        errors = dict()

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                for i in unknown_keys:
                    errors.update({i: ["Got unknown field"]})
                raise serializers.ValidationError({"errors": errors})

        if 'name' in data:
            data['name'] = data['name'].strip().title()
            errs = []

            if not 2 <= len(data['name']) <= 50:
                errs.append('Name must be limited in between 2 to 50 characters')

            if not re.search("^[A-Za-z\s]{1,}[A-Za-z\s\.\']{0,}[A-Za-z\s]{0,}$", data['name']):
                errs.append('Name must not contain any special characters or digits')

            if errs:
                errors.update({'name': errs})

        if 'email' in data:
            data['email'] = data['email'].strip().lower()
            user = User.objects.filter(email=data['email']).first()
            if user:
                errors.update({'email': ['User with this mail already exists.']})

        if 'gender' in data:
            if data['gender'] not in ['M', 'F', 'O']:
                errors.update({'gender': ['Please an valid option from M/F/O.']})

        if 'dob' in data:
            if datetime.now().date() <= data['dob']:
                errors.update({'dob': ["Date of Birth can't be a future date or today."]})

        if 'city' in data:
            data['city'] = data['city'].strip()

        if 'state' in data:
            data['state'] = data['state'].strip()

        if 'bio' in data:
            data['bio'] = data['bio'].strip()

        if 'password' in data:
            if validate_password(data['password']) is None:
                data['password'] = make_password(data['password'])

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['uid', 'email', 'dob', 'password', 'created_at', 'last_updated_at', 'is_active']


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ['username', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        errors = dict()

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                for i in unknown_keys:
                    errors.update({i: ["Got unknown field"]})
                raise serializers.ValidationError({"errors": errors})

        if 'email' in data:
            data['email'] = data['email'].strip().lower()

        if 'password' in data:
            data['password'] = make_password(data['password'])

        return data
