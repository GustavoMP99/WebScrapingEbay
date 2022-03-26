import os
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import csv


def get_page(url):
    response = requests.get(url)
    soup = None
    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_data_product(soup):
    try:
        name = soup.find('h1', {"class": "x-item-title__mainTitle"}).find('span', {
            'class': 'ux-textspans ux-textspans--BOLD'}).text
    except:
        name = ''
    try:
        state = soup.find('span', {'data-testid': 'ux-textual-display'}).find('span', {'class': "ux-textspans"}).text
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
    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', {'itemprop': 'url'})
    except:
        links = []
    url = [item.get('href') for item in links]

    return list(OrderedDict.fromkeys(url))


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
    url = 'https://www.ebay.com/globaldeals'
    # url1 = 'https://www.ebay.com/itm/194060416913?_trkparms=5373%3A0%7C5374%3AFeatured'
    # get_data_product(get_page(url1))
    products = get_index_data(get_page(url))
    if os.path.exists('data.csv') and os.path.isfile('data.csv'):
        os.remove('data.csv')
    else:
        print("file not found")
    for link in products:
        data = get_data_product(get_page(link))
        write_csv(data, link)


if __name__ == '__main__':
    main()
