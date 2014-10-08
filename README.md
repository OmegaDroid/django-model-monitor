django-model-monitor
====================

App to monitor changes in models

Usage
=====

To monitor all fields in the model use:

```python
from django.db import models
from modelmonitor import monitor

@monitor.changed
class TestModel(models.Model):
	first_field = models.IntegerField(default=0)
	second_field = models.IntegerField(default=0)
	third_field = models.IntegerField(default=0)
```

In this example changes to first_field, second_field and third_field will be monitored for changes.

To monitor specific fields use:

```python
from django.db import models
from modelmonitor import monitor

@monitor.changed("first_field", "second_field")
class TestModel(models.Model):
	first_field = models.IntegerField(default=0)
	second_field = models.IntegerField(default=0)
	third_field = models.IntegerField(default=0)
```

In this example first_field and second_field will be monitored for changes but third_field will not.

The decorator adds a few methods to each of your model instances.
* has_changed - Checks if any of the monitored fields for a  model instance have changed since the last time it was 
saved.
* revert - Resets all monitored fields on an instance back to the state they were in at the last time the instance was 
saved.
* get_changes - Gets a dictionary with all old and new values for changed monitored fields. 
