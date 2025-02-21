import os
from dotenv import load_dotenv
from django.shortcuts import redirect
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


User = get_user_model()

load_dotenv()

GOOGLE_SCOPE_USERINFO = os.getenv("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = os.getenv("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = os.getenv("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 로그인 페이지 연결
def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

# 구글 토큰 -> jwt
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def google_callback(request):
    print
    token = request.data.get('id_token')
    print(token)
    try:
        # Google의 ID 토큰 검증
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        print(idinfo)

        # 토큰에서 이메일 정보 추출
        email = idinfo['email']
        # 사용자 생성 또는 조회
        user, created = User.objects.get_or_create(email=email)
        
        # 사용자 로그인 처리
        # login(request, user)
        if created:
            user.save()
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }

        if created:
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_200_OK)

    except ValueError as e:
        print(str(e))
        return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
