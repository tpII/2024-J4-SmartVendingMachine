from django.urls import path
from .views import *


urlpatterns = [
      path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
      path('login/', UserLoginView.as_view(), name='login'),
      path("auth/login/google/", GoogleLoginApi.as_view(), 
         name="login-with-google"),
      path('google-auth/', GoogleAuthRedirectApi.as_view(), name='google-auth'),
      path('google-auth/callback/', GoogleAuthCallbackView.as_view(), name='google-auth-callback')
]