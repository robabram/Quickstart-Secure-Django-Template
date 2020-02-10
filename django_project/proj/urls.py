"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from apps.api_example.api_viewsets import *
from proj.settings.base import SWAGGER_DOCS_TITLE

# from proj.api_viewsets import *

admin.autodiscover()
router = routers.DefaultRouter()


schema_view = get_schema_view(
   openapi.Info(
      title=SWAGGER_DOCS_TITLE,
      default_version='v1',
      description="Test description",
      terms_of_service="",
      contact=openapi.Contact(email="contact@example.org"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# API Notes:
#     Non-Django model serializers must have 'base_name' manually set

router.register(r'api_example/temps', TempsViewSet)

urlpatterns = [

    # url(r'^admin/', admin.site.urls),

    # User account management app
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),

    # Dashboard app
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # API urls
    # url(r'^api/docs/', schema_view),  # Note: APIs can be hidden in the docs by editing swagger.py
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^api/', include(router.urls)),

    # Last - Redirect all to settings.LOGIN_REDIRECT_URL
    url(r'^.*$', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL, permanent=False))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



