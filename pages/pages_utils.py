import re
from collections import namedtuple

import requests  # type:ignore
from bs4 import BeautifulSoup

# defaults added in case some stock html is different than assumed "characteristics" assumed during soup creation.
# names of attributes visible under output.attribute_name in html templates
BasicStockInfo = namedtuple(
    "BasicStockInfo",
    "price price_change change_percent currency name",
    defaults=(
        "Not Found",
        "Not Found",
        "Not Found",
        "Not Found",
        "Not Found",
    ),
)


def get_requested_stock_basic_data(stock):
    """
    Method scrapping Yahoo fianncial tab.
    Deployment of simple soup (bs4) and scrapping price, price change, % change, currency, name.
    returns namedtupple with all elements as strings.
    """

    url_financials = f"https://finance.yahoo.com/quote/{stock}/financials?p={stock}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    }

    # send request to Yahoo
    response = requests.get(url_financials, headers=headers)
    soup = BeautifulSoup(markup=response.text, features="html.parser")

    price = soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    price_change = soup.find("fin-streamer", {"class": "Fw(500) Pstart(8px) Fz(24px)"}).text
    change_percent = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")[2].text

    # getting currency and name in one go as they are in the same element on the page.
    currency_name = soup.find(
        "div",
        {
            "class": "D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)"
        },
    ).text

    currency = (re.search(r"USD", currency_name)).group()
    name_ending = currency_name.find("(") - 1  # full name, then bracket (ABBREVIATION) then rest
    name = currency_name[:name_ending]

    StockInfo = BasicStockInfo(price, price_change, change_percent, currency, name)
    # NamedTuple
    return StockInfo
