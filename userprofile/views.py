from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
            'description': request.data.get('description', []),
            'tags': request.data.get('tags', []),
            'recentChats': request.data.get('recentChats', []),
            'prefor': request.data.get('prefor', []),
            'voiceVector': request.data.get('voiceVector',[]),
            'additionalInfo': request.data.get('additionalInfo', {}),
            'accountID':{"email":request.user.email}.get("id_token"),
            'characterstics':request.data.get('characterstics',{}),
            }
        # UserProfile 생성
        serializer = UserProfileSerializer(data=profile_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'UserProfile created successfully',
                'data': {'userID' : serializer.data['userID']}
            }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def LoadProfile(request):
    try:
        user_id = request.data.get('userID')
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
        user_id = request.data.get('userID')
        if not user_id:
            return Response({'error': "userID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profile = UserProfile.objects.get(userID=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': "userID does not exist"}, status=status.HTTP_404_NOT_FOUND)

        update_data ={'voiceVector', 'category', 'accountID', 'description','tags', 'recentChats', 'prefor', 'additionalInfo', 'characterstics'}
        profile_data ={}

        for field in update_data:
            if field in request.data:
                profile_data[field] = request.data[field]

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
@permission_classes([IsAuthenticated])
def DeleteProfile(request):
    try:
        account_id={"email":request.user.email}.get("id_token")

        profiles = UserProfile.objects.filter(
            accountID=account_id)
        if not profiles:
            return Response({
                'error': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        # 프로필 삭제
        profiles.delete()
        return Response({
            'message': 'Profiles successfully deleted',
            'data': {
                'accountID': account_id
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LoadProfileList(request):
    try:
        account_id ={"email": request.user.email}.get("id_token")
        profiles = UserProfile.objects.filter(accountID=account_id).only('userID', 'category', 'tags')

        if not profiles.exists():
            raise Http404("No UserProfiles found with the given accountID")
    
        serializer = UserProfileSerializer(profiles, many=True)
        return Response({
            'message': 'successfull',
            'data': serializer.data
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LoadFromCategory(request):
    try:
        required_fields = ['category']
        if not all(field in request.data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        account_id = JsonResponse({"email": request.user.email})
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
