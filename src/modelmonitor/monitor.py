import inspect
from django.db import models
from django.db.models.signals import post_init, post_save


class MonitorInstanceCache():
    """
    Holds the information about the last saved change of the model instance
    """
    def __init__(self, instance):
        self._cache = MonitorInstanceCache._extract_cache(instance)

    @staticmethod
    def _extract_cache(instance):
        """
        Extracts the cache from the model instance

        :param instance: The instance of the model to cache
        :return: A dictionary containing the original state of the object
        """
        monitored_fields = instance._monitored_fields
        fields = [
            field for field in instance._meta.local_fields if not monitored_fields or field.attname in monitored_fields
        ]

        return {field.attname: _process_field_value(type(field), getattr(instance, field.attname)) for field in fields}

    def is_different(self, instance):
        """
        Checks if the instance is the same as the cache. Only monitored fields will be checked.

        :param instance: The instance of the model to check against the cache
        :return: True if the instance does not matches the cache, False otherwise
        """
        return self._cache != MonitorInstanceCache._extract_cache(instance)

    def revert_instance(self, instance):
        """
        Reverts the model instance to it's original loaded value. Only monitored fields will be reverted

        :param instance: The instance to revert back to the original values.
        """
        for attr_name, value in self._cache.items():
            setattr(instance, attr_name, value)

    def get_changes(self, instance):
        """
        Gets all the monitored fields that have changed. Gives a dictionary of old and new values indexed against the
        attribute name eg:

        {
            "field_1": {"old": 1, "new": 2},
            "field_2": {"old": "foo", "new": "bar"}
        }

        :param instance: The instance of the model to check against the cache
        :return: A dictionary of ald and new values for monitored fields that have changed.
        """
        new_values = MonitorInstanceCache._extract_cache(instance)
        return {
            field: {"new": new_values[field], "old": self._cache[field]}
            for field in new_values if new_values[field] != self._cache[field]
        }


def _update_instance_cache(instance):
    """
    Updates the monitor cache of the model instance.

    :param instance: the model instance to update
    """
    instance._monitor_instance_cache = MonitorInstanceCache(instance)


def _on_init_cache_instance(sender, **kwargs):
    """
    Updates the monitor cache of the model instance. This is designed to be called on the post init signal of the
    instance

    :param sender: The class of the instance sending the signal
    :param kwargs: Keyword arguments sent by the signal (https://docs.djangoproject.com/en/1.7/ref/signals/#post-init)
    """
    _update_instance_cache(kwargs["instance"])


def _on_monitored_model_saved_cache_is_updated(sender, **kwargs):
    """
    Updates the monitor cache of the model instance on save. This is designed to be called on the post save signal of
    the instance

    :param sender: The class of the instance sending the signal
    :param kwargs: Keyword arguments sent by the signal (https://docs.djangoproject.com/en/1.7/ref/signals/#post-save)
    """
    _update_instance_cache(kwargs["instance"])


def changed(*monitored_fields):
    """
    Prepares the model for having it's instances monitored for changes.

    :param monitored_fields: The fields to monitor. If no fields are specified all fields are monitored.
    """
    def _decoration(fields, cls):
        cls._monitored_fields = fields
        cls.has_changed = lambda self: self._monitor_instance_cache.is_different(self)
        cls.revert = lambda self: self._monitor_instance_cache.revert_instance(self)
        cls.get_changes = lambda self: self._monitor_instance_cache.get_changes(self)

        post_init.connect(
            _on_init_cache_instance,
            sender=cls,
            dispatch_uid="__{class_name}_changed_post_init_dispatcher__".format(class_name=cls.__name__)
        )

        post_save.connect(
            _on_monitored_model_saved_cache_is_updated,
            sender=cls,
            dispatch_uid="__{class_name}_saved_post_save_dispatcher__".format(class_name=cls.__name__)
        )

        return cls

    # this is some hacking to allow @monitor.changed to be used as the decorator rather then
    # @monitor.changed()
    if len(monitored_fields) == 1 and inspect.isclass(monitored_fields[0]):
        return _decoration([], monitored_fields[0])
    else:
        return lambda cls: _decoration(monitored_fields, cls)


#
# Functions for handling extracting cache values from mutable fields
#

# a dictionary of field value processors indexed against
_field_value_processors = {}


def register_value_processor(field_class, processor):
    """
    Registers a function for handling values from mutable fields

    :param field_class: The class to register the processor for
    :param processor:   The processor function, this should take the field value as its arguments and return the value to cache
    """
    _field_value_processors[field_class] = processor


def _process_field_value(field_class, field_value):
    """
    Processes a model field and returns its cache value

    :param field_class: The class of the field
    :param field_value: The value of the field
    :return: The cache value
    """
    if field_class in _field_value_processors:
        return _field_value_processors[field_class](field_value)
    return field_value


def _file_field_value(field_value):
    """
    Processes the file object into the upload path

    :param field_value: The value of the field to process
    """
    if field_value:
        return field_value.path
    return None
register_value_processor(models.FileField, _file_field_value)