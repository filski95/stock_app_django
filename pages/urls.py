from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("watchlist/", views.Watchlist.as_view(), name="watchlist"),
    path("notfound/", views.NotFoundView.as_view(), name="notfound"),
]
