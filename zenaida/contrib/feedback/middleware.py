import re

from django.conf import settings
from django.utils.encoding import force_text


_HTML_TYPES = ('text/html', 'application/xhtml+xml')


class FeedbackMiddleware(object):
    """
    Middleware to attach the feedback form to all HTML responses.

    """

    def process_response(self, request, response):
        import logging

        logging.warning(
            "Zenaida Feedback is deprecated and the form no longer renders."
            "Please switch to django-talkback.",)

        return response
