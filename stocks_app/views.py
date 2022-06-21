from typing import Any, Dict

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from stocks_app.models import Stock

# Create your views here.


class Watchlist(ListView):
    model = Stock
    template_name: str = "stocks_app/stock_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["records"] = Stock.objects.filter(customuser__username=self.request.user)
        return context


class NotFoundView(TemplateView):
    template_name: str = "stocks_app/not_found.html"
