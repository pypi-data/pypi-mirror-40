# -*- coding: utf-8 -*-

"""
    Created on 06.10.16
    @author: druid
"""
import warnings

_drf_support = True

try:
    from rest_framework.fields import ChoiceField, empty, SkipField
    from django.utils.translation import ugettext_lazy as _
    from rest_framework.serializers import Serializer, set_value, OrderedDict, ValidationError, \
        api_settings, ListSerializer, html

except ImportError:
    warnings.warn("Trying to import drf serializers field. but django-rest-framework package"
                  "is not available.")
    _drf_support = False

from .pool import PoolInterface


if _drf_support:
    class PoolChoiceField(ChoiceField):

        """
            Type choice field for DRF serializers which works with class pools.
        """

        empty_label = _('Select type')
        exclude_types = ()

        def __init__(self, pool, *args, **kwargs):
            self._builded_choices = None

            assert isinstance(pool, PoolInterface), "Pool has to implement PoolInterface"
            self._pool = pool

            if 'choices' not in kwargs:
                kwargs['choices'] = self.build_choices()

            super(PoolChoiceField, self).__init__(*args, **kwargs)

        @property
        def pool(self):
            return self._pool

        def get_value(self, dictionary):
            value = super(PoolChoiceField, self).get_value(dictionary)

            # always replace empty value by default
            # DRF do that only if root serializer has partial=False, but type field is required even if serializer
            # is created with partial=True
            # It is still allowed to return empty as a value, just use empty as default value
            if value is empty:
                try:
                    value = self.get_default()
                except SkipField:
                    return empty

            return value

        def build_choices(self):

            if self._builded_choices is None:

                self._builded_choices = list(
                    (type_code, getattr(klass, 'verbose_name', type_code))
                    for type_code, klass in self._pool if type_code not in self.exclude_types
                )

            return self._builded_choices


    class BasePoolSerializer(Serializer):

        # PoolSerializers inherits from Serializer to support DRF fields nesting,
        # however it should inherit from BaseSerializer because none of functionality
        # provided by Serializer class is used. Unfortunately, DRF commonly test if
        # class is a subclass of Serializer (not BaseSerializer) to handle
        # serializers with nested fields, so this class has to inherit from Serializer
        # to behave the same as all other serializers...

        default_error_messages = {
            'invalid': _('Invalid data. Expected a dictionary, but got {datatype}.'),
            'missing_type': _('Data type is required'),
            'type_not_supported': _('Given type `{type_code}` is not supported'),
            'type_failed': _("Given type is not valid. {error}")
        }

        append_type_representation = True
        append_type_value = True

        def __init__(self, *args, **kwargs):

            self._pool = kwargs.pop('pool')
            self._serializer = None
            super(BasePoolSerializer, self).__init__(*args, **kwargs)

        def fail(self, *args, **kwargs):
            try:
                super(BasePoolSerializer, self).fail(*args, **kwargs)
            except ValidationError as exc:
                raise ValidationError({
                    api_settings.NON_FIELD_ERRORS_KEY: exc.detail
                })

        def get_type_field(self):
            """
            Returns a field which represents type. This field will be used to determine what is the type of
            serialized object and thus which serializer from the pool should be used.
            :return:
            """
            raise NotImplementedError()

        def get_serializer_class(self, type_code):
            """
            Basing on given type code returns appropriate serializer from the pool.
            :param type_code:
            :return:
            """

            return self._pool.get(type_code)

        def get_serializer_kwargs(self, **extra):
            """
            Returns dict of arguments which should be passed to actual data serializer
            :param extra:
            :return:
            """
            kwargs = {
                'context': self.context,
                'partial': self.partial,
                'instance': self.instance
            }
            kwargs.update(extra)
            return kwargs

        def get_serializer(self, type_code, **kwargs):
            """
            Returns actual serializer for data basing on given type code.
            :param type_code:
            :param kwargs:
            :return:
            """
            if self._serializer is None or self._serializer._type_code != type_code:

                kwargs = self.get_serializer_kwargs(**kwargs)
                serializer_cls = self.get_serializer_class(type_code)
                if serializer_cls is None:
                    return None

                self._serializer = serializer_cls(**kwargs)
                if self.parent is not None:
                    # if field is bound, bind dynamic serializer in the same way,
                    # if not it means that PoolSerializer is a root and there is nothing to bind
                    self._serializer.bind(self.field_name, self.parent)

                self._serializer._type_code = type_code

            return self._serializer

        def get_type_value(self, data):
            type_field = self.get_type_field()
            return type_field.get_value(data)

        def get_type_attribute(self, instance):
            type_field = self.get_type_field()
            # instance could be a dict of validated data or model instance,
            # both are dict accessible
            type_value = type_field.get_attribute(instance)
            return type_value

        def run_internal_validation(self, type_code, data):
            serializer = self.get_serializer(type_code)
            if serializer is None:
                self.fail('type_not_supported', type_code=type_code)

            return serializer.run_validation(data)

        def to_internal_value(self, data):

            if not isinstance(data, dict):
                self.fail('invalid', datatype=data.__class__.__name__)

            type_field = self.get_type_field()
            primitive_value = self.get_type_value(data)
            try:
                type_code = type_field.run_validation(primitive_value)
            except ValidationError as exc:
                self.fail('type_failed', error=', '.join(exc.detail))

            data = self.run_internal_validation(type_code, data)

            # join serialized data and type code value
            if self.append_type_value:
                try:
                    set_value(data, type_field.source_attrs, type_code)
                except (KeyError, AttributeError):
                    # probably type field is virtual and is not a really field
                    # but maybe a property or is discovered dynamically by subclass in
                    # other way
                    pass

            return data

        def to_representation(self, instance):

            type_field = self.get_type_field()
            type_value = self.get_type_attribute(instance)

            serializer = self.get_serializer(type_value)
            if serializer is None:
                raise AssertionError("Cannot represent instance, "
                                     "because there type '{}' is not supported".format(type_value))

            ret = serializer.to_representation(instance)

            if self.append_type_representation and not type_field.write_only:
                # if type field is not write_only, include type value to the representation
                ret[type_field.field_name] = type_field.to_representation(type_value)

            return ret

        def update(self, instance, validated_data):
            type_field = self.get_type_field()

            if 'type' in validated_data:
                primitive_value = self.get_type_value(validated_data)
                type_code = type_field.to_internal_value(primitive_value)
            else:
                type_value = self.get_type_attribute(instance)
                type_code = type_field.to_representation(type_value)

            return self.get_serializer(type_code).update(instance, validated_data)

        def create(self, validated_data):
            type_field = self.get_type_field()

            #primitive_value = type_field.get_value(validated_data)
            #type_code = type_field.to_internal_value(primitive_value)
            type_code = type_field.get_attribute(validated_data)

            assert type_code is not None, "Cannot determine type from data %r" % validated_data

            return self.get_serializer(type_code).create(validated_data)

        def __repr__(self):
            return "%s<%s>" % (self.__class__.__name__, self._pool.__class__.__name__)


    class PoolSerializer(BasePoolSerializer):
        """
        Dynamic serializer which serializes given data according to 'type'
        field value. Use this serializer if type field is given along with object data.
        Example:
            {
                "type": 1,
                "id': ...
                "propertyA":...
                "propertyB":...
            }
        """

        def __init__(self, *args, **kwargs):
            self._type_field = None
            super(PoolSerializer, self).__init__(*args, **kwargs)

        @property
        def type_field(self):
            if self._type_field is None:
                self._type_field = self.build_pool_choice_field()
            return self._type_field

        @property
        def fields(self):
            # do not return fields as BindingDict (default for DRF),
            # because fields are already bound to proper serializers
            # this property should only join items of two dicts
            # into one, without modifying source dicts but using
            # the same referenced field instances (so deepcopy is not
            # a solution). The simplest way is to get items tuples,
            # concatenate and return as an OrderedDict (to keep fields
            # order, put type field at the beginning)

            ret = tuple(super(PoolSerializer, self).fields.items())

            if self._serializer is not None:
                ret += tuple(self._serializer.fields.items())

            return OrderedDict(ret)

        def get_fields(self):
            return {
                'type': self.type_field
            }

        def get_pool_choice_field_class(self):
            return PoolChoiceField

        def get_pool_choice_field_kwargs(self):
            return {
                'pool': self._pool,
            }

        def build_pool_choice_field(self):
            kwargs = self.get_pool_choice_field_kwargs()
            field = self.get_pool_choice_field_class()(**kwargs)
            return field

        def get_type_field(self):
            return self.fields['type']


    class TypedSerializer(BasePoolSerializer):
        """
        Dynamic serializer for sub-objects which structure depends on type field
        given outside dumped object data (in parent serializer).
        Example:
            {
                "type": 1,
                "data": {
                    ... data of object type 1 ...
                }
            }
        """

        type_pass_key = '_typedSerializerType'

        append_type_representation = False
        append_type_value = False

        def __init__(self, field_name='type', *args, **kwargs):
            self.type_field_name = field_name
            super(TypedSerializer, self).__init__(*args, **kwargs)

        def get_type_field(self):
            assert self.parent is not None, "Parent serializer not given!"
            try:
                return self.parent.fields[self.type_field_name]
            except KeyError:
                raise AssertionError("Type field '{}' not found in parent serializer '{}'".format(
                    self.type_field_name, self.parent
                ))

        def get_type_attribute(self, instance):
            return instance['_typedSerializerType'] if isinstance(instance, dict) else instance._typedSerializerType

        def get_type_value(self, data):
            return data['_typedSerializerType'] if isinstance(data, dict) else data._typedSerializerType

        def get_attribute(self, instance):
            ret = super(TypedSerializer, self).get_attribute(instance)
            type_attr = self.get_type_field().get_attribute(instance)

            if ret is None:
                if not self.allow_null:
                    if not self.required:
                        raise SkipField()
                    else:
                        raise ValueError(f"Not allowed 'None' value for required field `{self.field_name}` "
                                         f"on serializer `{self.parent.__class__.__name__}` for "
                                         f"`{instance.__class__.__name__}` instance.")
            elif isinstance(ret, dict):
                ret[self.type_pass_key] = type_attr
            else:
                try:
                    setattr(ret, self.type_pass_key, type_attr)
                except:
                    raise NotImplementedError()

            return ret

        def validate_empty_values(self, data):
            is_empty, data = super().validate_empty_values(data)

            if isinstance(data, dict) and len(data) == 1 and self.type_pass_key in data:
                # if the only key in dict is type passing key, dict is empty
                # empty dicts should be considered as empty value
                return True, {}

            return is_empty, data

        def get_value(self, dictionary):
            ret = super(TypedSerializer, self).get_value(dictionary)
            type_attr = self.get_type_field().get_value(dictionary)

            if isinstance(ret, dict):
                ret[self.type_pass_key] = type_attr
            elif ret is not empty:
                if ret is None:
                    return None
                try:
                    setattr(ret, self.type_pass_key, type_attr)
                except:
                    raise NotImplementedError()

            return ret

else:
    def PoolChoiceField(*args, **kwargs):
        raise Exception("Django REST Framework cannot be imported. Serializer field is not available")
