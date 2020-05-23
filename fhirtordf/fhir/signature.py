import urllib.request
import urllib.error
from typing import Optional, Tuple
import os
import stat


def is_url(name: str) -> bool:
    """
    Return true if name represents a URL
    :param name:
    :return:
    """
    return '://' in name


def is_file(name: str) -> bool:
    """
    Return true if the name doesn't represent a URL
    :param name:
    :return:
    """
    return name and not is_url(name)


def file_signature(file_name: str) -> Optional[Tuple]:
    """
    Return an identity signature for file name
    :param file_name: name of file
    :return: mode, size, last modified time if file exists, otherwise none
    """
    try:
        st = os.stat(file_name)
    except FileNotFoundError:
        return None
    return stat.S_IFMT(st.st_mode), st.st_size, st.st_mtime


def url_signature(url: str) -> Optional[Tuple]:
    """
    Return an identify signature for url
    :param url: item to get signature for
    :return: tuple containing last modified, length and, if present, etag
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    response = None
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        return None
    return response.info()['Last-Modified'], response.info()['Content-Length'], response.info().get('ETag')


def signature(name: str) -> Optional[Tuple]:
    """
    Return the file or URL signature for name
    :param name:
    :return:
    """
    return url_signature(name) if is_url(name) else file_signature(name) if is_file(name) else None
