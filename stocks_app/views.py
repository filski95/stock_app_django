import concurrent.futures
from typing import Any, Dict, List, Union

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from pages import pages_utils

from stocks_app.models import Stock

# Create your views here.


class Watchlist(ListView):
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
                stock.name: executor.submit(pages_utils.get_requested_stock_basic_data, stock.name)
                for stock in user_stocks
            }

            # stocks = MANU : FUTURE(BasicStockInfo)
            for abbrev, stock_future in stocks.items():
                stock_details = stock_future.result(timeout=5)
                st_name = abbrev
                context["output"][st_name] = stock_details

        context["price_header"] = "Price"
        context["price_change_header"] = "Price Change"
        context["percent_change_header"] = "DtD Percent Change"
        context["stock_name_header"] = "Stock"

        return context


class NotFoundView(TemplateView):
    template_name: str = "stocks_app/not_found.html"
