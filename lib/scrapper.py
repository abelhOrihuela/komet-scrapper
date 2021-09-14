from bs4 import BeautifulSoup
import requests
from lib.bot import send_item

URL = "https://www.tiendakomet.com"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
from models.item import ItemModel


def get_links(context):
    pages = []

    for nav in context.find_all("a", class_="nav-bar__link link"):
        pages.append(URL + nav["href"])
        pages.append(URL + nav["href"] + "?page=2")
    for sub_nav in context.find_all("a", class_="nav-dropdown__link link"):
        pages.append(URL + sub_nav["href"])
        pages.append(URL + sub_nav["href"] + "?page=2")

    return pages


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for item in soup.find_all("div", class_="product-item"):
        validate_item(item)


def validate_item(item):

    if item.find("span", class_="product-item__inventory"):
        data_item = {
            "link": URL + item.find("a")["href"],
            "description": item.find(
                "a", class_="product-item__title text--strong link"
            ).text,
            "inventory": item.find(
                "span", class_="product-item__inventory"
            ).text,
            "image": item.find("img", class_="product-item__primary-image")[
                "src"
            ].replace("_60x.png", "_600x.png"),
        }

        exist = ItemModel.find_by_slug(data_item["link"])

        if exist:
            if data_item["inventory"] != exist.inventory:
                exist.inventory = data_item["inventory"]
                send_item(data_item)
                exist.save_to_db()

        else:
            send_item(data_item)
            ItemModel(
                description=data_item["description"],
                slug=data_item["link"],
                inventory=data_item["inventory"],
            ).save_to_db()


def main():
    links = get_links(soup)
    for link in links:
        get_content(link)
