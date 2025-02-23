from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import os

class AudioProcessView(APIView):
    def post(self, request):
        try:
            ## 전달받은 wav -> aws서버에 올라간 stt 모델 돌리기
            ## 결과 형식: [{'audio': 'path/to/clip', 'time': '0.0-5.0', 'text': 'transcript'}, ...]
            ## audio를 aws서버에 올라간 임베딩 모델로 돌리기
            ## 결과 형식 [{embedding data}, {...}, {...}, ...]
            ## 모든 userprofile 받아서 코싸인 비교해서 변환
            ## 결과 형식: [{"userID":'userID', 'TIME': '0.0-5.0', "TEXT":"hello, my name is ..."}, {data}, {data}, ...]

            # 프론트에서 전달된 음성 파일 받기
            audio_file = request.FILES.get('audio')
            if not audio_file:
                return Response(
                    {"error": "No audio file provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 파일 임시 저장
            temp_path = f'temp_{audio_file.name}'
            with open(temp_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # AI 모델로 음성 처리 (process_audio는 가정된 함수)
            # 결과 형식: [{'audio_clip': 'path/to/clip', 'time': '0.0-5.0', 'text': 'transcript'}, ...]
            # processed_result = process_audio(temp_path)

            # 결과를 프론트로 전달하기 위한 준비
            # response_data = []
            # for result in processed_result:
            #     response_data.append({
            #         'audio_clip': result['audio_clip'],  # 자른 음성 파일 경로
            #         'time': result['time'],             # 시간 구간
            #         'text': result['text']              # 변환된 텍스트
            #     })

            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # return Response(
            #     {"results": response_data},
            #     status=status.HTTP_200_OK
            # ) # 프론트로 데이터 전달

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
