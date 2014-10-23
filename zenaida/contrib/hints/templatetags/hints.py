from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

from zenaida.contrib import hints
from zenaida.contrib.hints.models import Dismissed
from zenaida.contrib.hints.forms import DismissHintForm

register = template.Library()

@register.tag("hint")
def hint(parser, token):
    """
    Usage::

        {% hint user key1 [key2 [...]] [immediate] %}
            <div class="alert alert-info">
                <p>Here's a little hint.</p>
                <form action="{{ hint.dismiss_action }}" method="post">
                    {% csrf_token %}
                    {{ hint.dismiss_form }}
                    <button>Dismiss this hint!</button>
                </form>
            </div>
        {% dismissed %}
            <p>I see you've been here before!</p>
        {% endhint %}

    The hint tag accepts a user object, any number of keys, and an optional
    ``immediate`` keyword. If the ``immediate`` keyword is provided, the hint
    is displayed once, immediately marked for dismissal, and will not be
    displayed again.

    The hint tag also sets some variables in context::

    ========================== =============================================
    Variable                   Description
    ========================== =============================================
    ``hint.dismiss_form``      The form to be used for dismissing the hint.
    ``hint.dismiss_action``    The URL to which the `dismiss_form` should
                               be submitted.
    ``hint.parent_hint``       For nested hints (why are you nesting
                               hints?!), this is the hint above the
                               current one
    ========================== =============================================

    """

    bits = token.split_contents()[1:]

    if bits[-1] == "immediate":
        immediate = True
        bits = bits[:-1]
    else:
        immediate = False

    values = [parser.compile_filter(bit) for bit in bits]

    nodelist = parser.parse(("dismissed", "endhint",))
    token = parser.next_token()
    if token.contents == "dismissed":
        nodelist_dismissed = parser.parse(("endhint",))
        parser.delete_first_token()
    else:
        nodelist_dismissed = None
    return HintNode(values, nodelist, nodelist_dismissed, immediate)


class HintNode(template.Node):
    def __init__(self, variables, nodelist, nodelist_dismissed=None, immediate=False):
        self.nodelist = nodelist
        self.nodelist_dismissed = nodelist_dismissed
        self.immediate = immediate
        self.vars = variables

    def render(self, context):
        if 'hint' in context:
            parent_hint = context['hint']
        else:
            parent_hint = {}

        with context.push():
            user = self.vars[0].resolve(context)
            keys = [unicode(x.resolve(context)) for x in self.vars[1:]]
            keystring = "".join(keys)

            try:
                # Add extra stuff to context:
                context['hint'] = {
                    'dismiss_form': DismissHintForm(initial={'key': keystring}),
                    'dismiss_action': reverse('zenaida.contrib.hints.views.dismiss'),
                    'parent_hint': parent_hint
                }
            except NoReverseMatch as e:
                message = "{}. {}.".format(str(e), "Ensure that url(r'^hints/', include('zenaida.contrib.hints.urls')) is in your urlconf")
                raise NoReverseMatch(message)

            dismissed = Dismissed.objects.filter(key=keystring, user=user).exists()

            if not dismissed:
                output = self.nodelist.render(context)
                # If immediate is set, dismiss the hint
                if self.immediate:
                    hints.dismiss(user, keys)
            elif self.nodelist_dismissed is not None:
                # If there is a dismissed block, render it:
                output = self.nodelist_dismissed.render(context)
            else:
                output = ""

        return output
