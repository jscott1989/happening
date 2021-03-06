"""Test event view."""

from happening.tests import TestCase
# from model_mommy import mommy
# from datetime import datetime, timedelta
# import pytz


class TestEventView(TestCase):

    """Test Event View."""

    def test_nonexisting_event(self):
        """Test view for event which doesn't exist."""
        response = self.client.get("/events/1")
        self.assertEqual(response.status_code, 404)

    def test_future_event(self):
        """Test view for an event in the future."""
        pass

    def test_past_event(self):
        """Test view for an event in the past."""
        pass
