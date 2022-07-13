import base64
import concurrent.futures
import datetime
import io
import urllib
from typing import Any, Dict, List, Union

import matplotlib
import matplotlib.pyplot as plt
import requests_cache
import yfinance as yf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from pages import pages_utils
from pandas_datareader import data

from stocks_app.models import Stock

from .forms import RemoveStockWatchlist


class Watchlist(LoginRequiredMixin, ListView):
    model = Stock
    template_name: str = "stocks_app/stock_list.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["remove_form"].is_valid():
            instance = context["remove_form"].cleaned_data
            removed_stock = instance["remove_stock_from_your_watchlist"]

            try:
                user = request.user
                removed_stock = Stock.objects.get(name=removed_stock)
                user.stock.remove(removed_stock)
            except ObjectDoesNotExist:
                context["error_msg"] = f"Such stock ({removed_stock}) does not exist"

        return render(request, "stocks_app/stock_list.html", context=context)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        self.object_list = super().get_queryset()  # otherwise error object has no attribute 'object_list'
        context = super().get_context_data(**kwargs)
        user_stocks = Stock.objects.filter(user=self.request.user)

        context = self.prepare_watchlist_context(context, user_stocks)

        # additional feature added to the context
        remove_from_wl_form = RemoveStockWatchlist(self.request.POST or None)
        context["remove_form"] = remove_from_wl_form

        return context

    def prepare_watchlist_context(
        self,
        context: Dict[str, Any],  # Union[str, Dict[Union[str, None], Union[pages_utils.BasicStockInfo, str, None]]]
        user_stocks: List[Stock],
    ):
        """
        Function preparing context for watchlist. To improve process time it uses threading.

        it takes pre-prepared context and list of stocks added by the user to his watchlist in form of stocks'abbreviations:
        "MANU", "AMZN" etc.

        Abbreviations are later used as key values and are rendered on the HTML template along the stock name.
        """
        context["output"] = {}

        #! without threading
        # for stock in user_stocks:
        #     stock_info = pages_utils.get_requested_stock_basic_data(stock.name)
        #     context["output"][stock.name] = stock_info
        #     print(stock.name)

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:

            stocks = {
                stock: executor.submit(pages_utils.get_requested_stock_basic_data, stock.name) for stock in user_stocks
            }

            # stocks = STOCK : FUTURE(BasicStockInfo)
            for stock_obj, stock_future in stocks.items():
                stock_details = stock_future.result(timeout=10)

                context["output"][stock_obj] = stock_details

        context["price_header"] = "Price"
        context["price_change_header"] = "Price Change"
        context["percent_change_header"] = "DtD Percent Change"
        context["stock_name_header"] = "Stock"

        return context


class NotFoundView(TemplateView):
    template_name: str = "stocks_app/not_found.html"


class StockDetailView(DetailView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = Stock.objects.get(pk=self.kwargs.get("pk"))

        context["stock"] = self.prepare_figure(stock)
        context["detailed_info"] = self.prepare_detailed_stock_info(stock)
        return context

    def prepare_figure(self, stock):
        matplotlib.use("Agg")

        st = data.DataReader(stock.name, start="2017-1-1", end=datetime.date.today(), data_source="yahoo")["Adj Close"]

        st = st.plot(title=f"{stock} Closing price")
        figure = plt.gcf()
        figure.set_size_inches(6, 3)
        figure.legend(
            [stock.name], loc="upper left", bbox_to_anchor=(0.115, 0.90)
        )  # place the label in the top left corner

        buf = io.BytesIO()
        figure.savefig(buf, format="png", transparent=True, quality=100, dpi=200)
        buf.seek(0)

        figure.clear()  # clear the graph after it was saved as byte obj. Without this line, stocks will get 'stacked up' across views
        # / treated as one graph in session?

        imsrc = base64.b64encode(buf.read())
        imuri = "data:image/png;base64,{}".format(urllib.parse.quote(imsrc))
        return imuri

    def prepare_detailed_stock_info(self, stock):
        """
        using yfinance lib instead of webscrapping specific contents -> lots of features out of the box.
        seesions created to speed up loading time.
        """
        session = requests_cache.CachedSession("yfinance.cache")
        session.headers[
            "User-agent"
        ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

        stock_ticker = yf.Ticker(stock.name, session=session)

        return stock_ticker.info["longBusinessSummary"]
