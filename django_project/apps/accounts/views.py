#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import logging
import copy

from django import forms
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import Error
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps import FormatModalDialogErrors
from apps.accounts import forms
from apps.accounts.models import generate_api_code
from proj.context_processors import user_can_edit
from proj.common.oauth_helper import create_access_token, encrypt_access_token
from proj.common.url_helper import build_url
from proj.common.error_msg_helper import bootstrap_alert_message

logger = logging.getLogger(__name__)


@csrf_exempt
def login_view(request, *args, **kwargs):

    # TODO: Support the "next" parameter in the template javascript redirect code.

    # This POST method is called by javascript and expects some JSON in return.
    # The goal here is to authenticate the user with oauth and then encrypt the
    # oauth information.  The encrypted information will be stored in a browser cookie,
    # to be later decrypted in the middleware level to set the "Authorization" header.
    if request.method == 'POST':

        if 'username' not in request.POST or 'password' not in request.POST:
            raise ValueError

        # Manually do django authentication.
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)

        if user is not None and user.is_active:

            # Log our user in to django
            login(request, user)

            # Create and encrypt the access token based on this user
            enc = encrypt_access_token(create_access_token(user, user.profile.oauth_scope))

            # Setup login redirect
            if 'next' in request.GET:
                redirect = request.GET['next']
            else:
                redirect = settings.LOGIN_REDIRECT_URL

            # Format our response
            response = JsonResponse(dict([('status', 'OK'), ('next', redirect)]))

            # TODO: find out why this delays forever when celery service is not running
            # user_security_event.delay(username, 'login')

            # Set the encrypted token in the response.
            response.set_cookie('token', enc.decode('UTF-8'))
            response.set_cookie('fade-page-in', 1)

        else:
            # Send our error message
            response = JsonResponse(dict([('status', 'ERROR')]))
            # user_security_event.delay(username, 'login', success=False)

        return response

    else:

        form = forms.LoginForm()
        context = {
            'form': form,
            'next': request.GET['next'] if 'next' in request.GET else None,
        }

    return render(request, 'accounts/login.html', context)


@login_required
@require_http_methods(["POST", "GET"])
def accounts_list_users(request):

    page_size = request.user.profile.page_size
    search_term = ''

    if request.method == "POST":
        page = 1
        form = forms.AccountsUsersListForm(request.POST)

    else:
        form = forms.AccountsUsersListForm(request.GET, initial={'search_term': search_term})
        page = request.GET.get('page')

    if form.is_valid():
        search_term = form.cleaned_data.get('search_term')

    if not search_term:
        user_results = User.objects.all().order_by('username')
    else:
        user_results = User.objects.filter(
            Q(username__icontains=search_term) |
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(email__icontains=search_term)).order_by('username')

    # set up paginator values
    paginator = Paginator(user_results, page_size)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'all_users': users,
        'page_range': range(1, paginator.num_pages + 1),
        'show_pager': user_results.count() > paginator.per_page,
        'add_form': forms.UserCreateEditForm(),
    }

    return render(request, 'accounts/users_list.html', context)


@login_required
@require_http_methods(["POST"])
def ajax_accounts_create_user(request):
    """
    Ajax request sent from bundle_list view. Creates new bundle record from post data.
    """
    can_edit = user_can_edit(request)
    if not can_edit:
        return JsonResponse(
            dict([('status', 'ERROR'), ('message', bootstrap_alert_message(_('Insufficient rights'), 'danger'))]))

    form = forms.UserCreateEditForm(request.POST)

    if form.is_valid():

        user = form.save(commit=False)
        user.is_active = True
        user.set_password(user.password)
        user.save()

        # Update user profile record information
        profile = User.objects.get(pk=user.id).profile
        profile.oauth_scope = form.cleaned_data.get('oauth_scope')
        profile.save()

        return JsonResponse(
            dict([
                ('status', 'OK'),
                ('location', reverse('accounts:user_read_update',
                                      kwargs={'user_id': user.id, 'mode': 'edit'}))
            ])
        )
    else:

        return JsonResponse(
            dict([
                ('status', 'ERROR'),
                ('message', FormatModalDialogErrors(form))
            ])
        )


