from accounts.models import CustomUser
from django.db import IntegrityError
from django.test import TestCase

from stocks_app.models import Stock


class TestStocksApp(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=27,
        )
        cls.stock = Stock.objects.create(name="MANU")

    def assertContainsAny(self, response, texts, status_code=200, msg_prefix="", html=False):

        total_count = 0
        for text in texts:
            text_repr, real_count, msg_prefix = self._assert_contains(response, text, status_code, msg_prefix, html)
            total_count += real_count

        self.assertTrue(total_count != 0)

    def test_watchlist_view_user_logged_out(self):
        response = self.client.get("/stocks/watchlist/")

        self.assertEqual(response.status_code, 302)  # redirect to login view.

    def test_watchlist_view_user_logged_in(self):
        self.user.stock.add(self.stock)  # add stock from setUpTestData to the cls.user
        new_stock = Stock.objects.create(name="AMZN")  # create new stock
        self.user.stock.add(new_stock)  # add the new stock

        self.client.login(username="testuser", password="admin")  # login the user with 2 stocks
        response = self.client.get("/stocks/watchlist/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks_app/stock_list.html")
        self.assertContainsAny(response, ["MANU", "AMZN", "testuser logged in", "Logout"])
        self.assertNotContains(response, "APPLE")

    def test_stock_model(self):

        with self.assertRaises(IntegrityError):
            new_stock = Stock.objects.create(name="MANU")  # unique constraint - dupplicate names not allowed
