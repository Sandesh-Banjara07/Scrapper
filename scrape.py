
import requests
from bs4 import BeautifulSoup
import json

url = "https://books.toscrape.com/catalogue/category/books_1/index.html"

def scrap_book(url):
    response = requests.get(url)

    #set encoding explicitely to handle special characters correcrtly
    response.encoding = response.apparent_encoding 
    



    if response.status_code != 200:
        return
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        book_list = []
        for book in books:
            title = book.h3.a['title']
            print(title)
            price_text = book.find("p", class_="price_color").text
            currency = price_text[0]
            price = float(price_text[1:])
            print(title, currency, price)

            book_list.append(
                {"title": title,
                 "price": price,
                 "currency": currency}
            )
        with open("books.json", "w", encoding ="utf-8") as f:
            

            json.dump(book_list, f, indent = 4, ensure_ascii=False)



scrap_book(url)

