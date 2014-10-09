from zenaida.contrib.hints.models import Dismissed
from zenaida.contrib.hints.forms import DismissHintForm

from django.core.exceptions import SuspiciousOperation
from django.http import (HttpResponse, HttpResponseNotAllowed,
                        HttpResponseBadRequest, HttpResponseRedirect)
from django.utils.http import is_safe_url


def dismiss(request):
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])
    else:
        form = DismissHintForm(request.POST, user=request.user)
        dismissed = form.save()
        if 'next' in request.GET:
            next_url = request.GET['next']
        else:
            next_url = request.META['HTTP_REFERER']

        if not is_safe_url(next_url, host=request.get_host()):
            raise SuspiciousOperation("Url {} is not safe to redirect to.".format(next_url))

        return HttpResponseRedirect(next_url)
