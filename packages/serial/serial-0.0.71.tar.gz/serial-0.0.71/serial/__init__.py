"""
`serial` is an object serialization/deserialization library intended to facilitate authoring of API models which are
readable and introspective, and to expedite code and data validation and testing. `serial` supports JSON, YAML, and
XML.
"""

# Tell the linters what's up:
# pylint:disable=wrong-import-position

# region Backwards Compatibility

# These compatibility issues are addressed here (as well as elsewhere in this module) in order to ensure this is done if this module is imported at the 
# top-level, with `import serial` rather than `from...`

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, \
    with_statement

from future import standard_library

standard_library.install_aliases()

from builtins import *  # noqa
from future.utils import native_str # noqa

# endregion

from serial import errors, utilities, properties, meta, hooks, test, model, request # noqa
