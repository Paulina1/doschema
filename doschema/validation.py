# -*- coding: utf-8 -*-
#
# This file is part of DoSchema.
# Copyright (C) 2016 CERN.
#
# DoSchema is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# DoSchema is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DoSchema; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Merger module."""

import collections
from doschema.errors import DoSchemaException, JSONSchemaCompatibilityException

def start(schemas_list, ignore_index=True, fields_types_dict={}):
    """Start processing a given list of schemas.

    :param schemas_list: List of schemas to check compatibility.
    :param ignore_index: If set to True, which is default, it will ignore
                         array indexes.
    """
    ind = 0
    for scheme in schemas_list:
        _JSONSchemaCompatibilityChecker(
            ind, (), scheme, ignore_index
        ).traverse(fields_types_dict)
        ind += 1

    return fields_types_dict


FieldToAdd = collections.namedtuple(
    'FieldToAdd',
    'schema_index field_tuple field_type'
)


class _JSONSchemaCompatibilityChecker(object):
    """Class for checking compatibility between schemas."""

    def __init__(self, schema_id, curr_field, curr_schema, ignore_index=True):
        """Constructor.

        :param schema_id: Index of schema that is currently processed.
        :param curr_field: Tuple with path to currently processed field.
        :param curr_schema: Schema or subschema that is currently processed.
        :param ignore_index: If set to True, which is default, it will ignore
                             array indexes.
        """
        self.schema_id = schema_id
        self.curr_field = curr_field
        self.curr_schema = curr_schema
        self.ignore_index = ignore_index

    def traverse(self, fields_types_dict):
        """Go through the schema and retrieve schema's particular fields.

        :param fields_types_dict: Dictionary keeping path and type of
                                  the field.
        """
        for field_name, field_value in self.curr_schema.items():
            if field_name in ['anyOf', 'allOf', 'oneOf']:
                self.collect_special(
                    fields_types_dict,
                    field_value
                )
            # if a value is a dict recursively comes into it
            elif isinstance(field_value, dict):
                _JSONSchemaCompatibilityChecker(
                    self.schema_id,
                    self.curr_field,
                    field_value,
                    self.ignore_index
                ).traverse(fields_types_dict)
            elif field_name == 'type':
                self.process_type_field(fields_types_dict, field_value)
            elif field_name == 'items':
                if isinstance(field_value, list):
                    self.process_array(fields_types_dict, field_value)

    def process_array(self, fields_types_dict, field_value):
        """Process each JSON object in the array according to ignore_index.

        :param fields_types_dict: Dictionary keeping path and type of
                                  the field.
        :param field_value: Type of the field.
        """
        field_path = self.curr_field + ('items', )
        print(fields_types_dict)
        for elem in field_value:
            if self.ignore_index:
                new_field_path = field_path
            else:
                new_field_path = field_path + (field_value.index(elem), )

            _JSONSchemaCompatibilityChecker(
                self.schema_id,
                new_field_path,
                elem,
                self.ignore_index
            ).traverse(fields_types_dict)

    def process_type_field(self, fields_types_dict, field_value):
        """Check if a name field with type "type" has already appeared.

        If had appeared with different type,raise an exception.
        Otherwise, add object to a dict of types.

        :param fields_types_dict: Dictionary keeping path and type of
                                  the field.
        :param field_name: Name of the field.
        :param field_value: Type of the field.
        """
        if self.curr_field in fields_types_dict.keys():
            if fields_types_dict[self.curr_field].field_type != field_value:
                err_msg = "Type mismatch in schemas {0} and {1}."
                old_schema = fields_types_dict[self.curr_field].schema_index
                raise JSONSchemaCompatibilityException(
                    old_schema,
                    self.schema_id,
                    err_msg.format(old_schema, self.schema_id)
                )
        else:
            fields_types_dict[self.curr_field] = FieldToAdd(
                schema_index = self.schema_id,
                field_tuple = self.curr_field,
                field_type = field_value
            )

    def collect_special(self, fields_types_dict, JSON_objects_list):
        """Operate a field with name 'allOf', 'anyOf' or 'oneOf'.

        :param fields_types_dict: Dictionary keeping path and type of
                                  the field.
        :param JSON_objects_list: List of JSON objects.
        """
        for elem in JSON_objects_list:
            _JSONSchemaCompatibilityChecker(
                self.schema_id,
                self.curr_field,
                elem,
                self.ignore_index
            ).traverse(fields_types_dict)


# class FieldToAdd(object):
#     """Class to keep field description."""

#     def __init__(self, schema_index, field_tuple, field_type):
#         """Constructor.

#         :param schema_index: Index of schema where field was first declared.
#         :param field_tuple: Tuple with path of a field.
#         :param field_type: Type of a field.
#         """
#         self.schema_index = schema_index
#         self.field_tuple = field_tuple
#         self.field_type = field_type
#

# class JSONSchemaCompatibilityException(Exception):
#     """Exception raised when a JSON schema is not backward compatible."""

#     def __init__(self, dict_of_args, *args, **kwargs):
#         """Constructor."""
#         super(JSONSchemaCompatibilityException, self).__init__(*args, **kwargs)
#         self.field_name = dict_of_args['field_name']
#         """Name of the field with wrong type."""
#         self.old_type = dict_of_args['old_type']
#         """Previous type of the field."""
#         self.old_schema = dict_of_args['old_schema']
#         """Index of schema in which field has occured before."""
#         self.new_type = dict_of_args['new_type']
#         """Type of field that has been tried to add."""
#         self.new_schema = dict_of_args['new_schema']
#         """Index of schema in which field occurs now."""

#     def __str__(self):
#         """Return the formatted error message string."""
#         return ("Field {0} already declared with type {1} in schema {2}."
#                 "It cannot be declared as {3} in schema {4}.").format(
#             self.field_name,
#             self.old_type,
#             self.old_schema,
#             self.new_type,
#             self.new_schema
#         )
