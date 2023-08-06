import json
import types
import unittest
from unittest.mock import patch, call

from heapapi import HeapAPIClient


class HeapAPIClientTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.client = HeapAPIClient(42)

    def test_init_missing_app_id(self):
        with self.assertRaises(AssertionError):
            HeapAPIClient(None)

    def test_init_ok(self):
        self.assertEqual(self.client.app_id, "42")

    @patch("requests.post")
    def test_track(self, request_post):
        resp = self.client.track("xxx", "Purchase")

        request_post.assert_called_with(
            "https://heapanalytics.com/api/track",
            data=json.dumps({"app_id": "42", "identity": "xxx", "event": "Purchase"}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(resp, request_post.return_value)
        resp.raise_for_status.assert_called_with()

    @patch("requests.post")
    def test_track_with_properties(self, request_post):
        resp = self.client.track("xxx", "Purchase", {"amount": 12, "currency": "USD"})

        request_post.assert_called_with(
            "https://heapanalytics.com/api/track",
            data=json.dumps(
                {
                    "app_id": "42",
                    "identity": "xxx",
                    "event": "Purchase",
                    "properties": {"amount": 12, "currency": "USD"},
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(resp, request_post.return_value)
        resp.raise_for_status.assert_called_with()

    @patch("requests.post")
    def test_add_user_properties(self, request_post):
        resp = self.client.add_user_properties("xxx", {"age": 22})

        request_post.assert_called_with(
            "https://heapanalytics.com/api/add_user_properties",
            data=json.dumps({"app_id": "42", "identity": "xxx", "properties": {"age": 22}}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(resp, request_post.return_value)
        resp.raise_for_status.assert_called_with()

    def test__get_bulks_empty(self):
        batches = self.client._get_bulks([])
        self.assertIsInstance(batches, types.GeneratorType)
        self.assertEqual(list(batches), [])

    def test__get_bulks_one_batch(self):
        objects = list(range(500))
        batches = self.client._get_bulks(objects)
        self.assertIsInstance(batches, types.GeneratorType)
        self.assertEqual(list(batches), [objects])

    def test__get_bulks_exactly_2_batches(self):
        objects = list(range(2000))
        batches = self.client._get_bulks(objects)
        self.assertIsInstance(batches, types.GeneratorType)
        self.assertEqual(list(batches), [list(range(1000)), list(range(1000, 2000))])

    @patch("requests.post")
    def test_bulk_track(self, request_post):
        events = [{"idx": idx} for idx in range(1001)]
        responses = self.client.bulk_track(events)
        self.assertEqual(responses, [request_post.return_value, request_post.return_value])
        request_post.assert_has_calls(
            [
                call(
                    self.client.track_api,
                    data=json.dumps(
                        {"app_id": "42", "events": [{"idx": idx} for idx in range(1000)]}
                    ),
                    headers={"Content-Type": "application/json"},
                ),
                call(
                    self.client.track_api,
                    data=json.dumps({"app_id": "42", "events": [{"idx": 1000}]}),
                    headers={"Content-Type": "application/json"},
                ),
            ]
        )

    @patch("requests.post")
    def test_bulk_add_user_properties(self, request_post):
        users = [{"idx": idx} for idx in range(1001)]
        responses = self.client.bulk_add_user_properties(users)
        self.assertEqual(responses, [request_post.return_value, request_post.return_value])
        request_post.assert_has_calls(
            [
                call(
                    self.client.props_api,
                    data=json.dumps(
                        {"app_id": "42", "users": [{"idx": idx} for idx in range(1000)]}
                    ),
                    headers={"Content-Type": "application/json"},
                ),
                call(
                    self.client.props_api,
                    data=json.dumps({"app_id": "42", "users": [{"idx": 1000}]}),
                    headers={"Content-Type": "application/json"},
                ),
            ]
        )
