"""
Module openvolunteer.bigint

A fix for the rather well-known ticket #399 in the django project.

Create and link to auto-incrementing primary keys of type bigint without
having to reload the model instance after saving it to get the ID set in
the instance.

By: Florian Leitner
"""

from django.core import exceptions
from django.conf import settings
from django.db import connection
from django.db.models import fields
from django.utils.translation import ugettext as _

class BigIntegerField(fields.IntegerField):
    """
    Provide a way to use bigint in django.
    """    
    def db_type(self):
        if settings.DATABASE_ENGINE == 'mysql':
            return "bigint"
        elif settings.DATABASE_ENGINE == 'oracle':
            return "NUMBER(19)"
        elif settings.DATABASE_ENGINE[:8] == 'postgres':
            return "bigint"
        else:
            raise NotImplemented
    
    def get_internal_type(self):
        return "BigIntegerField"
    
    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))
