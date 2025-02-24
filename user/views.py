import os
from dotenv import load_dotenv
from django.shortcuts import redirect
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
import firebase_admin
from firebase_admin import credentials, initialize_app

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
        service_account_path = "/home/ubuntu/myproject/flyai-repo/serviceAccountKey.json"
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            initialize_app(cred)
            message = "Firebase 서비스 계정 키가 정상적으로 로드되어 Firebase가 초기화되었습니다."
        else:
            message = "Firebase가 이미 초기화되어 있습니다."
        
        data = json.loads(request.body)
        id_token = data.get("id_token")
        # id token -> email, access, refresh, 
        if not id_token:
            return JsonResponse({"error": "Missing id_token"}, status=400)

        # Firebase에서 ID Token 검증
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        email = uid.email
        email2 = decoded_token.get("email")

        if not email:
            if not email2:
                return JsonResponse({"error": "Invalid token"}, status=400)
            else:
                user, created = User.objects.get_or_create(email=email2)
        else:
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