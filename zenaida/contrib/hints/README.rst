.. highlight:: python

Zenaida Contrib Hints
========================

Zenaida contrib hints is a pluggable Django app which allows you to integrate
user-dismissable messages into your templates.

Installation
------------

You can install the latest version of Zenaida using ``pip``:

.. code-block:: bash

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

Within the :ttag:`{% hint %}` tag, some context variables are available:

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

Ajax Submission
---------------

To avoid a reload and make your pages feel snappy, use the bundled javascript
to submit alert dismissals asynchronously. Include it on your page with your
javascripts:

.. code-block:: html+django

    {% load staticfiles %}
    <script type="text/javascript" src="{% static "hints/hints.js" %}"></script>

And then enable it on your hint form using the ``data-dismiss-hint`` attribute:

.. code-block:: html+django

    {% hint user key1 key2 %}
        <div class="alert alert-info" id="myHint">
            <p>Here's a little hint.</p>
            <form action="{{ hint.dismiss_action }}" method="post" data-dismiss-hint="#myHint">
                {% csrf_token %}
                {{ hint.dismiss_form }}
                <button>Dismiss this hint!</button>
            </form>
        </div>
    {% endhint %}

There are also a few additional data attributes available:

====================== ========= ===============================================
Name                   Default   Description
====================== ========= ===============================================
data-dismiss-hint      none      CSS selector that identifies the element to be
                                 hidden when the form is submitted.
data-transition        "fadeOut" The transition to use for hiding the
                                 hint. Can be ``fadeOut``, ``slideUp``,
                                 or ``none``.
data-transition-speed  200       How quickly to execute the transition in
                                 milleseconds.
====================== ========= ===============================================

The javascript relies on jQuery, so be sure to include that on the page
with your hints.

If for any reason the included javascript does not work with your templates, you
can write your own javascript that submits the form data to
``{{ hint.dismiss_action }}``. As long as the ajax request includes the
``X-Requested-With: XMLHttpRequest`` header, the view will return a JSON success
message or an error.
