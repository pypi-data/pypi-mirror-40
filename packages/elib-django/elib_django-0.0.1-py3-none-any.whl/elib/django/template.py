#
# copyright (c) 2019 east301
#
# This software is released under the Apache License, Version 2.0.
# https://opensource.org/licenses/Apache-2.0
#

from django.conf import settings


def django_settings(request):
    return {
        'django_settings': settings
    }
