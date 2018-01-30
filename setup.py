from distutils.core import setup

import sys

from fhirtordf import __version__

requires = ['python_dateutil', 'rdflib>=4.2.2', 'jsonasobj>=1.1.1', 'dirlistproc>=1.4.5', 'rdflib-jsonld',
            'isodate']
if sys.version_info < (3, 5):
    requires.append('typing')

setup(
    name='fhirtordf',
    version=__version__,
    packages=['tests', 'scripts', 'fhirtordf', 'fhirtordf.fhir', 'fhirtordf.loaders', 'fhirtordf.rdfsupport'],
    url='https://github.com/BD2KOnFHIR/fhirtordf',
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig.harold@mayo.edu',
    description='FHIR JSON to RDF Conversion Tool',
    long_description='Convert JSON representatin of FHIR resources into RDF',
    install_requires=requires,
    scripts=['scripts/fhirtordf'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
        'Programming Language :: Python :: 3'
    ]
)
