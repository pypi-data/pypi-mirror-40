"""
Helpers
=======

Utility functions which are used in other modules.
"""
import base64
import hashlib


def generate_signature(app_id, secret_key, content):
    """ Create a signature for an Akulaku api request

    :param `str` app_id: A unique app ID given by Akulaku
    :param `str` secret_key: A unique secret key given by Akulaku
    :param `str` content: The stringified content of the request.
    :returns: A string that can be used in an AkuLaku request body
    :rtype: str
    """
    content = f'{app_id}{secret_key}{content}'
    has_sha512 = hashlib.sha512(content.encode()).digest()
    encoded = base64.b64encode(has_sha512)

    encoded_string = encoded.decode('utf-8')
    return encoded_string.replace("+", "-").replace("/", "_").replace("=", "")
