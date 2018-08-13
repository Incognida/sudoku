from django.contrib.auth import get_user_model, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {
            "password":
                {
                    "write_only": True
                }
        }

    def create(self, validated_data):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        user_obj = User(
            username=username, email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password":
                {
                    "write_only": True
                }
        }

    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data['password']
        user = User.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user = user.first()
        else:
            raise ValidationError("Username does not exist")

        if not user.check_password(password):
            raise ValidationError("Password is incorrect")


        return data