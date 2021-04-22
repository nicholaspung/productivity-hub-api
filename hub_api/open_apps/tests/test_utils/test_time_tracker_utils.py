from django.test import TestCase
from open_apps.utils import time_tracker_utils


class FakeClass():
    hi = 'hi'
    query_params = {}


class SampleTestCase(TestCase):
    def test_get_archived_time_tracker_name_items(self):
        sample_request = FakeClass()
        self.assertEqual(
            time_tracker_utils.get_archived_time_tracker_name_items(sample_request), False)
        sample_request.query_params['archived'] = True
        self.assertEqual(
            time_tracker_utils.get_archived_time_tracker_name_items(sample_request), True)
