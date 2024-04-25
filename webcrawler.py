import requests
from bs4 import BeautifulSoup
import csv
base_url = 'https://www.digikala.com'
csv_file = 'laptops.csv'
headers = ['نام', 'قیمت']
def extract_laptop_info(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = soup.find('h1', class_='c-product__title').text.strip()
    price = soup.find('div', class_='c-product__seller-price-final').text.strip()
    
    return name, price
def scrape_laptops():
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for page_num in range(1, 3): 
            url = f'https://www.digikala.com/search/category-notebook/?pageno={page_num}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='c-product-box__content')

            for product in products:
                product_url = base_url + product.find('a')['href']
                name, price = extract_laptop_info(product_url)
                writer.writerow([name, price])
def create_comparison_table(laptop1, laptop2):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>مقایسه لپتاپ‌ها</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 50%;
                margin: auto;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h2>جدول مقایسه لپتاپ‌ها</h2>
        <table>
            <tr>
                <th>نام</th>
                <th>قیمت</th>
            </tr>
            <tr>
                <td>{laptop1[0]}</td>
                <td>{laptop1[1]}</td>
            </tr>
            <tr>
                <td>{laptop2[0]}</td>
                <td>{laptop2[1]}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    with open('comparison_table.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
scrape_laptops()
laptop1 = ['نام لپتاپ 1', 'قیمت لپتاپ 1']
laptop2 = ['نام لپتاپ 2', 'قیمت لپتاپ 2']
create_comparison_table(laptop1, laptop2)
