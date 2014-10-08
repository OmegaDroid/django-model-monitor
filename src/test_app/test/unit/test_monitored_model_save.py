from django.test import TestCase
from test_app.models import MonitorAllFields


class MonitoredModelSave(TestCase):
    def test_save_after_change_to_monitored_field___has_changed_is_false(self):
        MonitorAllFields(first_field=1).save()
        m = MonitorAllFields.objects.first()
        m.first_field = 2
        m.save()

        self.assertEqual(2, m.first_field)
        self.assertFalse(m.has_changed())
