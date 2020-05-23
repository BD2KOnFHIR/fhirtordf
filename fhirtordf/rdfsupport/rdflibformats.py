from rdflib import plugin
from rdflib.parser import Parser as rdf_Parser
from rdflib.serializer import Serializer as rdf_Serializer
from typing import List, Union

Parser = rdf_Parser
Serializer = rdf_Serializer

SUFFIX_FORMAT_MAP = {
    'xml': 'rdf',
    'turtle': 'ttl',
    'rdfa': 'html',
    'nquads': 'nq',
    'pretty-xml': 'xml',
    'nt11': 'nt',
    'ntriples': 'nt'
}


def known_formats(use: Union[Serializer, Parser]=Serializer, include_mime_types: bool = False) -> List[str]:
    """ Return a list of available formats in rdflib for the required task
    :param use: task (typically Serializer or Parser)
    :param include_mime_types: whether mime types are included in the return list
    :return: list of formats
    """
    return sorted([name for name, kind in plugin._plugins.keys()
                   if kind == use and (include_mime_types or '/' not in name)])


def suffix_for(fmt: str) -> str:
    return SUFFIX_FORMAT_MAP.get(fmt, fmt)
