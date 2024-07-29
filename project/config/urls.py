from config.yasg import urlpatterns as doc_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("api/v1/las_files/", include("las_files.urls"), name="las_files"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += doc_urls
