from django.urls import path

from . import views

app_name = "stocks"

urlpatterns = [
    path("watchlist/", views.Watchlist.as_view(), name="watchlist"),
    path("notfound/", views.NotFoundView.as_view(), name="notfound"),
    path("stock/<int:pk>/", views.StockDetailView.as_view(), name="stock_detail"),
]
