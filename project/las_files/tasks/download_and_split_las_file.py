import os
from config.celery import celery
from django.db.models import Q
from django.utils import timezone
from las_files.services import download_las_file, split_las

from las_files.models import LasFileModel
import requests


@celery.task
def download_and_split_las_file(las_file_object_id, custom_splits_count=None) -> None:
    las_file_object = LasFileModel.objects.get(id=las_file_object_id)

    if not las_file_object.downloaded:
        with requests.get(las_file_object.remote_download_url, stream=True) as r:
            r.raise_for_status()
            with open(las_file_object.local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

        las_file_object.downloaded = True
        las_file_object.save()
        print(f"Las file {las_file_object.local_path} Downloaded")
    try:
        # if las_file_object.status == las_file_object.Status.NOT_CONVERTED:
        split_las(las_file_object, "output", custom_splits_count=custom_splits_count)
    finally:
        pass
        # if file and os.path.exists(file):
        #     os.remove(file)
        #     print(f"Temporary file {file} deleted.")
