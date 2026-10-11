import httplib2
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from brain.error_handler import get_error_message


def make_http_error(status):
    resp = httplib2.Response({"status": status})
    return HttpError(resp, b"test error")


cases = [
    ("Gmail rate limit (429)", make_http_error(429)),
    ("Gmail server error (503)", make_http_error(503)),
    ("Gmail unauthorized (401)", make_http_error(401)),
    ("Expired token", RefreshError("invalid_grant")),
    ("Network failure", ConnectionError("no route")),
    ("Unknown error", ValueError("something unexpected")),
]

for label, error in cases:
    print(label, "->", get_error_message(error))