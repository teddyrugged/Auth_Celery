# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from .serializers import *
from .tasks import send_verification_email
from drf_spectacular.utils import extend_schema, OpenApiParameter
from utils.response import build_response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import ValidationError

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email.delay(user.id)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(build_response(True, "A Token has been sent to your Email"), status=response.status_code)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            message = list(e.detail.values())[0][0]  # Get the first error message
            return Response(
                build_response(False, message, None),
                status=status.HTTP_400_BAD_REQUEST
            )


        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(build_response(True, "Login successful", tokens), status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refreshToken"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            # return Response(build_response(True, "Logout successful"), status=status.HTTP_205_RESET_CONTENT)
            return Response(build_response(True, "Logout successful"), status=status.HTTP_200_OK)

        except TokenError as e:
            return Response(build_response(False, f"Logout failed: {str(e)}"), status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(build_response(False, "Logout failed"), status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_object()).data
        return Response(build_response(True, "Profile fetched", data), status=status.HTTP_200_OK)

    





@extend_schema(
    parameters=[
        OpenApiParameter(name="token", description="Email verification token", required=True, type=str)
    ]
)
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True
            user.verification_token = None
            user.save()
            return Response(build_response(True, "Account verified"), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(build_response(False, "Invalid verification token"), status=status.HTTP_400_BAD_REQUEST)
