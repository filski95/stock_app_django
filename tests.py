import re

import requests  # type:ignore
from bs4 import BeautifulSoup

stock = "MANU"

url_summary = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
url_profile = f"https://finance.yahoo.com/quote/{stock}/profile?p={stock}"
url_financials = f"https://finance.yahoo.com/quote/{stock}/financials?p={stock}"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
}

response = requests.get(url_financials, headers=headers)
# print(response.text)

soup = BeautifulSoup(markup=response.text, features="html.parser")

price = soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
change = soup.find("fin-streamer", {"class": "Fw(500) Pstart(8px) Fz(24px)"}).text
# print(price)
# print(change)

# currency = soup.find("div", {"class": "C($tertiaryColor) Fz(12px)"})
# change_percent = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")[2].text

# print(change_percent)
# x = (re.search(r"USD", currency.text)).group()  # type:ignore
# print(x)  # type:ignore

# print(currency.text)
# pattern = re.compile(r"\s--\sData\s--\s")
# script_data = soup.find("script", text=pattern)
# script_data = soup.find("script", text=pattern).contents[0]

name = soup.find(
    "div",
    {"class": "D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)"},
)

print(name.text)
x = name.text.find("(") - 1
print(name.text[:x])
