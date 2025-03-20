from urllib.parse import urlparse

import validators


def normalize_url(url: str) -> str:
    '''
    Return a normalized URL, preserving only the scheme and host.
    Example:
        normalize_ulr("https://www.example.com/some/path?query=param#fragment")
          will return "https://www.example.com".
    '''
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.hostname


def validate_url(url: str) -> list:
    errors = ''
    if not validators.url(url) or len(url) > 255:
        errors = 'Некорректный URL'
    return errors