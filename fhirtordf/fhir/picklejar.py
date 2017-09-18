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
import os
import pickle
import uuid
from typing import Tuple, Optional, Dict


class _PickleJarFactory:
    _instance = None
    _cache_directory = os.path.abspath(os.path.join(os.path.expanduser('~'), ".cache"))

    def clear(self):
        if self._instance:
            self._instance.clear()
        self._instance = None

    @property
    def picklejar(self) -> "_PickleJar":
        if not self._instance:
            self._instance = _PickleJar(self)
        return self._instance

    @property
    def cache_directory(self) -> str:
        return self._cache_directory

    @cache_directory.setter
    def cache_directory(self, path: str) -> None:
        self._cache_directory = path
        self._instance = None

    @property
    def cache_directory_index(self) -> str:
        return os.path.join(self._cache_directory, 'index') if self._cache_directory is not None else None

picklejarfactory = _PickleJarFactory()


class _PickleJar:

    class CacheEntry:
        def __init__(self, sig: Tuple, loc: str):
            """
            An entry in a cache
            :param sig: Unique signature for the entry
            :param loc: Location of the file containing the pickled image of the entry
            """
            self.sig = sig
            self.loc = loc

    def __init__(self, factory: type(_PickleJarFactory)):
        """
        Create a new image cache
        """
        self._cache_directory = factory.cache_directory
        self._cache_directory_index = factory.cache_directory_index
        if self._cache_directory is not None:
            os.makedirs(self._cache_directory, exist_ok=True)
        if self._cache_directory is not None and os.path.exists(self._cache_directory_index):
            self._load()
        else:
            self._cache = {}            # type: Dict[str, _PickleJar.CacheEntry]
            self._update()

    def add(self, name: str, sig: Tuple, obj: object) -> None:
        """
        Add a file to the cache
        :param name: name of the object to be pickled
        :param sig: signature for object
        :param obj: object to pickle
        """
        if self._cache_directory is not None:
            if name in self._cache:
                os.remove(os.path.join(self._cache_directory, self._cache[name].loc))
            fname = os.path.join(self._cache_directory, str(uuid.uuid4()))
            with open(fname, 'wb') as f:
                pickle.dump(obj, f)
            self._cache[name] = _PickleJar.CacheEntry(sig, fname)
            self._update()

    def get(self, name: str, sig: Tuple) -> Optional[object]:
        """
        Return the object representing name if it is cached
        :param name: name of object
        :param sig: unique signature of object
        :return: object if exists and signature matches
        """
        if name not in self._cache:
            return None
        if self._cache[name].sig != sig:
            del self._cache[name]
            self._update()
            return None
        with open(self._cache[name].loc, 'rb') as f:
            return pickle.load(f)

    def _update(self) -> None:
        if self._cache_directory is not None:
            with open(self._cache_directory_index, 'wb') as f:
                pickle.dump(self._cache, f)

    def _load(self) -> None:
        if self._cache_directory is not None:
            with open(self._cache_directory_index, 'rb') as f:
                self._cache = pickle.load(f)
        else:
            self._cache = {}

    def clear(self) -> None:
        """
        Clear all cache entries for directory and, if it is a 'pure' directory, remove the directory itself
        """
        if self._cache_directory is not None:
            # Safety - if there isn't a cache directory file, this probably isn't a valid cache
            assert os.path.exists(self._cache_directory_index), "Attempt to clear a non-existent cache"
            self._load()            # Shouldn't have any impact but...
            for e in self._cache.values():
                if os.path.exists(e.loc):
                    os.remove(e.loc)
            self._cache.clear()
            self._update()
        self._cache = {}


def picklejar():
    return picklejarfactory.picklejar
