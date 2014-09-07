"""Form definitions for beardo, allow easy validation of input
"""
# future imports
from __future__ import absolute_import

# third-party imports
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators

# local imports
from .validators import validate_ssh_key


class SSHKeyForm(Form):

    title = StringField(validators=[validators.DataRequired()])
    ssh_key = TextAreaField('SSH Key', validators=[validators.DataRequired(), validate_ssh_key])
