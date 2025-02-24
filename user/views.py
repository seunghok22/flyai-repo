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
from firebase_admin import auth
from django.http import JsonResponse
import json

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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def google_callback(request):
    try:
        data = json.loads(request.body)
        id_token = data.get("id_token")
        # id token -> email, access, refresh, 
        print(auth)
        if not id_token:
            return JsonResponse({"error": "Missing id_token"}, status=400)

        # Firebase에서 ID Token 검증
        decoded_token = auth.verify_id_token(id_token)
        print("decoded : ",decoded_token)
        uid = decoded_token.get("uid")
        email = uid.email
        email2 = decoded_token.get("email")

        if not email:
            return JsonResponse({"error": "Invalid token"}, status=400)

        # 기존 유저 확인 or 생성
        user, created = User.objects.get_or_create(email=email)

        return JsonResponse({
            "message": "Login successful",
            "email": user.email,
            "is_new_user": created
        })
    except auth.ExpiredIdTokenError:
        return JsonResponse({"error": "ID token has expired. Please obtain a new token."}, status=401)
    except auth.InvalidIdTokenError:
        return JsonResponse({"error": "Invalid ID Token"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)