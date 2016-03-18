# -*- coding: utf-8 -*-
#
# This file is part of DoSchema
# Copyright (C) 2016 CERN.
#
# DoSchema is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define all DoSchema exceptions."""


class DoSchemaException(Exception):
    """Parent for all DoSchema exceptions.
    .. versionadded:: 1.0.0
    """

class JSONSchemaCompatibilityException(DoSchemaException):
    """Exception raised when a JSON schema is not backward compatible."""

    def __init__(self, old_schema, new_schema, err_msg):
        """Constructor."""
#        super(JSONSchemaCompatibilityException, self).__init__(*args, **kwargs)
        # self.old_schema = dict_of_args['old_schema']
        # """Index of schema in which field has occured before."""
        # self.new_schema = dict_of_args['new_schema']
        # """Index of schema in which field occurs now."""
        # self.err_msg = dict_of_args['err_msg']
        # """Error message."""
        self.old_schema = old_schema
        """Index of schema in which field has occured before."""
        self.new_schema = new_schema
        """Index of schema in which field occurs now."""
        self.err_msg = err_msg
        """Error message."""
