# https://www.youtube.com/watch?v=IGPUs49a1Zo

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool

def main():
    # https://coinmarketcap.com/all/views/all/
    try:
        start = datetime.now()
        url = 'https://coinmarketcap.com/all/views/all'
        all = get_html(url)
        all_link = get_all_links( all )

        for i in all_link:
            html = get_html(i)
            data = get_page_data(html)
            print(data)
        #with Pool(5) as p:
            #p.map(make_all, all_link)

    except:
        print("SUCCESS")
        end = datetime.now()
        total = end - start
        print(str(total))


def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find_all('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price')

    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com/' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    name = soup.find('h2', id="markets").text.strip("Cash Market Pairs (Adjusted)")
    data = {'name': name,
            'price': price}
    return data

#def make_all(url):
#    html = get_html(url)
#    data = get_page_data(html)
#    print(data)

if __name__ == '__main__':
    main()
