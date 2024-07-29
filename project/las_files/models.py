from django.db import models
from uuid import uuid4
from django.conf import settings
from config.instances import MINIO_CLIENT_INSTANCE

# Create your models here.


class LasFileModel(models.Model):
    class Status(models.TextChoices):
        NOT_CONVERTED: str = "not_converted"
        CONVERTING: str = "converting"
        CONVERTED: str = "converted"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    local_path = models.CharField(max_length=100000)
    remote_download_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=Status.choices, max_length=100, default=Status.NOT_CONVERTED
    )
    name = models.CharField(max_length=100000)
    downloaded = models.BooleanField(default=False)
    deleted_from_local_path = models.BooleanField(default=False)

    @property
    def relative_converted_las_files_base_path(self):
        return f"potreeConverter/{self.name}"

    @property
    def absolute_converted_las_files_base_path(self):
        return f"{settings.MINIO_IMAGES_HOST}/{settings.MINIO_MEDIA_FILES_BUCKET}/{self.relative_converted_las_files_base_path}"

    @property
    def all_splited_and_converted_folders_paths(self):
        objects = list(
            MINIO_CLIENT_INSTANCE.list_objects(
                settings.MINIO_MEDIA_FILES_BUCKET,
                self.relative_converted_las_files_base_path,
                recursive=True,
            )
        )

        # Extract the object names
        object_names = [obj.object_name for obj in objects]

        # Define the base folder
        base_folder = self.relative_converted_las_files_base_path

        # Extract unique folder paths within the base folder
        folder_paths = set()
        for name in object_names:
            relative_path = name[len(base_folder) :].strip("/")
            if "/" in relative_path:
                folder = relative_path.split("/")[0]
                folder_paths.add(f"{folder}")

        # Convert set to sorted list
        folder_paths = sorted(folder_paths)

        return folder_paths
