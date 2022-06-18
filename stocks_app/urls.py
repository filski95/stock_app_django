from django.urls import path

from . import views

urlpatterns = [path("", views.StockMainView.as_view(), name="stocks_main")]
