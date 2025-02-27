from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import JsonHandleSerializer
from .models import JsonHandle

@api_view(['POST'])
@permission_classes([AllowAny])
def SaveJson(request):
    json_data = request.data  # 요청 데이터 가져오기
    try:
        # Serializer에 데이터 전달
        serializer = JsonHandleSerializer(data=json_data)

        # 데이터 유효성 검사
        if serializer.is_valid():
            # 유효한 경우 데이터 저장
            serializer.save()
            return Response({
                "message": "데이터가 성공적으로 저장되었습니다.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # 유효하지 않은 경우 에러 반환
        return Response({
            "message": "유효하지 않은 데이터입니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except json.JSONDecodeError:
        return Response({
            "message": "올바른 JSON 형식이 아닙니다."
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "message": "처리 중 오류가 발생했습니다.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def LoadJson(request):
    try:
        # 쿼리 파라미터에서 id 가져오기
        item_id = request.query_params.get('id', None)
        
        # id가 제공되지 않은 경우
        if not item_id:
            return Response({
                "message": "ID 파라미터가 필요합니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        # UUID로 특정 데이터 조회
        try:
            json_handle = JsonHandle.objects.get(id=item_id)
        except JsonHandle.DoesNotExist:
            return Response({
                "message": f"ID {item_id}에 해당하는 데이터가 없습니다."
            }, status=status.HTTP_404_NOT_FOUND)

        # Serializer를 통해 데이터 직렬화 (단일 객체이므로 many=False)
        serializer = JsonHandleSerializer(json_handle)

        return Response({
            "message": "데이터를 성공적으로 불러왔습니다.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except ValueError:
        # UUID 형식이 잘못된 경우
        return Response({
            "message": "유효하지 않은 ID 형식입니다."
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "message": "데이터 조회 중 오류가 발생했습니다.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

