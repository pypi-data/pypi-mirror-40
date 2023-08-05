"""
Module containing APICallError class
"""

import os
from pyowm.exceptions import OWMError


class APICallError(OWMError):
    """
    Error class that represents network/infrastructural failures when invoking OWM Weather API, in
    example due to network errors.

    :param message: the message of the error
    :type message: str
    :param triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)
    :type triggering_error: an *Exception* subtype
    """
    def __init__(self, message, triggering_error=None):
        self._message = message
        self._triggering_error = triggering_error

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in calling OWM Weather API.', os.linesep,
                       'Reason: ', self._message, os.linesep,
                       'Caused by: ', str(self._triggering_error)])


class BadGatewayError(APICallError):
    """
    Error class that represents 502 errors - i.e when upstream backend
    cannot communicate with API gateways.

    :param message: the message of the error
    :type message: str
    :param triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)
    :type triggering_error: an *Exception* subtype
    """
    pass


class APICallTimeoutError(APICallError):
    """
    Error class that represents response timeout conditions

    :param message: the message of the error
    :type message: str
    :param triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)
    :type triggering_error: an *Exception* subtype
    """
    pass


class APIInvalidSSLCertificateError(APICallError):
    """
    Error class that represents failure in verifying the SSL certificate provided
    by the OWM API

    :param message: the message of the error
    :type message: str
    :param triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)
    :type triggering_error: an *Exception* subtype
    """
    pass
