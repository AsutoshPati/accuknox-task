from django.contrib.auth.hashers import MD5PasswordHasher
from rest_framework.views import exception_handler

from accuknox.settings import SALT


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # errors = dict()
    # for err, msg in exc.detail.items():
    #     errors.update({err: str(msg[0])})
    if 'errors' in exc.detail:
        exc.detail = exc.detail['errors']
    response.data = {"errors": exc.detail}
    return response


def make_password(password: str):
    """
    Generate encrypted password from password string

    :param password: Raw string password
    :return: encoded password string
    """
    _, _, md5_hash = MD5PasswordHasher().encode(password, salt=SALT).split("$", 2)
    return md5_hash
