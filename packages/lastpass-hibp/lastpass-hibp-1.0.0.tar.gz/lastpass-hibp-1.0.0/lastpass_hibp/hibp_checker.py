import hashlib
import requests


def check_password(password):
    if isinstance(password, str):
        password = password.encode()

    h = hashlib.sha1(password).hexdigest().upper()
    prefix, suffix = h[:5], h[5:]
    response = requests.get(
        'https://api.pwnedpasswords.com/range/{}'.format(prefix)
    )
    response = response.content.decode()
    hashes = [x.split(':')[0].strip()
              for x in response.split("\r\n")]
    return suffix in hashes

