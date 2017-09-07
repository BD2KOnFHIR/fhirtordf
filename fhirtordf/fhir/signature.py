# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
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
