import requests
import re
import csv
import models
import statistics


class ParserBrand:
    def __init__(self, url: str):
        self.brand_name = self.__get_brand_name(url)
        self.brand_id = self.__get_brand_id(self.brand_name)

    @staticmethod
    def __get_brand_name(url: str):
        regex = "(?<=brands/).+"
        brand_name = re.search(regex, url)[0]
        return brand_name

    def __get_brand_id(self, brand_name):
        response = requests.get(f'https://static-basket-01.wb.ru/vol0/data/brands/{self.brand_name}.json')
        brand_id = (response.json()['id'])
        return brand_id

    def parse(self):
        i= 1
        self.__create_csv()
        while True:
            try:
                params = {
                    'TestGroup': 'no_test',
                    'TestID': 'no_test',
                    'appType': '1',
                    'brand': self.brand_id,
                    'curr': 'rub',
                    'dest': '-1257786',
                    'page': i,
                    'sort': 'popular',
                    'spp': '29',
                }

                response = requests.get('https://catalog.wb.ru/brands/m/catalog', params=params)
                items_info = models.Items.model_validate(response.json()['data'])
                i+=1
                if not items_info.products:
                    break
                self.__save_csv(items_info)
            except Exception:
                break

        with open("data.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = 0
            price = []
            discount = []
            rating = []
            amount = []
            feedbacks = []
            for row in file_reader:
                if count != 0:
                    price.append(float(row[2]))
                    discount.append(float(row[5]))
                    rating.append(float(row[6]))
                    amount.append(float(row[7]))
                    feedbacks.append(float(row[8]))
                count += 1
            print(round(sum(price) / len(price), 2))
        with open('statistics.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([' ', 'price', 'discount', 'rating', 'amount', 'feedbacks'])
            writer.writerow(['Среднее', (round(sum(price) / len(price), 2)), (round(sum(discount) / len(discount), 2)),
                             (round(sum(rating) / len(rating), 2)),
                             (round(sum(amount) / len(amount), 2)), (round(sum(feedbacks) / len(feedbacks), 2))])
            writer.writerow(
                ['Медиана', statistics.median(price), statistics.median(discount), statistics.median(rating),
                 statistics.median(amount), statistics.median(feedbacks)])
            writer.writerow(['Мода', statistics.mode(price), statistics.mode(discount), statistics.mode(rating),
                             statistics.mode(amount), statistics.mode(feedbacks)])
            writer.writerow(
                ['Дисперсия', round(statistics.pvariance(price), 3), round(statistics.pvariance(discount), 3),
                 round(statistics.pvariance(rating), 3),
                 round(statistics.pvariance(amount), 3), round(statistics.pvariance(feedbacks), 3)])
            writer.writerow(
                ['Стандартное отклонение', round(statistics.pstdev(price), 3), round(statistics.pstdev(discount), 3),
                 round(statistics.pstdev(rating), 3),
                 round(statistics.pstdev(amount), 3), round(statistics.pstdev(feedbacks), 3)])

    def __create_csv(self):
        with open('data.csv', mode='w', newline='', encoding="utf-8", errors='strict') as file:
            writer = csv.writer(file)
            writer.writerow(['id','name','price','brand', 'supplier', 'discount','rating','amount', 'feedbacks','url'])

    def __save_csv(self,items):
        with open('data.csv', mode='a', newline='',encoding="utf-8", errors='strict') as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id, product.name, product.salePriceU/100, product.brand,
                                 product.supplier, product.sale, product.rating, product.volume, product.feedbacks,
                                 f'https://www.wildberries.ru/catalog/{product.id}/detail.aspx'])


