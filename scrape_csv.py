import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://books.toscrape.com/catalogue/category/books_1/index.html"

def scrap_book(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    book_list = []
    for book in books:
        title = book.h3.a['title']
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        book_list.append({
            "title": title,
            "price": price,
            "currency": currency
        })

    # Save as JSON
    with open("books.json", "w", encoding="utf-8") as f_json:
        json.dump(book_list, f_json, indent=4, ensure_ascii=False)

    # Save as CSV
    with open("books.csv", "w", encoding="utf-8", newline='') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=["title", "price", "currency"])
        writer.writeheader()
        for book in book_list:
            writer.writerow(book)

    print("Books saved as books.json and books.csv")

scrap_book(url)
