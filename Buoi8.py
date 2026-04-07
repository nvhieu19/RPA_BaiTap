from bs4 import BeautifulSoup
import requests
import pandas as pd

data_books = []

# 5 trang
for page in range(1, 6):
    if page == 1:
        url = "http://books.toscrape.com/index.html"
    else:
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("article", class_="product_pod")

    for item in products:
        # name
        name = item.h3.a["title"]

        # price
        price = item.find("p", class_="price_color").text

        # rating
        rating = item.find("p", class_="star-rating")["class"][1]

        # availability
        availability_text = item.find("p", class_="instock availability").text.strip()

        if "In stock" in availability_text:
            availability = "In stock"
        else:
            availability = "Out of stock"

        data_books.append({
            "Name": name,
            "Price": price,
            "Rating": rating, 
            "Availability": availability
        })

# Tạo DataFrame
df = pd.DataFrame(data_books)

# Xuất Excel
df.to_excel("books.xlsx", sheet_name="Danh sách Sách", index=False)

print("đã lưu file books.xlsx")