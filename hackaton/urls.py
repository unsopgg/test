from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(

        title = "Authentication API",
        default_version = 'v1',
        description = 'SomeDescription'
    ),
    public=True
)

urlpatterns = [
    path("swagger/", schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('account/', include('application.account.urls')),
    path('comment/', include('application.comment.urls')),
    path('post/', include('application.posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
