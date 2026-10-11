import socket
import httplib2
import httpx
from google.auth.exceptions import TransportError, RefreshError
from googleapiclient.errors import HttpError

NO_INTERNET_MESSAGE = "I can't reach the internet right now. Please check your connection."
AUTH_EXPIRED_MESSAGE = "I've lost access to Gmail. Please reconnect your account."
GMAIL_ERROR_MESSAGE = "Something went wrong on Gmail's end. Please try again in a moment."
GENERIC_ERROR_MESSAGE = "Something went wrong. Please try again."

NETWORK_ERRORS = (
    socket.gaierror,
    ConnectionError,
    TimeoutError,
    httplib2.ServerNotFoundError,
    httpx.ConnectError,
    httpx.TimeoutException,
    TransportError,
)


def chain_matches(error, check):
    seen = set()
    current = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if check(current):
            return True
        current = current.__cause__ or current.__context__
    return False


def is_network_error(error):
    return chain_matches(error, lambda e: isinstance(e, NETWORK_ERRORS))


def is_auth_error(error):
    def check(e):
        if isinstance(e, RefreshError):
            return True
        return isinstance(e, HttpError) and e.resp.status == 401
    return chain_matches(error, check)


def is_gmail_service_error(error):
    def check(e):
        return isinstance(e, HttpError) and (e.resp.status == 429 or e.resp.status >= 500)
    return chain_matches(error, check)


def get_error_message(error):
    if is_network_error(error):
        return NO_INTERNET_MESSAGE
    if is_auth_error(error):
        return AUTH_EXPIRED_MESSAGE
    if is_gmail_service_error(error):
        return GMAIL_ERROR_MESSAGE
    return GENERIC_ERROR_MESSAGE