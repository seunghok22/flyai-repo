from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([AllowAny])
def CreateProfile(request):
    try:
        required_fields = ['category']
        if not all(field in request.data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        profile_data = {
            'category': request.data.get('category', []),
            'accountID': request.data.get('accountID'),
            'description': request.data.get('description', []),
            'tags': request.data.get('tags', []),
            'recentChats': request.data.get('recentChats', []),
            'prefor': request.data.get('prefor', []),
            'characterstics': request.data.get('characterstics', []),
            'additionalInfo': request.data.get('additionalInfo', {})
        }
        # UserProfile 생성
        serializer = UserProfileSerializer(data=profile_data)
        serializer.save()
        return Response({
            'message': 'UserProfile created successfully',
            'data': {'userID' : serializer.data['userID']}
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def LoadProfile(request):
    try:
        user_id = request.query_params.get('userID')
        if not user_id:
            return Response({'error': 'userID is required'}, status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(UserProfile, userID=user_id)
        serializer = UserProfileSerializer(profile)
        return Response({
            'message': 'UserProfile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def UpdateProfile(request):
    try:
        required_fields = ['userID']
        if not all(field in request.data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(userID=request.data['userID'])
        profile_data = {
            'category': request.data.get('category', []),
            'accountID': request.data.get('accountID'),
            'description': request.data.get('description', []),
            'tags': request.data.get('tags', []),
            'recentChats': request.data.get('recentChats', []),
            'prefor': request.data.get('prefor', []),
            'characterstics': request.data.get('characterstics', []),
            'additionalInfo': request.data.get('additionalInfo', {})
        }
        serializer = UserProfileSerializer(instance=user_profile, data=profile_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'UserProfile update complete',
                'data': {'userID' : serializer.data['userID']}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def DeleteProfile(request):
    try:
        # 필수 파라미터 확인
        user_id = request.query_params.get('userID')
        if not user_id:
            return Response({
                'error': 'userID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        # accountID와 userID 모두 일치하는 프로필 찾기
        profile = UserProfile.objects.filter(
            userID=user_id
        ).first()
        if not profile:
            return Response({
                'error': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        # 프로필 삭제
        profile.delete()
        return Response({
            'message': 'Profile successfully deleted',
            'data': {
                'userID': user_id
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def LoadProfileList(request):
    try:
        account_id = request.query_params.get('accountID')
        if not account_id:
            return Response({'error': 'accountID is required'}, status=status.HTTP_400_BAD_REQUEST)
        profiles = UserProfile.objects.filter(accountID=account_id)

        if not profiles.exists():
            raise Http404("No UserProfiles found with the given accountID")
    
        serializer = UserProfileSerializer(profiles)
        return Response({
            'message': 'successfull',
            'data': serializer.data
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def LoadFromCategory(request):
    try:
        required_fields = ['accountID','category']
        if not all(field in request.data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        account_id = request.query_params.get('accountID')
        category = request.query_params.get('category')
        profiles = UserProfile.objects.filter(
            accountID=account_id,
            category__contains=[category]  # 단일 카테고리를 리스트로 변환하여 검색
        )
        if not profiles.exists():
            raise Http404("No UserProfiles found with the given accountID and category")
        serializer = UserProfileSerializer(profiles, many=True)
        return Response({
            'message': 'successful',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Http404 as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)