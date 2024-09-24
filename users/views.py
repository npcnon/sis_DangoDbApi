    # views.py

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from DangoDBApp.models import TblStudentBasicInfo
    from .models import User, Profile
    from .serializers import TblStudentBasicInfoSerializer, UserSerializer
    from rest_framework.exceptions import AuthenticationFailed, ValidationError
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.permissions import IsAuthenticated
    from rest_framework_simplejwt.views import TokenRefreshView

    class RegisterView(APIView):
        def post(self, request):
            student_id = request.data.get('student_id')
            
            # Check if student_id exists in TblStudentBasicInfo
            if not TblStudentBasicInfo.objects.filter(student_id=student_id).exists():
                raise ValidationError('Student ID does not exist in TblStudentBasicInfo.')

            # Check if student_id is already used by another User
            if User.objects.filter(student_id=student_id).exists():
                raise ValidationError('Student ID is already registered.')

            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()
            Profile.objects.get_or_create(user=user)

            return Response(serializer.data)


    class LoginView(APIView):
        def post(self, request):
            student_id = request.data.get('student_id')
            password = request.data.get('password')

            if not student_id or not password:
                raise AuthenticationFailed('Student ID and password are required')

            user = User.objects.filter(student_id=student_id).first()

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




    # In your views
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

            # Fetch the user
            user_profile = User.objects.get(id=user.id)

            # Fetch the student's info using the student_id
            student_info = TblStudentBasicInfo.objects.filter(student_id=user_profile.student_id).first()

            # If student info exists, serialize it
            if student_info:
                student_info_serialized = TblStudentBasicInfoSerializer(student_info).data
            else:
                student_info_serialized = None

            # Serialize the user's profile along with the student info
            user_data = UserSerializer(user_profile).data
            user_data['profile']['student_info'] = student_info_serialized

            return Response(user_data)



    class LogoutView(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            try:
                refresh_token = request.data.get('refresh_token')
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful'})
            except Exception as e:
                return Response({'error': str(e)}, status=400)


    class RefreshTokenView(TokenRefreshView):
        def post(self, request, *args, **kwargs):
            # This view handles refreshing the access token using the refresh token
            return super().post(request, *args, **kwargs)
