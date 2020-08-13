from json import load
import requests
import urllib3
from urllib.request import urlopen
import termtables as tt
from bs4 import BeautifulSoup as bs
from unidecode import unidecode


def check_internet():
    try:
        requests.get("http://sanjesh.org")
        return True
    except urllib3.URLError as err:
        return False


def check_ip_location():
    try:
        url = urlopen('http://ipinfo.io/json')
        data = load(url)
        if data['country'] == 'IR':
            return True
        else:
            print("Your Not in IRAN :)  ")
            return False
    except:
        pass


# def car_spider():
#     try:
#         if check_internet():
#
#             page = requests.get("https://bama.ir/price")
#             soup = bs(page.content, 'html.parser')
#             # print(soup.prettify())
#
#             prices = soup.find_all('small', class_='sefr-price')
#             models = soup.find_all('span', class_='sefr-model')
#             years = soup.findAll('small', class_="sefr-trim")
#
#             car_models = []
#             car_prices = []
#             car_years = []
#
#             for model in models:
#                 car_models.append(
#                     model.text.strip()
#                         .replace('\n', '')
#                         .replace(' \u200f ', '')
#                         .replace(')', '')
#                         .replace('(', ''))
#
#             for price in prices:
#                 car_prices.append(price.text.strip())
#
#             for year in years:
#                 car_years.append(year.text.strip())
#
#             total_info = (list(zip(car_years, car_prices, car_models)))
#
#             tbl_info = tt.to_string(
#                 total_info,
#                 header=["(1)", "(2)", "(3)"],
#                 style=tt.styles.ascii_thin_double,
#
#             )
#             print(tbl_info, '\n')
#
#     except:
#         print("\n   No internet connection :(")


def laptop_spider():
    try:
        if check_internet() and check_ip_location():

            page = requests.get("https://b2n.ir/386916")
            soup = bs(page.content, 'html.parser')

            prices = soup.find_all('div', class_="col-md-2 col-sm-12 col-12 item-price")
            models = soup.find_all('a', class_="maintitle")

            laptop_prices = []
            laptop_models = []

            for index, price in enumerate(prices):
                laptop_prices.append(price.find('span').text.strip())
                if index == 30:
                    break

            for index, model in enumerate(models):
                laptop_models.append(model.text.strip())
                if index == 30:
                    break

            total_info = list(zip(laptop_models, laptop_prices))

            tbl_info = tt.to_string(
                total_info,
                header=["   Title", "   Price "],
                style=tt.styles.ascii_thin_double,

            )
            print(tbl_info, '\n')
            return True
        else:
            print("hoora")

    except:
        print("\n   No internet connection :(")
        return False


def crypto_spider():
    try:
        if check_internet() and check_ip_location():
            page = requests.get("https://arzdigital.com/coins/")
            soup = bs(page.content, 'html.parser')

            titles = soup.find_all('tr', class_="arz-coin-tr arz-sort-value-row arz-fiat-parent")

            prices = soup.find_all('td', class_="arz-coin-table-rial-price-td arz-sort-value")

            crypto_prices = []

            crypto_titles = []

            for index, title in enumerate(titles):
                crypto_titles.append(title.find('a').text.strip())
                if index == 30:
                    break

            for index, price in enumerate(prices):
                tmp = unidecode(price.text)[:-4]
                crypto_prices.append(tmp)
                if index == 30:
                    break

            total_info = list(zip(crypto_titles, crypto_prices))

            tbl_info = tt.to_string(
                total_info,
                header=["   Title", "   Price (Toman)"],
                style=tt.styles.ascii_thin_double,

            )
            print(tbl_info, '\n')
            return True

    except:
        print("\n No internet connection  :(")
        return False
