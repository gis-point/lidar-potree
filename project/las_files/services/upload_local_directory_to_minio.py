import glob
import os

from config.instances import MINIO_CLIENT_INSTANCE
from config.celery import celery


@celery.task
def upload_local_directory_to_minio(local_path, bucket_name, minio_path):
    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + "/**"):
        local_file = local_file.replace(os.sep, "/")  # Replace \ with / on Windows
        if not os.path.isfile(local_file):
            upload_local_directory_to_minio.delay(
                local_file, bucket_name, minio_path + "/" + os.path.basename(local_file)
            )
        else:
            remote_path = os.path.join(minio_path, local_file[1 + len(local_path) :])
            remote_path = remote_path.replace(
                os.sep, "/"
            )  # Replace \ with / on Windows
            MINIO_CLIENT_INSTANCE.fput_object(bucket_name, remote_path, local_file)
