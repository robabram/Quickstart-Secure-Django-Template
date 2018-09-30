#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneFormField

from apps.accounts.models import ROLE_CHOICES, PAGE_SIZE_CHOICES, UserProfile


class AccountsUsersListForm (forms.Form):

    error_messages = {
        'invalid_char': _("Search term may only contain the characters A-Z, 0-9 and '-'."),
    }

    search_term = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control has-clear', 'placeholder': 'Search Users'}),
        validators=[
            RegexValidator(r'^[a-zA-Z0-9- ]*$', message=error_messages['invalid_char'], code='invalid_char'),
            MaxLengthValidator(50),
        ],
    )


class SDAuthenticationForm(forms.Form):

    # Override the form user and password objects to work with Bootstrap
    username = forms.CharField(
        label=_('Username'),
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'true'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': 'true'
        })
    )


class UserChangePasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': _("The new passwords do not match."),
    }

    old_password = forms.CharField(
        label=_('Current User Password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control password'}),
    )

    new_password = forms.CharField(
        label=_('New Password'),
        required=True,
        validators=[MinLengthValidator(8), ],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control password'}),
    )

    new_password2 = forms.CharField(
        label=_('Retype New Password'),
        required=True,
        validators=[MinLengthValidator(8), ],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control password'}),
    )

    # def clean_new_password2(self):
    #
    #     new_pwd = self.cleaned_data.get('new_password')
    #     new_pwd2 = self.cleaned_data.get('new_password2')
    #
    #     if new_pwd and new_pwd2 and new_pwd != new_pwd2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #
    #     return new_pwd2


class UserCreateEditForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that user name already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_mismatch': _("The two email fields didn't match."),
        'invalid_current_password': _("Your current password is incorrect."),
        'invalid_char': _("May only contain the characters A-Z, 0-9, '-' and ' '."),
        'invalid_page_size': _("May only contain the characters 0-9"),
        'invalid_offset': _("Invalid UTC offset value"),
    }

    is_active = forms.BooleanField(
        label=_('Active'),
        widget=forms.CheckboxInput(attrs={'class': 'toggle'}),
        help_text=_("User will not be able to login if disabled"),
        required=False
    )

    username = forms.CharField(
        label=_('User Name'),
        required=False,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(150), ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('User name'), 'pattern': '{3,150}', 'required': '1'}),
        help_text=_("Username must be a minimum of 3 characters and a maximum of 150 characters"),
    )

    first_name = forms.CharField(
        label=_('First Name'),
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(30), ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First Name'), 'pattern': '{0,30}'}),
        help_text=_("Maximum 30 characters"),
    )

    last_name = forms.CharField(
        label=_('Last Name'),
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(30), ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name'), 'pattern': '{0,30}'}),
        help_text=_("Maximum 30 characters"),
    )

    email = forms.EmailField(
        label=_('Email Address'),
        required=False,
        error_messages={'required': _('Enter a valid email address.')},
        widget=forms.EmailInput(attrs={'class': 'form-control email', 'placeholder': _('Email address')}),
    )

    password = forms.CharField(
        label=_('Password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'class': 'form-control password', 'placeholder': _('Password'),
                                          'required': '1'}),
    )

    oauth_scope = forms.ChoiceField(
        label=_("Permissions"),
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9- ]*$', message=error_messages['invalid_char'], code='invalid_char'),
            MaxLengthValidator(255),
            MinLengthValidator(4),
        ],
    )

    timezone = TimeZoneFormField(
        label=UserProfile._meta.get_field('timezone').verbose_name,
        help_text=_('Select your preferred timezone or location within the timezone.'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    page_size = forms.ChoiceField(
        label=_("Results Per Page"),
        choices=PAGE_SIZE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        validators=[
            RegexValidator(r'^[0-9]*$', message=error_messages['invalid_page_size'], code='invalid_page_size'),
        ],
    )

    api_access = forms.BooleanField(
        label=_('API Access'),
        widget=forms.CheckboxInput(attrs={'class': 'toggle'}),
        required=False
    )

    api_code = forms.ChoiceField(
        label=_("API Auth Token"),
        choices=ROLE_CHOICES,
        widget=None,
        required=False,
    )

    class Meta:
        model = User
        fields = ('is_active', 'username', 'first_name', 'last_name', 'email', 'password', 'oauth_scope',
                  'page_size', 'api_access', 'api_code', 'timezone')
