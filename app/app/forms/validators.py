"""Common form validators for beardo dashboard
"""
# marty mcfly imports
from __future__ import absolute_import

# stdlib import
import base64
import struct

# third-party imports
from wtforms import ValidationError


def validate_ssh_key(form, field):
    """Ensure the passed in SSH key *looks* valid.
    """
    try:
        type, key_string, comment = field.data.split()
    except ValueError:
        raise ValidationError('Not a valid SSH key: requires 3 parts (type, key string and email/comment)')

    data = base64.decodestring(key_string)
    int_len = 4
    str_len = struct.unpack('>I', data[:int_len])[0]  # this should return 7
    if not data[int_len:int_len+str_len] == type:
        raise ValidationError('Not a valid SSH key')
