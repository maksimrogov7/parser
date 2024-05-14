import requests
import re
import csv
import models
from datetime import datetime


class Parser:
    def __init__(self, url: str):
        self.item_id = self.__get_item_id(url)
        self.item_root = self.__get_item_root(self.item_id)

    @staticmethod
    def __get_item_id(url: str):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id

    def __get_item_root(self, item_id):
        response = requests.get(
            f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=29&nm={self.item_id}')

        item_root = models.Items.model_validate(response.json()['data'])
        return item_root.products[0].root

    def parse(self):
        self.__create_csv()
        response = requests.get(
            f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=29&nm={self.item_id}')
        items_info = models.Items.model_validate(response.json()['data'])
        self.__save_csv(items_info)

    def parse_price(self):
        self.__create_csv1()
        try:
            for q in range(20):
                if q < 10:
                    b = '0'
                else:
                    b = ''
                try:
                    response = requests.get(
                        f'https://basket-{b}{q}.wb.ru/vol{self.item_id[:len(self.item_id)-5:]}/part{self.item_id[:len(self.item_id)-3:]}/{self.item_id}/info/price-history.json')
                    with open('dataPrice.csv', mode='a', newline='',encoding="utf-8") as file:
                        writer = csv.writer(file)
                        for i in range(len(response.json())):
                            writer.writerow([datetime.utcfromtimestamp(response.json()[i]['dt']).strftime('%Y-%m-%d'), response.json()[i]['price']['RUB']/100])
                        break
                except Exception:
                    pass

        except Exception:
            pass

    def __create_csv(self):
        with open('data.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id','name','price','brand', 'supplier', 'discount','rating','amount', 'feedbacks'])

    def __save_csv(self,items):
        with open('data.csv', mode='a', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id, product.name, product.salePriceU/100, product.brand, product.supplier, product.sale, product.rating, product.volume, product.feedbacks])

    def __create_csv1(self):
        with open('dataPrice.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'price'])


if __name__ == "__main__":
    Parser('https://www.wildberries.ru/catalog/150972149/detail.aspx').parse()
    Parser('https://www.wildberries.ru/catalog/150972149/detail.aspx').parse_price()