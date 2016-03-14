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

from doschema.merger import FieldToAdd, JsonSchemaCompatibilityChecker, \
    JsonSchemaCompatibilityException


def test_collect():
    schemik = {
        "type": "object",
        "properties": {
            "field_A": {"type": "string"}
        },
        "required": ["field_A"]
    }
    fields_types_dict = {}
    JsonSchemaCompatibilityChecker(0, (), schemik).traverse(fields_types_dict)
    assert () in fields_types_dict.keys()
    assert ('properties', 'field_A') in fields_types_dict.keys()
    assert isinstance(fields_types_dict[()], FieldToAdd)
    assert isinstance(fields_types_dict[('properties', 'field_A')], FieldToAdd)
    assert fields_types_dict[()].field_type == 'object'
    assert fields_types_dict[('properties', 'field_A')].field_type == 'string'


def test1_fail():
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
    with pytest.raises(JsonSchemaCompatibilityException):
        JsonSchemaCompatibilityChecker.starter(schema_list)


def test1_pass():
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
    JsonSchemaCompatibilityChecker.starter(schema_list)


def test2_collect():
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
    JsonSchemaCompatibilityChecker.starter(schema_list)


def test3_collect():
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
    with pytest.raises(JsonSchemaCompatibilityException):
        JsonSchemaCompatibilityChecker.starter(schema_list)


def test3_1_ignore():  # can be the same
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
    with pytest.raises(JsonSchemaCompatibilityException):
        JsonSchemaCompatibilityChecker.starter(schema_list, True)


def test3_1_noIgnore():
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
    JsonSchemaCompatibilityChecker.starter(schema_list, False)
