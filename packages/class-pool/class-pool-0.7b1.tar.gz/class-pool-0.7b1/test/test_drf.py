from unittest import TestCase, mock

import django
from django.conf import settings
settings.configure(mock.Mock(
    INSTALLED_APPS=(),
    LANGUAGE_CODE='en',
    LOGGING_CONFIG=None,
    LOGGING=None,
    LOCALE_PATHS=(),
    REST_FRAMEWORK={}
))
django.setup()

from rest_framework import serializers

from class_pool.drf import TypedSerializer


class PoolSerializerTestCase(TestCase):

    def test_required(self):
        pass


class TypedSerializerTestCase(TestCase):

    def test_typed_required_failed_empty(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'existing',
        })

        serializer.is_valid()
        self.assertIn('data', serializer.errors)
        self.assertIn('non_field_errors', serializer.errors['data'])
        self.assertEqual(serializer.errors['data']['non_field_errors'][0].code, 'required')

    def test_typed_required_empty_given(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'existing',
            'data': {}
        })

        self.assertTrue(serializer.is_valid())
        self.assertIn('data', serializer.validated_data)
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'existing',
            'data': {}
        })

    def test_typed_required_not_empty_given(self):

        class FooSerializer(serializers.Serializer):
            foo = serializers.CharField()

        pool = mock.Mock(
            get=mock.Mock(return_value=FooSerializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'existing',
            'data': {
                'foo': 'bar'
            }
        })

        self.assertTrue(serializer.is_valid())
        self.assertIn('data', serializer.validated_data)
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'existing',
            'data': {
                'foo': 'bar'
            }
        })

    def test_typed_not_required_not_given(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', required=False)

        serializer = ExampleTyped(data={
            'type_field': 'existing',
        })

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'existing'
        })

    def test_typed_required_partial(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'existing',
        }, partial=True)

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'existing'
        })

    def test_typed_notnullable_failing_null(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'existing',
            'data': None
        })

        serializer.is_valid()
        self.assertIn('data', serializer.errors)
        self.assertIn('non_field_errors', serializer.errors['data'])
        self.assertEqual(serializer.errors['data']['non_field_errors'][0].code, 'null')

    def test_typed_nullable_null_given(self):

        pool = mock.Mock(
            get=mock.Mock(return_value=serializers.Serializer)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', allow_null=True)

        serializer = ExampleTyped(data={
            'type_field': 'existing',
            'data': None
        })

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'existing',
            'data': None
        })

    def test_missing_typed_required(self):
        """
        Missing serializer in the pool, but serializer is mark as required.
        Expected: ValidationError
        :return:
        """
        pool = mock.Mock(
            get=mock.Mock(return_value=None)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field')

        serializer = ExampleTyped(data={
            'type_field': 'missing',
            'data': {
                'foo': 'bar'
            }
        })

        serializer.is_valid()
        self.assertIn('data', serializer.errors)
        self.assertIn('non_field_errors', serializer.errors['data'])
        self.assertEqual(serializer.errors['data']['non_field_errors'][0].code, 'type_not_supported')

    def test_missing_typed_not_required_value_given(self):
        """
        Missing serializer in the pool, serializer mark as not required, no value given
        Expected: ValidationError
        :return:
        """
        pool = mock.Mock(
            get=mock.Mock(return_value=None)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', required=False)

        serializer = ExampleTyped(data={
            'type_field': 'missing',
            'data': {
                'foo': 'bar'
            }
        })

        serializer.is_valid()
        self.assertIn('data', serializer.errors)
        self.assertIn('non_field_errors', serializer.errors['data'])
        self.assertEqual(serializer.errors['data']['non_field_errors'][0].code, 'type_not_supported')

    def test_missing_typed_not_required_empty_given(self):
        """
        Missing serializer in the pool, serializer mark as blank, empty value (empty dict) given
        Expected: empty dict at output
        :return:
        """

        pool = mock.Mock(
            get=mock.Mock(return_value=None)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', required=False)

        serializer = ExampleTyped(data={
            'type_field': 'missing',
            'data': {}
        })

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'missing',
            'data': {}
        })

    def test_missing_typed_not_required_null_given(self):
        """
        Missing serializer in the pool, serializer mark as blank, empty value (empty dict) given
        Expected: empty dict at output
        :return:
        """

        pool = mock.Mock(
            get=mock.Mock(return_value=None)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', required=False)

        serializer = ExampleTyped(data={
            'type_field': 'missing',
            'data': None
        })

        serializer.is_valid()
        self.assertIn('data', serializer.errors)
        self.assertIn('non_field_errors', serializer.errors['data'])
        self.assertEqual(serializer.errors['data']['non_field_errors'][0].code, 'null')

    def test_missing_typed_nullable_null_given(self):
        """
        Missing serializer in the pool, serializer mark as not required, no value given
        Expected: None at output
        :return:
        """
        pool = mock.Mock(
            get=mock.Mock(return_value=None)
        )

        class ExampleTyped(serializers.Serializer):
            type_field = serializers.CharField()
            data = TypedSerializer(pool=pool, field_name='type_field', allow_null=True)

        serializer = ExampleTyped(data={
            'type_field': 'missing',
            'data': None
        })

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, {
            'type_field': 'missing',
            'data': None
        })
