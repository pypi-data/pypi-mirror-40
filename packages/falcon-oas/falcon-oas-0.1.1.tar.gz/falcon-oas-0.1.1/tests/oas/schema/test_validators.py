# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from falcon_oas.oas.schema.validators import SchemaValidator
from falcon_oas.oas.schema.validators import ValidationError
from falcon_oas.oas.spec import create_spec_from_dict


@pytest.fixture
def schema():
    return {'type': str('string')}


@pytest.fixture
def spec(schema):
    return create_spec_from_dict({'a': {'b': schema}})


@pytest.fixture
def reference():
    return {'$ref': '#/a/b'}


def test_validate_success(spec, reference):
    instance = 'foo'
    try:
        SchemaValidator(spec).validate(instance, reference)
    except ValidationError as e:
        pytest.fail('Unexpected error: {}'.format(e))


def test_validate_error(spec, reference):
    instance = 123
    message = "123 is not of type 'string'"

    with pytest.raises(ValidationError) as exc_info:
        SchemaValidator(spec).validate(instance, reference)

    assert exc_info.value.errors[0].message == message


def test_validate_format_date(spec, schema, reference):
    schema['format'] = 'date'
    instance = '2018-01-02'
    try:
        SchemaValidator(spec).validate(instance, reference)
    except ValidationError as e:
        pytest.fail('Unexpected error: {}'.format(e))


def test_validate_format_date_error(spec, schema, reference):
    schema['format'] = str('date')
    instance = str('2018/01/02')
    message = "'2018/01/02' is not a 'date'"

    with pytest.raises(ValidationError) as exc_info:
        SchemaValidator(spec).validate(instance, reference)

    assert exc_info.value.errors[0].message == message


def test_validate_format_date_time(spec, schema, reference):
    schema['format'] = 'date-time'
    instance = '2018-01-02T03:04:05Z'
    try:
        SchemaValidator(spec).validate(instance, reference)
    except ValidationError as e:
        pytest.fail('Unexpected error: {}'.format(e))


def test_validate_format_date_time_error(spec, schema, reference):
    schema['format'] = str('date-time')
    instance = str('2018-01-02T03:04:05')
    message = "'2018-01-02T03:04:05' is not a 'date-time'"

    with pytest.raises(ValidationError) as exc_info:
        SchemaValidator(spec).validate(instance, reference)

    assert exc_info.value.errors[0].message == message


@pytest.mark.parametrize(
    'instance',
    [
        'http://example.com',
        'http://example.com/',
        'http://example.com/path',
        'http://example.com/path?query#segment',
        'https://example.com',
    ],
)
def test_validate_format_uri(spec, schema, reference, instance):
    schema['format'] = 'uri'
    try:
        SchemaValidator(spec).validate(instance, reference)
    except ValidationError as e:
        pytest.fail('Unexpected error: {}'.format(e))


@pytest.mark.parametrize(
    'instance',
    [str('http'), str('http://'), str('example.com'), str('example.com/path')],
)
def test_validate_format_uri_error(spec, schema, reference, instance):
    schema['format'] = str('uri')
    message = "'" + instance + "' is not a 'uri'"

    with pytest.raises(ValidationError) as exc_info:
        SchemaValidator(spec).validate(instance, reference)

    assert exc_info.value.errors[0].message == message


def test_validate_without_parsers(spec, schema, reference):
    schema['format'] = 'date'
    instance = '2018/01/02'
    try:
        SchemaValidator(spec, parsers={}).validate(instance, reference)
    except ValidationError as e:
        pytest.fail('Unexpected error: {}'.format(e))


def test_validate_format_non_string(spec, schema, reference):
    schema['format'] = 'date'
    instance = 123
    message = "123 is not of type 'string'"

    with pytest.raises(ValidationError) as exc_info:
        SchemaValidator(spec).validate(instance, reference)

    assert exc_info.value.errors[0].message == message
