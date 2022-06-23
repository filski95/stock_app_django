from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from stocks_app.models import Stock

from accounts.admin_utils import Trie
from accounts.forms import CustomUserCreationForm

from . import views
from .models import CustomUser


class TestAccounts(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=27,
        )

        cls.stock = Stock.objects.create(name="MANU")

        cls.factory = RequestFactory()

    def test_signup_view(self):
        response = self.client.get("/accounts/signup/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("accounts/customuser_form.html")
        self.assertContains(response, "Required. 150 characters or fewer")

    def test_signup_form(self):
        data = {
            "username": "testtest",
            "age": 35,
            "password1": "xasdloasd[p123lol123",
            "password2": "xasdloasd[p123lol123",
            "First name": "testname",
            "Last name": "testlastname",
            "Email address": "myasd@gmail.com",
            "background": "IT",
        }

        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_signup_form_filled(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "testtest",
                "age": 35,
                "password1": "xasdloasd[p123lol123",
                "password2": "xasdloasd[p123lol123",
                "First name": "testname",
                "Last name": "testlastname",
                "Email address": "myasd@gmail.com",
                "background": "IT",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.all().last().username, "testtest")

    def test_login_user(self):
        response = self.client.post(
            ("/accounts/login/"),
            {
                "username": "testuser",
                "password": "admin",
            },
        )

        self.assertEqual(response.status_code, 302)  # 302 cuz of redirect

    def test_trie_stock(self):
        response = self.client.get("/accounts/trie/")
        request = self.factory.get("/accounts/trie/")

        t = Trie()
        views.add_trie_stock(request)
        all_stocks = t.collect_all_words()

        suggestion = t.alternatives("M")
        no_suggestion = t.alternatives("X")

        self.assertEqual(no_suggestion, None)  # check that suggestion system does not yield senseless suggestions
        self.assertEqual(suggestion, ["MANU"])  # check if sugestion system works
        self.assertEqual(all_stocks, ["MANU"])  # check if stocks from DB are correctly being added to the app Trie.
        self.assertEqual(response.status_code, 302)
