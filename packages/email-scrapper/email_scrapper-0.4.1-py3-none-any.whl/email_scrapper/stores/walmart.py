import datetime
import re

from bs4 import BeautifulSoup

from email_scrapper.models import Order, Stores, Item


def parse_walmart_email(email):
    email = str(email)
    soup = BeautifulSoup(email, "lxml")
    order_items = soup.find_all("table", {"cellpadding": "5", "cellspacing": "0"})[0].find_all("tr", {"valign": "top"})[
                  1:]
    date = datetime.datetime.strptime(soup.find_all("orderdate")[0].text, "%B %d, %Y")
    order_number = soup.find_all("ordernumber")[0].text
    cart = []
    for item in order_items:
        name = item.select("itemname")[0].text
        quantity = float(item.select("quantity")[0].text)
        unit_price = float(item.select("price")[0].text[1:])
        cart.append(Item(name, unit_price, int(quantity), order_number))
    order = Order(order_number, date, Stores.WALMART, cart)
    return order
