from accounts.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from stocks_app.models import Stock


class ApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stock = Stock.objects.create(name="MANU")
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=27,
        )
        cls.my_admin = CustomUser.objects.create_superuser(username="admin", password="adminadmin", age=27)
        cls.user.stock.add(cls.stock)
        # linking a stock with a user - user should show up on the stock api, stock on user

    def test_authentication_api_view(self):
        response = self.client.get(reverse("stock_list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # user has to be authenticated.

    def test_user_apis_not_admin(self):
        self.client.login(username="testuser", password="admin")
        response = self.client.get(reverse("users_list"))

        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # only admins are allowed to view user related APIs

    def test_stock_list_view_api(self):
        self.client.login(username="testuser", password="admin")
        response = self.client.get(reverse("stock_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.stock)
        self.assertContains(response, "testuser")
        # user who has stock MANU on the watchlist is visible on the api under "user"
        self.assertEqual(Stock.objects.count(), 1)

    def test_user_list_view_api(self):
        self.client.login(username="admin", password="adminadmin")  # only admins are allowed to view user related APIs

        response = self.client.get(reverse("users_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user)
        self.assertContains(response, "MANU")  # MANU stock is visible on the users api in "Stock"
        self.assertEqual(CustomUser.objects.get(username="testuser").username, "testuser")

    def test_user_detail_view_api(self):
        self.client.login(username="admin", password="adminadmin")  # only admins are allowed to view user related APIs
        response = self.client.get(reverse("user_detail", args=[1]))  #  kwargs={"pk": self.user.id}))
        response_user_not_exist = self.client.get(
            reverse("user_detail", args=[3])
        )  # only two users - this should yield 404.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user_not_exist.status_code, status.HTTP_404_NOT_FOUND)
