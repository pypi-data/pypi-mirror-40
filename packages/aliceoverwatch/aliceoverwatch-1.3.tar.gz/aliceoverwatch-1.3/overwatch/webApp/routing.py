#!/usr/bin/env python

""" Contains routing functions.

Contains functions to ensure safe routing and redirection of the next URL. These functions are from
http://flask.pocoo.org/snippets/62/, and were written by the author of Flask.

Slight modifications were made to :func:`redirectBack` to ensure that a login-logout loop was avoided
under particular circumstances.

.. codeauthor:: Raymond Ehlers <raymond.ehlers@cern.ch>, Yale University
"""

from flask import request, url_for, redirect

# Handle python 2/3
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin

# Logging
import logging
logger = logging.getLogger(__name__)

def isSafeUrl(target):
    """ Checks URL for safety to ensure that it does not redirect unexpectedly.

    Note:
        Relies on the flask.request object.

    Args:
        target (str): URL for the target to test.
    Returns:
        bool: True if the URL is safe.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def getRedirectTarget():
    """ Extracts the Next target and checks its safety.

    Note:
        Relies on the flask.request object.

    Args:
        None
    Returns:
        str: URL if the target is safe.
    """
    for target in [request.values.get('next'), request.referrer]:
        if not target:
            continue
        if isSafeUrl(target):
            return target

def redirectBack(endpoint, **values):
    """ Handles safe redirection.

    It extracts the value of Next from flask.request. If the target is not safe, then redirect back
    to ``endpoint`` instead.

    Note:
        Relies on the request.form dict.

    Args:
        endpoint (str): Where to redirect in case the Next url is not safe
        **values (dict): Arguments to pass to url_for() in case of needing to redirect to
            endpoint instead.
    Returns:
        redirect to NextUrl: Redirect is called on the next URL if it is safe. Redirects to the
            given endpoint if the URL is not safe.
    """
    target = request.form['next']
    # If an unauthenticated user attempted to access /logout, then after logging in, it would redirect
    # them to logout, causing a loop. So instead we just redirect to the default location in such a case.
    # Also prevent downloading test data since it would lead to a confusing situation where the user stays
    # on the login page after logging in.
    # This logout and test data specific change is the only one made in these functions
    if not target or not isSafeUrl(target) or "logout" in target or "testingDataArchive" in target:
        target = url_for(endpoint, **values)
    #logger.debug("target for redirectBack: {target}".format(target = target))
    return redirect(target)

