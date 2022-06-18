from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

app_name = "stocks"


class StockMainView(TemplateView):

    template_name = "main_stocks.html"
