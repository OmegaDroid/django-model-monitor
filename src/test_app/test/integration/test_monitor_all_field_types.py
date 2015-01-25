from datetime import date, datetime
from django.core.files import File
from django.test import TestCase
from django.utils.timezone import utc
import os
from test_app.models import AllFieldTypes


class MonitorAllFieldTypes(TestCase):
    def test_no_fields_changed___has_changed_is_false(self):
        m = AllFieldTypes()

        self.assertFalse(m.has_changed())

    def test_change_big_int_field___has_changed_is_true(self):
        m = AllFieldTypes(big_int_field=1)

        m.big_int_field = 2

        self.assertTrue(m.has_changed())

    def test_change_big_int_field___get_changes_has_the_change(self):
        m = AllFieldTypes(big_int_field=1)

        m.big_int_field = 2

        self.assertEqual({"big_int_field": {"old": 1, "new": 2}}, m.get_changes())

    def test_change_int_field___has_changed_is_true(self):
        m = AllFieldTypes(int_field=1)

        m.int_field = 2

        self.assertTrue(m.has_changed())

    def test_change_int_field___get_changes_has_the_change(self):
        m = AllFieldTypes(int_field=1)

        m.int_field = 2

        self.assertEqual({"int_field": {"old": 1, "new": 2}}, m.get_changes())

    def test_change_binary_field___has_changed_is_true(self):
        m = AllFieldTypes(bin_field=b"some bytes")

        m.bin_field = b"some other bytes"

        self.assertTrue(m.has_changed())

    def test_change_binary_field___get_changes_has_the_change(self):
        m = AllFieldTypes(bin_field=b"some bytes")

        m.bin_field = b"some other bytes"

        self.assertEqual({"bin_field": {"old": b"some bytes", "new": b"some other bytes"}}, m.get_changes())

    def test_change_bool_field___has_changed_is_true(self):
        m = AllFieldTypes(bool_field=True)

        m.bool_field = False

        self.assertTrue(m.has_changed())

    def test_change_bool_field___get_changes_has_the_change(self):
        m = AllFieldTypes(bool_field=True)

        m.bool_field = False

        self.assertEqual({"bool_field": {"old": True, "new": False}}, m.get_changes())

    def test_change_char_field___has_changed_is_true(self):
        m = AllFieldTypes(char_field="some chars")

        m.char_field = "some other chars"

        self.assertTrue(m.has_changed())

    def test_change_char_field___get_changes_has_the_change(self):
        m = AllFieldTypes(char_field="some chars")

        m.char_field = "some other chars"

        self.assertEqual({"char_field": {"old": "some chars", "new": "some other chars"}}, m.get_changes())

    def test_change_csv_field___has_changed_is_true(self):
        m = AllFieldTypes(csv_field="1,2,3")

        m.csv_field = "4,5,6"

        self.assertTrue(m.has_changed())

    def test_change_csv_field___get_changes_has_the_change(self):
        m = AllFieldTypes(csv_field="1,2,3")

        m.csv_field = "4,5,6"

        self.assertEqual({"csv_field": {"old": "1,2,3", "new": "4,5,6"}}, m.get_changes())

    def test_change_date_field___has_changed_is_true(self):
        m = AllFieldTypes(date_field=date(2014, 1, 1))

        m.date_field = date(2014, 1, 2)

        self.assertTrue(m.has_changed())

    def test_change_date_field___get_changes_has_the_change(self):
        m = AllFieldTypes(date_field=date(2014, 1, 1))

        m.date_field = date(2014, 1, 2)

        self.assertEqual({"date_field": {"old": date(2014, 1, 1), "new": date(2014, 1, 2)}}, m.get_changes())

    def test_change_date_time_field___has_changed_is_true(self):
        m = AllFieldTypes(date_time_field=datetime(2014, 1, 1, tzinfo=utc))

        m.date_time_field = datetime(2014, 1, 2, tzinfo=utc)

        self.assertTrue(m.has_changed())

    def test_change_date_time_field___get_changes_has_the_change(self):
        m = AllFieldTypes(date_time_field=datetime(2014, 1, 1, tzinfo=utc))

        m.date_time_field = datetime(2014, 1, 2, tzinfo=utc)

        self.assertEqual({
            "date_time_field": {
                "old": datetime(2014, 1, 1, tzinfo=utc),
                "new": datetime(2014, 1, 2, tzinfo=utc)
            }
        }, m.get_changes())

    def test_change_decimal_field___has_changed_is_true(self):
        m = AllFieldTypes(decimal_field=1)

        m.decimal_field = 2

        self.assertTrue(m.has_changed())

    def test_change_decimal_field___get_changes_has_the_change(self):
        m = AllFieldTypes(decimal_field=1)

        m.decimal_field = 2

        self.assertEqual({"decimal_field": {"old": 1, "new": 2}}, m.get_changes())

    def test_change_email_field___has_changed_is_true(self):
        m = AllFieldTypes(email_field="foo@bar.com")

        m.email_field = "bar@foo.com"

        self.assertTrue(m.has_changed())

    def test_change_email_field___get_changes_has_the_change(self):
        m = AllFieldTypes(email_field="foo@bar.com")

        m.email_field = "bar@foo.com"

        self.assertEqual({"email_field": {"old": "foo@bar.com", "new": "bar@foo.com"}}, m.get_changes())

    def test_change_file_field___has_changed_is_true(self):
        test_file_dir = os.path.join(os.path.dirname(__file__), "test_files")

        m = AllFieldTypes()
        with open(os.path.join(test_file_dir, "first_file"), 'rb') as f:
            m.file_field.save("first_file", File(f), save=True)
        m.save()

        m = AllFieldTypes.objects.first()
        with open(os.path.join(test_file_dir, "second_file"), 'rb') as f:
            m.file_field.save("second_file", File(f), save=True)

        self.assertTrue(m.has_changed())

    def test_change_file_field___get_changes_has_the_change(self):
        test_file_dir = os.path.join(os.path.dirname(__file__), "test_files")

        m = AllFieldTypes()
        with open(os.path.join(test_file_dir, "first_file"), 'rb') as f:
            m.file_field.save("first_file", File(f), save=True)
        m.save()

        m = AllFieldTypes.objects.first()
        with open(os.path.join(test_file_dir, "second_file"), 'rb') as f:
            m.file_field.save("second_file", File(f), save=True)

        self.assertEqual({}, m.get_changes())