class ParserSeller:
    def __init__(self, url: str):
        self.seller_id = self.__get_seller_id(url)

    @staticmethod
    def __get_seller_id(url: str):
        regex = '(?<=seller/).+'
        seller_id = re.search(regex, url)[0]

        return seller_id

    def parse(self):
        i= 1
        self.__create_csv()
        while True:
            try:
                params = {
                    'TestGroup': 'no_test',
                    'TestID': 'no_test',
                    'appType': '1',
                    'curr': 'rub',
                    'dest': '-1257786',
                    'page': i,
                    'sort': 'popular',
                    'spp': '29',
                    'supplier': self.seller_id,
                }

                response = requests.get('https://catalog.wb.ru/sellers/catalog', params=params)
                items_info = models.Items.model_validate(response.json()['data'])
                i+=1
                if not items_info.products:
                    break
                self.__save_csv(items_info)
            except Exception:
                break

        with open("data.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = 0
            price = []
            discount = []
            rating = []
            amount = []
            feedbacks = []
            for row in file_reader:
                if count != 0:
                    price.append(float(row[2]))
                    discount.append(float(row[5]))
                    rating.append(float(row[6]))
                    amount.append(float(row[7]))
                    feedbacks.append(float(row[8]))
                count += 1
            print(round(sum(price) / len(price), 2))
        with open('statistics.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([' ', 'price', 'discount', 'rating', 'amount', 'feedbacks'])
            writer.writerow(['Среднее', (round(sum(price) / len(price), 2)), (round(sum(discount) / len(discount), 2)),
                             (round(sum(rating) / len(rating), 2)),
                             (round(sum(amount) / len(amount), 2)), (round(sum(feedbacks) / len(feedbacks), 2))])
            writer.writerow(
                ['Медиана', statistics.median(price), statistics.median(discount), statistics.median(rating),
                 statistics.median(amount), statistics.median(feedbacks)])
            writer.writerow(['Мода', statistics.mode(price), statistics.mode(discount), statistics.mode(rating),
                             statistics.mode(amount), statistics.mode(feedbacks)])
            writer.writerow(
                ['Дисперсия', round(statistics.pvariance(price), 3), round(statistics.pvariance(discount), 3),
                 round(statistics.pvariance(rating), 3),
                 round(statistics.pvariance(amount), 3), round(statistics.pvariance(feedbacks), 3)])
            writer.writerow(
                ['Стандартное отклонение', round(statistics.pstdev(price), 3), round(statistics.pstdev(discount), 3),
                 round(statistics.pstdev(rating), 3),
                 round(statistics.pstdev(amount), 3), round(statistics.pstdev(feedbacks), 3)])

    def __create_csv(self):
        with open('data.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id','name','price','brand','supplier','discount','rating','amount','feedbacks','url'])

    def __save_csv(self,items):
        with open('data.csv', mode='a', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id, product.name, product.salePriceU/100, product.brand, product.supplier, product.sale, product.rating, product.volume, product.feedbacks,
                                 f'https://www.wildberries.ru/catalog/{product.id}/detail.aspx'])


class ParserSearch:
    def __init__(self, url: str):
        #self.search_name = self.__get_search_name(url)
        self.search_name = url

    @staticmethod
    def __get_search_name(url: str):

        regex = '(?<=search=).+'
        search_name = re.search(regex, url)[0]
        search_name = search_name.replace('%20',' ')

        return search_name

    def parse(self):
        i= 1
        self.__create_csv()
        while True:
            try:
                params = {
                    'TestGroup': 'no_test',
                    'TestID': 'no_test',
                    'appType': '1',
                    'curr': 'rub',
                    'dest': '-1257786',
                    'page': i,
                    'query': self.search_name,
                    'resultset': 'catalog',
                    'sort': 'popular',
                    'spp': '32',
                    'suppressSpellcheck': 'false',
                }

                response = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/search', params=params)
                items_info = models.Items.model_validate(response.json()['data'])
                i+=1
                if not items_info.products:
                    break
                self.__save_csv(items_info)
            except Exception:
                break

        with open("data.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = 0
            price = []
            discount = []
            rating = []
            amount = []
            feedbacks = []
            for row in file_reader:
                if count != 0:
                    price.append(float(row[2]))
                    discount.append(float(row[5]))
                    rating.append(float(row[6]))
                    amount.append(float(row[7]))
                    feedbacks.append(float(row[8]))
                count += 1
            print(round(sum(price) / len(price), 2))
        with open('statistics.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([' ', 'price', 'discount', 'rating', 'amount', 'feedbacks'])
            writer.writerow(['Среднее', (round(sum(price) / len(price), 2)), (round(sum(discount) / len(discount), 2)),
                             (round(sum(rating) / len(rating), 2)),
                             (round(sum(amount) / len(amount), 2)), (round(sum(feedbacks) / len(feedbacks), 2))])
            writer.writerow(
                ['Медиана', statistics.median(price), statistics.median(discount), statistics.median(rating),
                 statistics.median(amount), statistics.median(feedbacks)])
            writer.writerow(['Мода', statistics.mode(price), statistics.mode(discount), statistics.mode(rating),
                             statistics.mode(amount), statistics.mode(feedbacks)])
            writer.writerow(
                ['Дисперсия', round(statistics.pvariance(price), 3), round(statistics.pvariance(discount), 3),
                 round(statistics.pvariance(rating), 3),
                 round(statistics.pvariance(amount), 3), round(statistics.pvariance(feedbacks), 3)])
            writer.writerow(
                ['Стандартное отклонение', round(statistics.pstdev(price), 3), round(statistics.pstdev(discount), 3),
                 round(statistics.pstdev(rating), 3),
                 round(statistics.pstdev(amount), 3), round(statistics.pstdev(feedbacks), 3)])

    def __create_csv(self):
        with open('data.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id','name','price','brand','supplier','discount','rating','amount','feedbacks','url'])

    def __save_csv(self,items):
        with open('data.csv', mode='a', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            for product in items.products:
                if product.id!=301392582 and product.id!=344439646 and product.id!=390647600:
                    writer.writerow([product.id, product.name, product.salePriceU/100, product.brand, product.supplier, product.sale, product.rating, product.volume, product.feedbacks,
                                     f'https://www.wildberries.ru/catalog/{product.id}/detail.aspx'])





if __name__ == "__main__":
    #ParserBrand('https://www.wildberries.ru/brands/kingston').parse()
    #ParserSeller('https://www.wildberries.ru/seller/132324').parse()
    ParserSearch('серега пират').parse()

