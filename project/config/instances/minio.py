from django.conf import settings
from minio import Minio


print(settings.MINIO_ENDPOINT, 'settings.MINIO_ENDPOINT')
MINIO_CLIENT_INSTANCE: Minio = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)
