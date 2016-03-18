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

import pytest

from doschema.errors import DoSchemaException, JSONSchemaCompatibilityException
from doschema.validation import start


def test_special_field_fail():
    v1 = {
        "type": "object",
        "oneOf": [{
            "type": "object",
            "properties": {
                "field_A": {"type": "string"}
            }
        }, {
            "type": "object",
            "properties": {
                "field_A": {"type": "integer"}
            }
        }]
    }
    schema_list = [v1]
    with pytest.raises(JSONSchemaCompatibilityException):
        start(schema_list)


def test_special_field_pass():
    v1 = {
        "type": "object",
        "oneOf": [{
            "type": "object",
            "properties": {
                "field_A": {"type": "string"}
            }
        }, {
            "type": "object",
            "properties": {
                "field_B": {"type": "integer"}
            }
        }]
    }
    schema_list = [v1]
    start(schema_list)


def test_success_two_schemas():
    v1 = {
        "type": "object",
        "properties": {
            "field_A": {"type": "string"}
        },
        "required": ["field_A"]
    }
    v2 = {
        "type": "object",
        "properties": {
            "field_B": {"type": "string"}
        },
        "required": ["field_B"]
    }
    schema_list = [v1, v2]
    start(schema_list)


def test_failure_between_schemas():
    v1 = {
        "type": "object",
        "properties": {
            "field_A": {"type": "string"}
        },
        "required": ["field_A"]
    }
    v2 = {
        "type": "object",
        "properties": {
            "field_B": {"type": "string"}
        },
        "required": ["field_B"]
    }
    v3 = {
        "type": "object",
        "properties": {
            "field_B": {"type": "string"},
            "field_A": {"type": "number"}
        },
        "required": ["field_B"]
    }
    schema_list = [v1, v2, v3]
    with pytest.raises(JSONSchemaCompatibilityException):
        start(schema_list)


def test_ignoring_indexes():  # can be the same
    v1 = {
        "type": "object",
        "properties": {
            "experiment_info": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "string"}
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "number"}
                        }
                    }
                ]
            }
        }
    }
    schema_list = [v1]
    with pytest.raises(JSONSchemaCompatibilityException):
        start(schema_list, True)


def test_not_ignoring_indexes():
    v1 = {
        "type": "object",
        "properties": {
            "experiment_info": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "string"}
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "number"}
                        }
                    }
                ]
            }
        }
    }
    schema_list = [v1]
    start(schema_list, False)
