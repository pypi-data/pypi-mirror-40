from __future__ import absolute_import, print_function, unicode_literals

import sys

from .tokenex import TokenExRequest, TokenExResponse, TokenExException

SUPPORTED_VERSIONS = [(2, 7), (3, 4), (3, 5), (3, 6), (3, 7)]

python_major_version = sys.version_info[0]
python_minor_version = sys.version_info[1]

if (python_major_version, python_minor_version) not in SUPPORTED_VERSIONS:  # pragma: no cover
    formatted_supported_versions = ['{}.{}'.format(mav, miv) for mav, miv in SUPPORTED_VERSIONS]
    err_msg = 'This version of Python ({}.{}) is not supported!\n'.format(python_major_version, python_minor_version) +\
              'The following versions of Python are supported: {}'.format(formatted_supported_versions)
    raise RuntimeError(err_msg)
