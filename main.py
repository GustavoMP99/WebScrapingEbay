import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import csv
from datetime import datetime
import psycopg2

def post_db(url, products):
    mydb = psycopg2.connect(user='jnhtfcjqoslawm', password='cecd94fc0872c4bc82b837bde8eedcd3c990e7f50644ccc0d495bbd77954e526', host='ec2-44-196-174-238.compute-1.amazonaws.com', database='dfhhdtj8ujfucj', port=5432)

    mycursor = mydb.cursor()

    sql = "INSERT INTO auditoria (fecha, pagina_web, numero_registros,estado,errores) VALUES (%s, %s, %s, %s, %s)"
    val = (datetime.today(), url, products, 0, "")
    mycursor.execute(sql, val)
    mydb.commit()


# Function to get a request from a string
def get_page(url):
    response = requests.get(url)
    soup = None
    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


# Function to get the data(name, state, description, ...) from a product
def get_data_product(soup):
    mydb = psycopg2.connect(user='jnhtfcjqoslawm',
                            password='cecd94fc0872c4bc82b837bde8eedcd3c990e7f50644ccc0d495bbd77954e526',
                            host='ec2-44-196-174-238.compute-1.amazonaws.com', database='dfhhdtj8ujfucj', port=5432)

    mycursor = mydb.cursor()
    try:
        name = soup.find('h1', {"class": "x-item-title__mainTitle"}).find('span', {
            'class': 'ux-textspans ux-textspans--BOLD'}).text
    except:
        name = ''
    try:
        state = soup.find('span', {'data-testid': 'spa'}).find('span', {'class': "ux-textspans"}).text
    except:
        state = ''
    try:
        description = soup.find('div', {'class': 'd-item-condition-desc'}).find('span', {
            'class': "ux-textspans ux-textspans--ITALIC"}).text
    except:
        description = ''
    try:
        price = soup.find('span', {'id': 'prcIsum'}).text
    except:
        price = ''
    try:
        cant = soup.find('span', {'id': 'qtySubTxt'}).text.strip()
    except:
        cant = ''
    try:
        sell_n = soup.find('span', {'class': 'w2b-sgl'}).text
    except:
        sell_n = ''
    try:
        seller = soup.find('div', {'data-testid': 'x-about-this-seller'}).find('a', {'data-testid': 'ux-action'}).text
    except:
        seller = ''
    try:
        seller_stars = \
            soup.find('div', {'data-testid': 'x-about-this-seller'}).find_all('a', {'data-testid': 'ux-action'})[1].text
    except:
        seller_stars = ''
    try:
        seller_quality = \
            soup.find('div', {'data-testid': 'x-about-this-seller'}).find_all('div',
                                                                              {'class': 'ux-seller-section__item'})[
                1].text
    except:
        seller_quality = ''
    try:
        day_back = soup.find('div', {'id': 'why2buy'}).find_all('span', {'class': 'w2b-sgl'})[1].text
    except:
        day_back = ''
    try:
        mark_as_favorite = soup.find('div', {'id': 'why2buy'}).find_all('span', {'class': 'w2b-sgl'})[2].text
    except:
        mark_as_favorite = ''
    try:
        shipping_cost = soup.find('span', {'id': 'fshippingCost'}).find('span').text
    except:
        shipping_cost = ''
    try:
        shipping_day = soup.find('span', {'class': 'vi-acc-del-range'}).text
    except:
        shipping_day = ''
    try:
        id_product_ebay = soup.find('div', {'id': 'descItemNumber'}).text
    except:
        id_product_ebay = ''
    try:
        image = soup.find('img', {'id': 'icImg'})['src']
    except:
        image = ''
    data = {
        'name': name,
        'state': state,
        'description': description,
        'price': price,
        'cant': cant,
        'sell_n': sell_n,
        'seller': seller,
        'seller_stars': seller_stars,
        'seller_quality': seller_quality,
        'day_back': day_back,
        'mark_as_favorite': mark_as_favorite,
        'shipping_cost': shipping_cost,
        'shipping_day': shipping_day,
        'id_product_ebay': id_product_ebay,
        'image': image
    }
    sql = "INSERT INTO registro (name, state, description,price,cant,sell_n,seller,seller_stars, seller_quality,day_back,mark_as_favorite,shipping_cost,shipping_day,id_product_ebay, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, state, description,price,cant,sell_n,seller,seller_stars, seller_quality,day_back,mark_as_favorite,shipping_cost,shipping_day,id_product_ebay, image)
    mycursor.execute(sql, val)
    mydb.commit()
    return data

# Function that allow to find links to other pages and save it to a list
def get_index_data(soup):
    try:
        links = soup.find_all('a', {'itemprop': 'url'})
    except:
        links = []
    url = [item.get('href') for item in links]

    return list(OrderedDict.fromkeys(url))


# Function that creates and add the data of the products in a csv
def write_csv(data, url):
    with open('data.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        row = [
            data['name'],
            data['state'],
            data['description'],
            data['price'],
            data['cant'],
            data['sell_n'],
            data['seller'],
            data['seller_stars'],
            data['seller_quality'],
            data['day_back'],
            data['mark_as_favorite'],
            data['shipping_cost'],
            data['shipping_day'],
            data['id_product_ebay'],
            data['image'], url
        ]
        writer.writerow(row)

def main():
    url = 'https://www.ebay.com/globaldeals'  # Url of the offers in eBay
    products = get_index_data(get_page(url))  # List of the Urls of different products
    post_db(url, len(products))
    for link in products:
        get_data_product(get_page(link))

    #Code to import in a CSV
    #if os.path.exists('data.csv') and os.path.isfile('data.csv'):  # IF that delete the csv in case this exist
    #    os.remove('data.csv')
    #else:
    #    print("file not found")
    #for link in products:
    #    data = get_data_product(get_page(link))
    #write_csv(data, link)


if __name__ == '__main__':
    main()
