import datetime
import os
from typing import Any

from decouple import Csv, config
from django.conf import settings

INSTALLED_APPS: list[str] = [
    # default django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Other libs app:
    "corsheaders",
    "drf_standardized_errors",
    "rest_framework_swagger",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "channels",
    "las_files.apps.LasFilesConfig",
    "django_minio_backend.apps.DjangoMinioBackendConfig",
]

MIDDLEWARE: list[str] = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS: list[str] = [
    "authentication.services.auth_service.CaseInsensitiveEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]


AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(settings._BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

SWAGGER_SETTINGS: dict[str, Any] = {
    "SHOW_REQUEST_HEADERS": True,
    "HIDE_HOSTNAME": True,
    "SECURITY_DEFINITIONS": {
        "User": {"type": "apiKey", "name": "Authorization", "in": "Header"},
    },
    "USE_SESSION_AUTH": config("USE_SESSION_AUTH", cast=bool),
    "JSON_EDITOR": config("JSON_EDITOR", cast=bool),
    "SUPPORTED_SUBMIT_METHODS": (
        "get",
        "post",
        "put",
        "delete",
        "patch",
    ),
}


REST_FRAMEWORK: dict[str, Any] = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("config.renderers.CustomRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "config.pagination.CustomPagination",
}

SIMPLE_JWT: dict[str, Any] = {
    "AUTH_HEADER_TYPES": (config("AUTH_HEADER_TYPES", cast=str)),
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME", cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(
        days=config("REFRESH_TOKEN_LIFETIME", cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

CORS_ALLOWED_ORIGINS = config(
    "ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")]
)
CORS_ALLOW_METHODS: list[str] = config(
    "CORS_ALLOW_METHODS", cast=lambda v: [s.strip() for s in v.split(",")]
)
CORS_ALLOW_HEADERS: list[str] = config(
    "CORS_ALLOW_HEADERS", cast=lambda v: [s.strip() for s in v.split(",")]
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
