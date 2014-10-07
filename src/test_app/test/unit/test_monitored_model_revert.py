from django.test import TestCase
from test_app.models import MonitorAllFields, MonitorSomeFields


class MonitoredModelRevert(TestCase):
    def test_instance_is_changed___reverted_to_its_original_value(self):
        m = MonitorAllFields(first_field=1)
        m.first_field = 2
        m.revert()

        self.assertEqual(1, m.first_field)

    def test_instance_of_model_with_partially_monitored_fields_change_to_monitored_field___reverted_to_its_original_value(self):
        m = MonitorSomeFields(monitored_field=1)
        m.monitored_field = 2
        m.revert()

        self.assertEqual(1, m.monitored_field)

    def test_instance_of_model_with_partially_monitored_fields_change_to_unmonitored_field___not_reverted_to_its_original_value(self):
        m = MonitorSomeFields(unmonitored_field=1)
        m.unmonitored_field = 2
        m.revert()

        self.assertEqual(2, m.unmonitored_field)

