import base64
import concurrent.futures
import datetime
import io
import urllib
from typing import Any, Dict, List, Union

import matplotlib
import matplotlib.pyplot as plt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from pages import pages_utils
from pandas_datareader import data

from stocks_app.models import Stock


class Watchlist(LoginRequiredMixin, ListView):
    model = Stock
    template_name: str = "stocks_app/stock_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_stocks = Stock.objects.filter(customuser__username=self.request.user)

        context = self.prepare_context(context, user_stocks)

        return context

    def prepare_context(
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
