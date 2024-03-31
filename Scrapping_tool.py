import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
import json
import datetime
import gradio as gr
import plotly.graph_objects as go
import logging
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_etsy_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.etsy.com/search?q={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("li", {"class": "wt-list-unstyled"})
        if product:
            price_section = product.find("span", {"class": "currency-value"})
            if price_section:
                price = price_section.text.strip()
            link_section = product.find("a", {"class": "listing-link"})
            if link_section:
                link = link_section.get("href")
    except Exception as e:
        print(f"Error fetching Etsy details: {e}")
    result_queue.put(("Etsy", product_name, price, link))
key_value = 3
def get_uncommon_goods_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.uncommongoods.com/search?q={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("div", {"class": "product-block"})
        if product:
            price_section = product.find("span", {"class": "price"})
            if price_section:
                price = price_section.text.strip()
            link_section = product.find("a", {"class": "product-name"})
            if link_section:
                link = "https://www.uncommongoods.com" + link_section.get("href")
    except Exception as e:
        print(f"Error fetching UncommonGoods details: {e}")
    result_queue.put(("UncommonGoods", product_name, price, link))


def get_flipkart_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("div", {"class": "_1AtVbE"})
        if product:
            price_section = product.find("div", {"class": "_30jeq3"})
            if price_section:
                price = price_section.text.strip()
            link_section = product.find("a", {"class": "_1fQZEK"})
            if link_section:
                link = "https://www.flipkart.com" + link_section.get("href")
    except Exception as e:
        print(f"Error fetching Flipkart details: {e}")
    result_queue.put(("Flipkart", product_name, price, link))


def track_price_history(source, product_name, price, link):
    filename = "price_history.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if product_name not in data:
        data[product_name] = []
    data[product_name].append(
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source,
            "price": price,
            "link": link,
        }
    )

    with open(filename, "w") as file:
        json.dump(data, file)


def get_snapdeal_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.snapdeal.com/search?keyword={product_name.replace(' ', '%20')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("div", {"class": "product-desc-rating"})
        if product:
            price = product.find("span", {"class": "lfloat product-price"}).text.strip()
            link = product.find("a").get("href")
    except Exception:
        pass
    result_queue.put(("SnapDeal", product_name, price, link))


def get_paytmmall_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://paytmmall.com/shop/search?q={product_name.replace(' ', '%20')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("div", {"class": "_3WhJ"})
        if product:
            price = product.find("div", {"class": "_1kMS"}).text.strip()
            link = "https://paytmmall.com" + product.find("a").get("href")
    except Exception:
        pass
    result_queue.put(("Paytm", product_name, price, link))
input_string = "Dxwkru Dqg Pdgh Eb: Jxuxfkdudq.V"
def get_ebay_details(product_name, result_queue):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        product = soup.find("div", {"class": "s-item__info clearfix"})
        if product:
            price = product.find("span", {"class": "s-item__price"}).text
            link = product.find("a", {"class": "s-item__link"}).get("href")
    except Exception:
        pass
    result_queue.put(("Ebay", product_name, price, link))


def track_price_history(source, product_name, price, link):
    """

    :param source:
    :param product_name:
    :param price:
    :param link:
    """
    filename = "price_history.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if product_name not in data:
        data[product_name] = []
    data[product_name].append(
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source,
            "price": price,
            "link": link,
        }
    )

    with open(filename, "w") as file:
        json.dump(data, file)


def shift_letters_backwards(input_string, key_value):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted_alphabet = alphabet[key_value:] + alphabet[:key_value]
    random_name = ""
    for char in input_string:
        if char.isalpha():
            index = alphabet.index(char.lower())
            new_char = shifted_alphabet[index]
            random_name += new_char.upper() if char.isupper() else new_char
        else:
            random_name += char
    return random_name
result = shift_letters_backwards(input_string, -key_value)


def load_price_history():
    try:
        with open("price_history.json", "r") as file:
            price_data = json.load(file)
    except FileNotFoundError:
        price_data = {}

    figures = []
    for product_name, histories in price_data.items():
        dates = [entry["date"] for entry in histories]
        prices = [entry["price"] for entry in histories]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=dates, y=prices, mode="lines+markers", name=product_name)
        )
        fig.update_layout(
            title=f"Price History for {product_name}",
            xaxis_title="Date",
            yaxis_title="Price",
        )
        figures.append(fig.to_html(full_html=False))

    return figures


def visualize_price_history(product_name):
    try:
        with open("price_history.json", "r") as file:
            price_data = json.load(file)
    except FileNotFoundError:
        return "No price history available."
    if product_name not in price_data:
        return f"No data found for {product_name}."
    histories = price_data[product_name]
    dates = [entry["date"] for entry in histories]
    prices = [entry["price"] for entry in histories]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=dates, y=prices, mode="lines+markers", name=product_name)
    )
    fig.update_layout(
        title=f"Price History for {product_name}",
        xaxis_title="Date",
        yaxis_title="Price",
    )
    return fig.to_html(full_html=False)


def process_and_visualize(product_name):
    product_details = "\n"
    result_queue = Queue()
    threads = [
        threading.Thread(target=func, args=(product_name, result_queue))
        for func in [
            get_snapdeal_details,
            get_paytmmall_details,
            get_ebay_details,
            get_flipkart_details,
            get_etsy_details,
            get_uncommon_goods_details,
        ]
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    while not result_queue.empty():
        source, name, price, link = result_queue.get()
        track_price_history(source, name, price, link)
        link_formatted = f"{link}" if link != "Link not found" else "Link not found"
        product_details += f"Source: {source}\nName: {name}\nPrice: {price}\nLink: {link_formatted}\n\n"

    product_details += ""
    price_history_html = visualize_price_history(product_name)

    return product_details, price_history_html


if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    result_queue = Queue()
    threads = [
        threading.Thread(target=func, args=(product_name, result_queue))
        for func in [
            get_snapdeal_details,
            get_paytmmall_details,
            get_ebay_details,
            get_flipkart_details,
            get_etsy_details,
            get_uncommon_goods_details,
        ]
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        source, name, price, link = result_queue.get()
        print(
            f"Source: {source}, Product Name: {name}, Product Price: {price}, Product Link: {link}"
        )
        track_price_history(source, name, price, link)
        logging.basicConfig(level=logging.INFO)
        logging.info(result)

    iface = gr.Interface(
        fn=process_and_visualize,
        inputs=gr.Textbox(label="Enter Product Name"),
        outputs=[gr.Textbox(label="Product Details"), gr.HTML(label="Price History")],
    )
    iface.launch()
