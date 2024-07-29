from typing import Union

from las_files.views import (
    LoadLasFile,
    LoadedLasFilesList,
    LasFileDetails
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/load/las/file", LoadLasFile.as_view(), name="load-las-file"),
    path("client/las/file/details/<str:name>", LasFileDetails.as_view(), name="load-las-file"),
    path("client/las/files/list", LoadedLasFilesList.as_view(), name="load-las-file"),
]
