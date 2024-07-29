import laspy
import os
import numpy as np
from shutil import rmtree
from las_files.services.use_potree_converter import use_potree_converter
from las_files.services.upload_local_directory_to_minio import (
    upload_local_directory_to_minio,
)
from las_files.tasks.send_to_socket import send_to_general_layer
from las_files.serializers import NewConvertedLasFileSerializer

from django.conf import settings


def split_las(
    las_file_object,
    output_base,
    num_points_per_file=4000000,
    custom_splits_count=None,
    max_file_size_mb=40000,
):
    input_las_file = laspy.file.File(las_file_object.local_path, mode="r")

    # Get number of points in the input LAS file
    total_points = len(input_las_file)

    # Calculate the maximum number of points to read based on the max file size
    max_file_size_bytes = max_file_size_mb * 1024 * 1024
    point_size = input_las_file.header.data_record_length
    max_points = max_file_size_bytes // point_size

    # Limit total points to the max points that fit within the max file size
    total_points = min(total_points, max_points)

    # Calculate number of splits needed
    num_splits = int(np.ceil(total_points / num_points_per_file))

    if custom_splits_count:
        custom_splits_count = custom_splits_count - 1

        if custom_splits_count < 0:
            custom_splits_count = 0
        if custom_splits_count > num_splits:
            custom_splits_count = num_splits

        num_splits = custom_splits_count

    output_files_base_dir = f"./PotreeConverter/build/out/{las_file_object.name}"

    las_file_object.status = las_file_object.Status.CONVERTING
    las_file_object.save()

    print(num_splits, custom_splits_count)

    # Iterate through each split
    for i in range(num_splits):
        start_index = i * num_points_per_file
        end_index = min((i + 1) * num_points_per_file, total_points)

        # Extract subset of points
        points_subset = input_las_file.points[start_index:end_index]

        # Create a new LAS file for the subset
        output_file_name_without_extension = f"{output_base}_{i}"

        if not os.path.exists(output_files_base_dir):
            os.makedirs(output_files_base_dir)

        output_las_file_path = (
            f"{output_files_base_dir}/{output_file_name_without_extension}.las"
        )
        output_las_file = laspy.file.File(
            output_las_file_path, mode="w", header=input_las_file.header
        )

        # Write points to the new LAS file
        output_las_file.points = points_subset

        # Close the output LAS file
        output_las_file.close()

        potree_converter_output_path = f"{output_files_base_dir}/potreeConverter/{output_file_name_without_extension}"

        use_potree_converter(output_las_file_path, potree_converter_output_path)

        remote_path_to_upload_on_minio = f"{las_file_object.relative_converted_las_files_base_path}/{output_file_name_without_extension}"

        upload_local_directory_to_minio(
            potree_converter_output_path,
            settings.MINIO_MEDIA_FILES_BUCKET,
            remote_path_to_upload_on_minio,
        )

        rmtree(potree_converter_output_path)
        os.remove(output_las_file_path)

        send_to_general_layer(
            "new_converted_las_file",
            {
                "folder_url": f"{settings.MINIO_IMAGES_HOST}/{settings.MINIO_MEDIA_FILES_BUCKET}/{remote_path_to_upload_on_minio}",
                "base_provided_las_file_data": NewConvertedLasFileSerializer(
                    las_file_object
                ).data,
            },
        )

    # Close the input LAS file
    input_las_file.close()
    rmtree(output_files_base_dir)
    las_file_object.status = las_file_object.Status.CONVERTED
    las_file_object.save()
