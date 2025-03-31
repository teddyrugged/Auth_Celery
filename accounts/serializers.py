# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value



    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if user.is_locked:
            raise serializers.ValidationError("Account is locked. Please contact support.")

        user_auth = authenticate(username=username, password=password)
        if not user_auth:
            user.failed_login_attempts += 1
            attempts_left = 3 - user.failed_login_attempts

            if user.failed_login_attempts >= 3:
                user.lock_account()
                raise serializers.ValidationError("Account locked after 3 failed login attempts. Please contact support.")
            else:
                user.save(update_fields=["failed_login_attempts"])
                raise serializers.ValidationError(f"Invalid password. {attempts_left} login attempt(s) remaining.")

        user.failed_login_attempts = 0
        user.save(update_fields=["failed_login_attempts"])
        return user

class LogoutSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()




    
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        # Explicitly tell Swagger the token is a query parameter
        kwargs['data'] = kwargs.get('data') or kwargs.get('query_params')
        super().__init__(*args, **kwargs)
















