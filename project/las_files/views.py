from typing import Type

from config.serializers import BaseBulkSerializer
from django.db.models import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from las_files.tasks import download_and_split_las_file
from las_files.models import LasFileModel
from las_files.serializers import LoadLasFileSerializer, LasFileDetailsSerializer
from config.exceptions import ObjectNotFoundException

from urllib.parse import urlparse
import os


class LoadLasFile(GenericAPIView):
    serializer_class = LoadLasFileSerializer
    authentication_classes = []  # disables authentication
    permission_classes = []

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_name_with_extension = ''
        file_name  = ''
        is_file_downloaded = False
        remote_download_url = serializer.validated_data["file_url"]

        if not serializer.validated_data["local_file_url"]:
            parsed_url = urlparse(remote_download_url)
            file_name_with_extension = os.path.basename(parsed_url.path)

        else:
            file_name_with_extension = serializer.validated_data["local_file_url"]
            is_file_downloaded = True
        file_name = os.path.splitext(file_name_with_extension)[0]

        lasFiles = LasFileModel.objects.filter(name=file_name)

        las_file_object = None
        if not lasFiles.exists():
            las_file_object = LasFileModel.objects.create(
                name=file_name,
                local_path=file_name_with_extension,
                remote_download_url=remote_download_url,
                downloaded=is_file_downloaded
            )
        else:
            las_file_object = LasFileModel.objects.get(
                name=file_name,
            )
        download_and_split_las_file.delay(
            las_file_object.id, serializer.validated_data["custom_splits_count"]
        )
        return Response(LasFileDetailsSerializer(las_file_object).data, HTTP_200_OK)


class LasFileDetails(GenericAPIView):
    serializer_class: Type[Serializer] = LasFileDetailsSerializer
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request, name: int) -> Response:
        las_files = LasFileModel.objects.filter(name=name)
        if las_files.exists():
            serializer = self.serializer_class(las_files.first())
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            raise ObjectNotFoundException(object=LasFileModel)


class LoadedLasFilesList(ListAPIView):
    serializer_class: Type[Serializer] = LasFileDetailsSerializer
    authentication_classes = []
    permission_classes = []
    queryset = LasFileModel.objects.all()
