from audioop import add

from accounts.models import CustomUser
from django.contrib.auth import get_user
from django.test import RequestFactory, TestCase
from django.urls import reverse
from stocks_app.models import Stock

from .forms import StockEntryForm
from .views import HomePageView


class TestPages(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stock = Stock.objects.create(name="MANU")
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=27,
        )
        cls.factory = RequestFactory()

    def assertContainsAny(self, response, texts, status_code=200, msg_prefix="", html=False):

        total_count = 0
        for text in texts:
            text_repr, real_count, msg_prefix = self._assert_contains(response, text, status_code, msg_prefix, html)
            total_count += real_count

        self.assertTrue(total_count != 0)

    def test_home_page_get(self):
        response_get = self.client.get("/")
        response_reverse = self.client.get(reverse("pages:home"))

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed("pages/home.html")
        self.assertEqual(response_reverse.status_code, 200)
        self.assertContainsAny(response_get, ["Enter here", "Add to Watchlist", "Login"])

    def test_home_page_form(self):
        data = {"stock_abbreviation": "MANU", "add": True}
        form = StockEntryForm(data)

        self.assertTrue(form.is_valid())

    def test_home_page_post_no_user(self):
        response = self.client.post(reverse("pages:home"), {"stock_abbreviation": "MANU", "add": True})

        self.assertEqual(response.status_code, 200)  # no redirect, same page
        self.assertContains(response, "Manchester United")
        # no user - no option to add anything to the watchlist
        self.assertContains(response, "You have to log in in order to add stocks to the watchlist")

    def test_home_page_post_user_logged_in(self):
        self.client.login(username="testuser", password="admin")
        data = {"stock_abbreviation": "AMZN", "add": True}
        res = self.client.post(reverse("pages:home"), data)

        added_stock = Stock.objects.all().last()
        user_stock = Stock.objects.filter(customuser__username="testuser")[0].name

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "You have to log in in order to add stocks to the watchlist")
        self.assertEqual(added_stock.name, "AMZN")  # check if add: True triggered creation of stock in DB.
        self.assertEqual(user_stock, "AMZN")  # check if stock was linked with the logged in user.

    def test_home_page_post_wrong_data(self):
        response = self.client.post(reverse("pages:home"), {"stock_abbreviation": "MX1", "add": True})

        self.assertEqual(response.status_code, 302)

    def test_home_page_post_wrong_data_follow_html_content(self):
        response = self.client.post(reverse("pages:home"), {"stock_abbreviation": "MANU1", "add": True}, follow=True)

        self.assertTemplateUsed(response, "stocks_app/not_found.html")
        self.assertContains(response, "YAHOO")
