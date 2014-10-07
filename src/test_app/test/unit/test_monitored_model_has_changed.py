from django.test import TestCase
from test_app.models import MonitorAllFields, MonitorSomeFields


class MonitoredModelHasChanged(TestCase):
    def test_initialise_model_entry___result_is_false(self):
        MonitorAllFields(first_field=1).save()

        m = MonitorAllFields.objects.first()

        self.assertFalse(m.has_changed())

    def test_instance_is_changed___result_is_true(self):
        MonitorAllFields(first_field=1).save()

        m = MonitorAllFields.objects.first()
        m.first_field = 2

        self.assertTrue(m.has_changed())

    def test_instance_of_model_with_partially_monitored_fields_no_changes___result_is_false(self):
        MonitorSomeFields(monitored_field=1).save()

        m = MonitorSomeFields.objects.first()

        self.assertFalse(m.has_changed())

    def test_instance_of_model_with_partially_monitored_fields_change_to_monitored_field___result_is_true(self):
        MonitorSomeFields(monitored_field=1).save()

        m = MonitorSomeFields.objects.first()
        m.monitored_field = 2

        self.assertTrue(m.has_changed())

    def test_instance_of_model_with_partially_monitored_fields_change_to_unmonitored_field___result_is_false(self):
        MonitorSomeFields(unmonitored_field=1).save()

        m = MonitorSomeFields.objects.first()
        m.unmonitored_field = 2

        self.assertFalse(m.has_changed())
