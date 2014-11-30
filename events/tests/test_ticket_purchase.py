""" Test ticket purchasing. """

from django_bs_test import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestTicketPurchase(TestCase):

    """ Test ticket purchasing. """

    def setUp(self):
        """ Set up a common user. """
        self.user = mommy.make("auth.User")
        self.user.set_password("password")
        self.user.save()

    def test_purchase_requires_login(self):
        """ Test you need to be logged in to purchase tickets. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20))
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue("accounts/login" in response.redirect_chain[0][0])

    def test_past_event(self):
        """ Test that we can't buy tickets past the deadline. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20))
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % past_event.pk))

    def test_quantity(self):
        """ Test that the quantity box doesn't allow > remainging tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/events/%s/purchase_tickets" % event.pk)
        quantity = response.soup.find(id="id_quantity")
        highest_value = quantity.findAll("option")[-1]["value"]
        self.assertEquals("30", highest_value)

        event.buy_ticket(self.user, tickets=5)

        response = self.client.get("/events/%s/purchase_tickets" % event.pk)
        quantity = response.soup.find(id="id_quantity")
        highest_value = quantity.findAll("option")[-1]["value"]
        self.assertEquals("25", highest_value)

    def test_sold_out(self):
        """ Test that we can't buy tickets once they are sold out. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        event.buy_ticket(self.user, tickets=30)

        response = self.client.get("/events/%s/purchase_tickets" % event.pk,
                                   follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % event.pk))

    def test_purchase(self):
        """ Test that a purchase creates a ticket and redirects. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            "/events/%s/purchase_tickets" % event.pk,
            {"quantity": 5},
            follow=True)
        self.assertTrue(
            "events/tickets_purchased" in response.redirect_chain[0][0])
        self.assertEquals(self.user.tickets.first(),
                          response.context["ticket"])
        self.assertEquals(event.tickets.first(), response.context["ticket"])

    def test_cant_view_others_confirmation(self):
        """ Test that users can only view their own order confirmations. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)

        user2 = mommy.make("auth.User")
        user2.set_password("password")
        user2.save()

        ticket = event.buy_ticket(self.user, tickets=5)

        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEquals(200, response.status_code)

        self.client.login(username=user2.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEquals(404, response.status_code)