@login_required
@require_http_methods(["POST", "GET"])
def user_read_update(request, user_id, mode):

    messages = []
    tab = 'user'  # Must be the exact name suffix of a "nav-section-xxxxxx" class name.

    try:
        user = User.objects.get(pk=user_id)
        profile = User.objects.get(pk=user.id).profile
        save_pwd = user.password

    except ObjectDoesNotExist:
        return redirect('/accounts/')

    if request.method == "POST" and user_can_edit(request):

        form = forms.UserCreateEditForm(request.POST, instance=user)

        if form.is_valid():
            try:

                user = form.save(commit=False)

                # Ensure the primary user record is enabled
                if int(user_id) == 1:
                    user.is_active = 1

                user.password = save_pwd  # Restore the correct password
                user.save()

                # Update user profile record information

                profile.page_size = form.cleaned_data.get('page_size')
                profile.timezone = form.cleaned_data.get('timezone')

                if int(user_id) > 1:
                    profile.oauth_scope = form.cleaned_data.get('oauth_scope')
                    profile.api_access = form.cleaned_data.get('api_access')

                    if profile.api_access is True:
                        if not profile.api_code:
                            profile.api_code = generate_api_code()
                    else:
                        profile.api_code = None

                profile.save()

                # TODO: make api_code a read-only text input with a copy to clipboard button. https://clipboardjs.com/

                # api_code always needs to be added to the form data
                data = copy.deepcopy(form.data)
                data['api_code'] = profile.api_code
                form.data = data

            except Error as e:
                messages = ['error|{0}'.format(_('An unexpected error occurred while trying to save, please try again ({0})'.format(e)))]
        else:
            messages = ['error|{0}'.format(_('There are values that need to be corrected before saving.'))]
    else:
        form = forms.UserCreateEditForm(instance=user, initial={
                    'oauth_scope': profile.oauth_scope,
                    'timezone': profile.timezone,
                    'page_size': profile.page_size,
                    'api_access': profile.api_access,
                    'api_code': profile.api_code, })

    context = {
        'form': form,
        'messages': messages,
        'user_id': user_id,
        'active_tab': tab,
        'pwd_form': forms.UserChangePasswordForm(),
    }

    return render(request, 'accounts/users_edit.html', context)


@login_required
@require_http_methods(["GET"])
def accounts_delete_user(request, user_id):
    """
    Delete user 
    """
    can_edit = user_can_edit(request)

    if not user_id or user_id == 1:
        return redirect("/")

    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return redirect("/")

    # Only delete if there are zero rules associated with this user
    if can_edit and user:
        user.delete()

    kwargs = {}

    if 'search_term' in request.GET and request.GET['search_term'] != 'None':
        kwargs['search_term'] = request.GET['search_term']

    if 'page' in request.GET:
        kwargs['page'] = request.GET['page']

    return redirect(build_url('accounts:accounts_list_users', get=kwargs))


@login_required
@require_http_methods(["POST"])
def ajax_accounts_change_password(request, user_id):
    """
    Ajax request sent from bundle_list view. Creates new bundle record from post data.
    """
    can_edit = user_can_edit(request)
    if not can_edit:
        return JsonResponse(
            dict([('status', 'ERROR'), ('message', bootstrap_alert_message(_('Insufficient rights'), 'danger'))]))

    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            dict([('status', 'ERROR'),
                  ('message', bootstrap_alert_message(_('Invalid user'), 'danger'))]))

    form = forms.UserChangePasswordForm(request.POST)

    if form.is_valid():

        current_password = form.cleaned_data['old_password']

        if not request.user.check_password(current_password):
            return JsonResponse(
                dict([('status', 'ERROR'),
                      ('message', bootstrap_alert_message(_('Invalid current user password'), 'danger'))]))

        password = form.cleaned_data['new_password']
        password2 = form.cleaned_data['new_password2']

        if password and password2:

            if password != password2:
                return JsonResponse(
                    dict([('status', 'ERROR'),
                          ('message', bootstrap_alert_message(_('New passwords do not match'), 'danger'))]))

            user.set_password(password)
            user.save()

            return JsonResponse(
                dict([
                    ('status', 'OK'),
                    ('message', bootstrap_alert_message(_('User password has been changed.'), 'success'))
                ])
            )

    return JsonResponse(
        dict([
            ('status', 'ERROR'),
            ('message', FormatModalDialogErrors(form))
        ])
    )