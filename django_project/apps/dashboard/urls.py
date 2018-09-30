#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django.conf.urls import url
from apps.dashboard import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.overview, name='overview'),
    # url(r'^update/status/', views.ajax_get_update_status, name='ajax_get_update_status'),
]

