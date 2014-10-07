import inspect
from django.db.models.signals import post_init


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

        return {field.attname: getattr(instance, field.attname) for field in fields}

    def is_different(self, instance):
        return self._cache != MonitorInstanceCache._extract_cache(instance)


def _on_init_cache_instance(sender, **kwargs):
    """
    Updates the monitor cache of the model instance. This is designed to be called on the post init signal of the
    instance

    :param sender: The class of the instance sending the signal
    :param kwargs: Keyword arguments sent by the signal (https://docs.djangoproject.com/en/1.7/ref/signals/#post-init)
    """
    instance = kwargs["instance"]
    instance._monitor_instance_cache = MonitorInstanceCache(instance)


def changed(*monitored_fields):
    """
    Prepares the model for having it's instances monitored for changes.

    :param monitored_fields: The fields to monitor. If no fields are specified all fields are monitored.
    """
    def _decoration(fields, cls):
        cls._monitored_fields = fields
        cls.has_changed = lambda self: self._monitor_instance_cache.is_different(self)

        post_init.connect(
            _on_init_cache_instance,
            sender=cls,
            dispatch_uid="__{class_name}_changed_post_init_dispatcher__".format(class_name=cls.__name__)
        )

        return cls

    if len(monitored_fields) == 1 and inspect.isclass(monitored_fields[0]):
        return _decoration([], monitored_fields[0])
    else:
        return lambda cls: _decoration(monitored_fields, cls)
