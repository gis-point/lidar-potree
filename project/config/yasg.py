from config.openapi import (
    CustomOpenAPISchemaGenerator,
)
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="CryptoDouble",
        default_version="0.0.1",
    ),
    public=True,
    permission_classes=(),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
