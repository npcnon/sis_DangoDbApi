# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed('Email and password are required')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not Found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return the tokens in the response body
        return Response({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token
        })



class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                raise AuthenticationFailed('No Authorization header provided')

            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token prefix')

            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Not Authenticated')

        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        # In a stateless JWT system, there's no need to delete cookies. 
        # You just need to inform the client to delete the token from local storage or state.

        return Response({
            'message': 'Logout successful'
        })


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # This view handles refreshing the access token using the refresh token
        return super().post(request, *args, **kwargs)
