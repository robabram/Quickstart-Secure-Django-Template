#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django import template
from django.template.defaulttags import URLNode, url
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.tag
def smarturl(parser, token):
    validator = url(parser, token)
    return SmartURLNode(validator.view_name, validator.args, validator.kwargs, validator.asvar)


class SmartURL(str):
    """
    This is a wrapper class that allows us to attach attributes to regular
    unicode strings.
    """
    pass


class SmartURLNode(URLNode):

    # def __init__(self, view_name, args, kwargs, asvar):
    #     super(SmartURLNode, self).__init__(view_name, args, kwargs, asvar)
    #     self.crap = 'test'

    def render(self, context):

        # Loosely based off of https://www.silviogutierrez.com/blog/smarter-django-url-tag/ and
        # http://www.turnkeylinux.org/blog/django-navbar

        # Get the view name and the current url from the request object
        resolved_view_name = self.view_name.resolve(context)
        request_url = context.get('request', None).path

        # Resolve the
        try:
            resolved_url = reverse(resolved_view_name)
        except NoReverseMatch:
            return ''

        # Save the resolved url string into the SmartURL object
        rendered = SmartURL(resolved_url)

        # Add active and active_root properties
        if resolved_url == request_url:
            rendered.active = ' selected'
        else:
            rendered.active = ''

        parent_url = '/'.join(resolved_url.split('/')[:-1])

        if request_url.startswith(parent_url):
            rendered.active_root = ' button-selected'
        else:
            rendered.active_root = ''

        # Assign the SmartURL instance back into the context and we're done.
        # As this is an assignment use, return an empty string.
        context[self.asvar] = rendered

        return ''


