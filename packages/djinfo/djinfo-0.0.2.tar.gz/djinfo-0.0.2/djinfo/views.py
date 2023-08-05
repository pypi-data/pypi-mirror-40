# -*- coding: utf-8 -*-
"""
djinfo generic views
"""

from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest

from djinfo.utils import get_context
from djinfo.decorators import superuser_required


@superuser_required
@require_http_methods(['GET'])
def djinfo(request):  # noqa pylint: disable=inconsistent-return-statements
    """ djinfo process ajax view """
    ctx = get_context()
    if request.is_ajax():
        return HttpResponseBadRequest()
    elif request.GET.get('json'):
        return JsonResponse(ctx)
    return render(request, 'djinfo/index.html', ctx)
