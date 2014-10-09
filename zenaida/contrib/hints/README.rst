Zenaida Contrib Hints
========================

Zenaida contrib hints is a pluggable Django app which allows you to integrate
user-dismissable messages into your templates.

Installation
------------

You can install the latest version of Zenaida using ``pip``::

    $ pip install https://github.com/littleweaver/django-zenaida/tarball/master

You can clone the repository yourself at https://github.com/littleweaver/django-zenaida.

.. highlight:: python

Setup
-----

Ensure that ``'zenaida.contrib.hints'`` is in your project's ``INSTALLED_APPS``::

INSTALLED_APPS = (
    'zenaida.contrib.hints',
    ...
)

Add the following or similar anywhere in your URLconf::

urlpatterns = patterns('',
    url(r'^hints/', include('zenaida.contrib.hints.urls')),
    ...
)

Usage
-----

Include a hint on a template page like so:

.. code-block:: html+django

    {% hint user key1 key2 %}
        <div class="alert alert-info">
            <p>Here's a little hint.</p>
            <form action="{{ hint.dismiss_action }}?next=/next_url/" method="post">
                {% csrf_token %}
                {{ hint.dismiss_form }}
                <button>Dismiss this hint!</button>
            </form>
        </div>
    {% dismissed %}
        <p>I see you've been here before!</p>
    {% endhint %}

You may include as many keys as you like (noting that there is a string limit
on keys of 255 characters) and must include one user. The
:ttag:`{% dismissed %}` section is optional for rendering different HTML if the
user has already dismissed this hint.

Within the :ttag:`{% hint %}` tag, some context variables are available::

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

You may add a querystring to the dismiss action to specify where the user should
be directed to after dismissing the hint. If no ``next_url`` is specified, it
will redirect back to the referring page.
