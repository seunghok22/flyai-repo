import base64
import openai
import requests
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Character
from .serializers import CharacterSerializer
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv("OPENAI")


def resize_image(image_bytes, max_size=(64, 64)):
    """이미지를 리사이징하여 Base64로 변환"""
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size)

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)
            return base64.b64encode(img_byte_arr.read()).decode("utf-8")
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def analyze_image(image_bytes, gender): 
    """GPT-4 Vision을 이용해 얼굴 분석 후 해시태그 추출"""
    base64_image = resize_image(image_bytes)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content" : "당신은 사람의 이목구비를 분석하고 특징적인 키워드를 해시태그 형식으로 추출하는 전문가입니다. 구어체로 자연스럽게 설명해주세요." },
            {"role": "system", "content" : "**이 {gender} 사람의 얼굴 특징을 분석하고 주요 얼굴 특징을 해시태그로 추출합니다. 해시태그 형식으로만 작성해주세요.**"},
            {"role": "user", "content": f"data:image/png;base64,{base64_image}"}
        ],
        max_tokens=100
    )
    return response["choices"][0]["message"]["content"].strip()

def generate_image_from_reference(keywords, gender):
    """DALL-E 3를 이용해 키워드를 기반으로 이미지 생성"""
    response = openai.Image.create(
        model="dall-e-3",
        prompt=f"""Create a portrait of a {gender} with exaggerated facial features based on: {keywords}. 
                   Use cubism style with sharp angles, geometric shapes, and contrasting colors. 
                   Ensure the face fills the entire frame with no other elements.""",
        size="1024x1024",
        n=1
    )
    return response["data"][0]["url"]

@csrf_exempt
@api_view(['POST'])
def process_image(request):
    """프론트엔드에서 이미지 URL을 받아 분석 후 새로운 이미지 생성"""
    try:
        image_file = request.FILES.get("image")
        gender = request.data.get("gender", "female")
        user_id = request.data.get('userID')
        
        if not user_id:
            return Response({'error': 'userID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if image_file == "none":
            return JsonResponse({"error": "Missing image_file"}, status=400)
        
        image_bytes =  image_file.read()
        keywords = analyze_image(image_bytes, gender)
        character_url = generate_image_from_reference(keywords, gender)

        character, created = Character.objects.update_or_create(
            userID=request.data.get('userID'),
            defaults={'imageUrl': character_url}
        )
        return JsonResponse({"keywords": keywords, "generated_image_url": character_url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def LoadCharacter(request):
    try:
        user_id = request.query_params.get('userID')

        if not user_id:
            return JsonResponse({'error': 'userID is required'}, status=400)

        character_profile = get_object_or_404(Character, userID=user_id)
        serializer = CharacterSerializer(character_profile)
        return Response({
             'message': 'UserProfile retrieved successfully',
            'data':serializer.data
            }, status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

