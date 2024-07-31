from rest_framework.serializers import (
    CharField,
    Serializer,
    ModelSerializer,
    IntegerField,
)
from las_files.models import LasFileModel


class LoadLasFileSerializer(Serializer):
    file_url: str = CharField(required=False, allow_null=True, max_length=100000)
    custom_splits_count = IntegerField(required=False, allow_null=True)
    local_file_url = CharField(required=False, allow_null=True, max_length=100000)

    class Meta:
        fields = ["file_url", "custom_splits_count", "local_file_url"]


class LasFileDetailsSerializer(ModelSerializer):

    class Meta:
        model = LasFileModel
        fields = [
            "id",
            "name",
            "local_path",
            "remote_download_url",
            "created_at",
            "status",
            "downloaded",
            "deleted_from_local_path",
            "relative_converted_las_files_base_path",
            "absolute_converted_las_files_base_path",
            "all_splited_and_converted_folders_paths",
        ]


class NewConvertedLasFileSerializer(ModelSerializer):

    class Meta:
        model = LasFileModel
        fields = [
            "id",
            "name",
            "local_path",
            "remote_download_url",
            "created_at",
            "status",
            "relative_converted_las_files_base_path",
            "absolute_converted_las_files_base_path",
        ]
