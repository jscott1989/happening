""" Test sponsorship page. """

from django_bs_test import TestCase


class TestIndex(TestCase):

    """ Test sponsorship page. """

    def test_sponsorship(self):
        """ Test it renders. """
        response = self.client.get("/sponsorship")
        self.assertEqual(200, response.status_code)
