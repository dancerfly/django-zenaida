from zenaida.contrib.hints.models import Dismissed
from zenaida.contrib.hints.forms import DismissHintForm

from django.http import (HttpResponse, HttpResponseNotAllowed,
                        HttpResponseBadRequest, HttpResponseRedirect)

def dismiss(request):
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])
    else:
        form = DismissHintForm(request.POST)
        dismissed = form.save(commit=False)
        dismissed.user = request.user
        dismissed.save()
        if 'next' in request.GET:
            next_url = request.GET['next']
        else:
            next_url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(next_url)
