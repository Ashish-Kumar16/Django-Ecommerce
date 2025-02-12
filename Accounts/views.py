from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, LoginSerializer
from base.models import Profile
import logging

logger = logging.getLogger(__name__)  # Logger for debugging

# ✅ User Registration View
class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate activation link
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{request.get_host()}/accounts/activate/{uidb64}/{token}/"

            email_subject = "Activate your account"
            message = f"Hi {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThanks,\nYour Website Team"

            send_mail(email_subject, message, 'your_email@example.com', [user.email])

            return Response({'message': 'User registered successfully! Please check your email for activation.'},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Email Activation View
@api_view(['GET'])
@permission_classes([AllowAny])
def activate_email_account(request, uidb64, token):
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        logger.info(f"Decoded UID: {uid}")

        user = User.objects.get(pk=uid)  # Ensure user exists

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return Response({'message': 'Invalid or expired activation token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate user profile
        profile, created = Profile.objects.get_or_create(user=user)  # Ensures Profile exists
        profile.is_email_verified = True
        profile.save()

        return Response({'message': 'Email successfully verified! You can now log in.'}, status=status.HTTP_200_OK)

    except (User.DoesNotExist, Profile.DoesNotExist):
        return Response({'message': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Activation error: {str(e)}")
        return Response({'message': 'Invalid activation link or token.'}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            # 🔹 Ensure user has a profile
            profile, created = Profile.objects.get_or_create(user=user)

            # 🔹 Block login if email is not verified
            if not profile.is_email_verified:
                return Response({'message': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)

            # 🔹 Proceed with login if verified
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful!', 'token': token.key}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Logout View (Token-Based)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Successfully logged out!'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'No active session found.'}, status=status.HTTP_400_BAD_REQUEST)
