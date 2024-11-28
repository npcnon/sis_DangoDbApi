# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from DangoDBApp.models import TblStudentBasicInfo,TblStudentOfficialInfo
from .models import User, Profile
from .serializers import TblStudentBasicInfoSerializer, UserSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
class RegisterView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        email = request.data.get('get')
        # Check if student_id exists in TblStudentBasicInfo
        # if not TblStudentOfficialInfo.objects.filter(student_id=student_id).exists():
        #     raise ValidationError('Student ID does not exist in TblStudentBasicInfo.')
        
        # if not TblStudentBasicInfo.objects.filter(email=email).exists():
        #     raise ValidationError('Student Email does not exist in TblStudentBasicInfo.')
        
        # Check if student_id is already used by another User
        
        if User.objects.filter(student_id=student_id).exists():
            raise ValidationError('Student ID is already registered.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Student Email is already registered.')
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        Profile.objects.get_or_create(user=user)

        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        print(request.data)
        identifier = request.data.get('identifier') 
        password = request.data.get('password')

        if not identifier or not password:
            raise AuthenticationFailed('Identifier and password are required')

        
        user = User.objects.filter(student_id=identifier).first()

        if user is None:
            user = User.objects.filter(email=identifier).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

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
            if len(auth_header.split(' ')) != 2:
                raise AuthenticationFailed('Invalid Authorization header format')
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token prefix')

            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Not Authenticated')

        user_profile = User.objects.get(id=user.id)

        student_info = TblStudentBasicInfo.objects.filter(email=user_profile.email).first()
        print("Student Info:", student_info)

        if student_info:
            student_info_serialized = TblStudentBasicInfoSerializer(student_info).data
        else:
            student_info_serialized = None

        user_data = UserSerializer(user_profile).data
        user_data['profile']['student_info'] = student_info_serialized
        print("User Data:",user_data)
        return Response(user_data)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    # If blacklisting fails, we can still return success
                    # since the frontend will remove the tokens anyway
                    pass
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        # This view handles refreshing the access token using the refresh token
        return super().post(request, *args, **kwargs)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the current user
        user = request.user

        # Validate old password
        old_password = request.data.get('old_password')
        if not user.check_password(old_password):
            raise AuthenticationFailed('Current password is incorrect')

        # Get and validate new password
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            raise ValidationError('New password and confirmation are required')

        if new_password != confirm_password:
            raise ValidationError('New passwords do not match')

        # Check password complexity (optional, but recommended)
        if len(new_password) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        # Set and save the new password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'})


class PasswordResetRequestView(APIView):
    def post(self, request):
        # Get identifier from request (can be email or student_id)
        identifier = request.data.get('identifier')
        
        if not identifier:
            raise ValidationError('Email or Student ID is required')

        # Find user by email or student_id
        user = (
            User.objects.filter(email=identifier).first() or 
            User.objects.filter(student_id=identifier).first()
        )
        
        if not user:
            # For security, return success even if account not found
            return Response({
                'message': 'If an account exists with this email or student ID, a password reset link will be sent'
            })

        # Generate a secure reset token
        reset_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        
        # Store the reset token
        user.password_reset_token = reset_token
        user.save()

        # Construct reset link (adjust the URL as needed)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        # Send email
        try:
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error
            print(f"Email send error: {e}")
            raise ValidationError('Failed to send password reset email')

        return Response({
            'message': 'Password reset link has been sent to your email'
        })
    
    
class PasswordResetConfirmView(APIView):
    def post(self, request):
        # Get reset token and new password
        reset_token = request.data.get('reset_token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Validate inputs
        if not reset_token or not new_password or not confirm_password:
            raise ValidationError('All fields are required')

        if new_password != confirm_password:
            raise ValidationError('Passwords do not match')

        # Find user with the reset token
        user = User.objects.filter(password_reset_token=reset_token).first()
        
        if not user:
            raise AuthenticationFailed('Invalid or expired reset token')

        # Optional: Add token expiration check
        # You'd need to add a password_reset_token_expires_at field to your User model

        # Set and save the new password
        user.set_password(new_password)
        
        # Clear the reset token
        user.password_reset_token = None
        user.save()

        return Response({'message': 'Password reset successfully'})