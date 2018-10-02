#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from apps.accounts import views
from django.conf.urls import url
from django.contrib.auth.views import logout_then_login

# Replacement oauth enabled views
from apps.accounts.views import login_view
from apps.accounts.forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.accounts_list_users, name='accounts_list_users'),
    url(r'^create/$', views.ajax_accounts_create_user, name='ajax_accounts_create_user'),
    url(r'^(?P<user_id>[0-9]+)/delete/$', views.accounts_delete_user, name='accounts_delete_user'),
    url(r'^(?P<user_id>[0-9]+)/(?P<mode>(view|edit))/', views.user_read_update, name='user_read_update'),
    url(r'^(?P<user_id>[0-9]+)/changepwd/$', views.ajax_accounts_change_password, name='ajax_accounts_change_password'),

    # override django built-ins
    url(r'^login/', login_view,
        {'template_name': 'accounts/login.html', 'authentication_form': LoginForm,
         'redirect_field_name': 'next'}, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),

]

