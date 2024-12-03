
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import serializers, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from CreditCard.serializers import CreditCardSerializer
import CreditCard
from urllib.parse import urlencode

from authentication.models import User
from authentication.serializers import UserSerializer

from .mixins import PublicApiMixin, ApiErrorsMixin
from .utils import google_get_access_token, google_get_user_info
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from .models import User  # Asegúrate de que tu modelo User est importado

import requests

class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def post(self, request, *args, **kwargs):  
        input_serializer = self.InputSerializer(data=request.data)  
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google/'
        access_token = google_get_access_token(code=code, 
                                               redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)
        except User.DoesNotExist:
            username = user_data['email'].split('@')[0]
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = User.objects.create(
                username=username,
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                registration_method='google',
                phone_no=None,
                referral=None
            )
         
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)

class GoogleAuthRedirectApi(PublicApiMixin, APIView):
    """
    API View that either redirects the user to Google for authentication or
    returns the URL for the frontend to handle the redirection.
    """
    
    def get_google_login_url(self):
        """
        Constructs the Google OAuth2 login URL with required parameters.
        """
        params = { 
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'redirect_uri': f'{settings.BASE_FRONTEND_URL}',  #
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent'  
        }
        google_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(params)
        return google_url

    def get(self, request, *args, **kwargs):
        if request.GET.get('redirect', False):
            google_login_url = self.get_google_login_url()
            return redirect(google_login_url)
        
        return Response({'google_login_url': self.get_google_login_url()})

class GoogleAuthCallbackView(APIView):
    """
    API View to handle the callback from Google after authentication.
    """
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        print(f"Authorization code received: {code}")
        
        if not code:
            print("No code provided in the request.")
            return Response({'error': 'No code provided'}, status=400)

        token_url = 'https://oauth2.googleapis.com/token'
        params = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000/api/google-auth/callback',  
            'grant_type': 'authorization_code',
            'scope': 'email profile openid',  
        }

        try:
            response = requests.post(token_url, data=params)
            print(f"Token request response status: {response.status_code}")
        except Exception as e:
            print(f"Error while requesting token: {e}")
            return Response({'error': 'Failed to connect to Google token endpoint'}, status=500)

        if response.status_code != 200:
            print(f"Error response from Google: {response.text}")
            return Response({'error': 'Failed to obtain access token'}, status=response.status_code)

        token_data = response.json()
        print(f"Token data received: {token_data}")
        
        access_token = token_data.get('access_token')
        if not access_token:
            print("No access token received.")
            return Response({'error': 'No access token provided by Google'}, status=400)

        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        try:
            user_info_response = requests.get(user_info_url, 
                                              headers={'Authorization': f'Bearer {access_token}'})
            print(f"User info request response status: {user_info_response.status_code}")
        except Exception as e:
            print(f"Error while requesting user info: {e}")
            return Response({'error': 'Failed to connect to Google user info endpoint'}, status=500)

        if user_info_response.status_code != 200:
            print(f"Error response from Google UserInfo: {user_info_response.text}")
            return Response({'error': 'Failed to obtain user info'}, status=user_info_response.status_code)

        user_info = user_info_response.json()
        print(f"User info received: {user_info}")

        return Response(user_info)
    
