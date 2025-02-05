from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import json

class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    @permission_classes([AllowAny])
    def post(self, request):
        print(request.body)
        try:
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('password')
            print(email)
            print(password)

            if not email or not password:
                return JsonResponse({
                    'error': 'Email and password are required.'
                }, status=400)
            print("auth")
            
            user = authenticate(request, username=email, password=password)
            
            if user is None:
                return JsonResponse({
                    'error': 'Invalid email or password.'
                }, status=401)

            if not user.is_active:
                return JsonResponse({
                    'error': 'Please verify your email before logging in.'
                }, status=403)

            # # FCM 토큰 업데이트
            # if fcm_token:
            #     user.fcm_token = fcm_token
            #     user.save()

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }

            # 로그인 처리
            login(request, user)

            return JsonResponse(tokens, status=200)

        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
