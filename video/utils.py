import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import uuid
from datetime import datetime

class S3PresignedUrlGenerator:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def _generate_key(self, file_type='video'):
        """Generate a unique S3 key"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        folder = 'videos' if file_type == 'video' else 'thumbnails'
        return f"{folder}/{timestamp}_{unique_id}"

    def generate_presigned_post(self, file_type='video'):
        """Generate presigned POST data for S3 upload"""
        key = self._generate_key(file_type)
        
        # Set conditions based on file type
        conditions = [
            ["content-length-range", 0, 100 * 1024 * 1024]  # 100MB max for videos
        ]
        
        if file_type == 'video':
            conditions.append(["eq", "$Content-Type", "video/mp4"])
        elif file_type == 'thumbnail':
            conditions.append(["starts-with", "$Content-Type", "image/"])
            conditions[0] = ["content-length-range", 0, 5 * 1024 * 1024]  # 5MB max for thumbnails

        try:
            response = self.s3_client.generate_presigned_post(
                Bucket=self.bucket_name,
                Key=key,
                Fields={
                    'acl': 'public-read',
                },
                Conditions=conditions,
                ExpiresIn=3600
            )
            
            return {
                'presigned_data': response,
                'file_url': f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}",
                'key': key
            }
        except ClientError as e:
            print(f"Error generating presigned URL: {str(e)}")
            raise

    def generate_presigned_url_for_get(self, s3_key, expiration=3600):
        """Generate a presigned URL for retrieving an object"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {str(e)}")
            return None