def dismiss(user, keys):
    """
    Dismiss a hint. Expects parameters ``user`` as a user object
    and ``keys`` as an iterable.

    """

    from zenaida.contrib.hints.models import Dismissed

    keystring = "".join(keys)
    return Dismissed.objects.create(user=user, key=keystring)
