from django.test import TestCase
from test_app.models import MonitorAllFields, MonitorSomeFields


class MonitoredModelGetChanges(TestCase):
    def test_monitor_all_fields_no_changes___result_is_empty_dict(self):
        m = MonitorAllFields(first_field=1)

        self.assertEqual({}, m.get_changes())

    def test_monitor_all_fields_all_fields_changed___result_contains_the_old_and_new_values_for_all_fields(self):
        m = MonitorAllFields(first_field=1, second_field=3)
        m.first_field = 2
        m.second_field = 4

        self.assertEqual({
            "first_field": {"old": 1, "new": 2},
            "second_field": {"old": 3, "new": 4}
        }, m.get_changes())

    def test_monitor_all_fields_single_field_changed___result_contains_the_changed_fields_old_and_new_values(self):
        m = MonitorAllFields(first_field=1, second_field=3)
        m.first_field = 2

        self.assertEqual({
            "first_field": {"old": 1, "new": 2},
        }, m.get_changes())

    def test_monitor_some_fields_change_monitored_fields___result_contains_the_changed_fields_old_and_new_values(self):
        m = MonitorSomeFields(monitored_field=1)
        m.monitored_field = 2

        self.assertEqual({
            "monitored_field": {"old": 1, "new": 2},
        }, m.get_changes())

    def test_monitor_some_fields_change_unmonitored_fields___result_is_empty_dict(self):
        m = MonitorSomeFields(unmonitored_field=1)
        m.unmonitored_field = 2

        self.assertEqual({}, m.get_changes())