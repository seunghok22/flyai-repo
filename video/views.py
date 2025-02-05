from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializers import VideoListSerializer, VideoCreateSerializer
from .utils import S3PresignedUrlGenerator

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return VideoCreateSerializer
        return VideoListSerializer

    @action(detail=False, methods=['post'])
    def presigned_url(self, request):
        """Generate presigned URLs for video and thumbnail upload"""
        try:
            s3_generator = S3PresignedUrlGenerator()
            print("click1")
            # Generate presigned POST data for both video and thumbnail
            video_data = s3_generator.generate_presigned_post('video')
            thumbnail_data = s3_generator.generate_presigned_post('thumbnail')
            
            return Response({
                'video': video_data,
                'thumbnail': thumbnail_data
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        """Create video record after successful S3 upload"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response(
                VideoListSerializer(video).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Provide personalized video feed"""
        videos = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)