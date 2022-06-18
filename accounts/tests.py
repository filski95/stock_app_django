from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import CustomUserCreationForm

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
        logged_in_user = get_user_model().objects.filter(username="testuser")

        # 302 cuz of redirect
        self.assertEqual(response.status_code, 302)
        # converting to string to compare it literally
        self.assertEqual(str(*logged_in_user), "testuser")
        self.assertNotEqual(str(*logged_in_user), "testuser2")
