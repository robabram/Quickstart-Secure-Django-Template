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

from rest_framework import routers
from proj.swagger import get_swagger_view
from proj.settings.base import SWAGGER_DOCS_TITLE

from proj.api_viewsets import *
from apps.api_example.api_viewsets import *

admin.autodiscover()
router = routers.DefaultRouter()
schema_view = get_swagger_view(title=SWAGGER_DOCS_TITLE)

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
    url(r'^api/docs/', schema_view),  # Note: APIs can be hidden in the docs by editing swagger.py
    url(r'^api/', include(router.urls)),

    # Last - Redirect all to settings.LOGIN_REDIRECT_URL
    url(r'^.*$', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL, permanent=False))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



