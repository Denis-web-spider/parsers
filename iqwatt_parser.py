import time
import requests
from bs4 import BeautifulSoup
import mysql.connector
import csv

class Bot:
    '''
    Бот собирает информацию о товарах в файлы csv (ссыка на изображение, цена, характеристики)
    '''

    def __init__(self, username='root', host='localhost', database='iqwatt', user_db_host_password='dghkjYFY989))900-'):

        self.username = username
        self.host = host
        self.database = database
        self.user_db_host_password = user_db_host_password

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        self.root_url = 'https://iqwatt.ru'

    def create_db(self):
        '''
        Создает базу данных mysql.
        '''

        connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.user_db_host_password
        )

        cursor = connection.cursor()

        try:
            cursor.execute(f'CREATE DATABASE {self.database}')
        except:
            print(f'База данных {self.database} уже существует')

    def connect_to_db(self):
        '''
        Соединяется с базой данных mysql.
        '''

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.user_db_host_password,
            database=self.database
        )

        self.cursor = self.connection.cursor(buffered=True)

    def create_category_table(self):
        '''
        Создает таблицу в базе данных. Если таблица существует, то перезаписывает её.
        '''

        self.cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        self.cursor.execute('DROP TABLE IF EXISTS category')
        self.cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        self.cursor.execute('''CREATE TABLE category (
                                                    id                  INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                                    category_name       VARCHAR(255),
                                                    url                 VARCHAR(255)
        )''')

    def create_product_table(self):
        '''
        Создает таблицу в базе данных. Если таблица существует, то перезаписывает её.
        '''

        self.cursor.execute('DROP TABLE IF EXISTS product')

        self.cursor.execute('''CREATE TABLE product (
                                                    id              INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                                    category_id     INT,
                                                    product_url     VARCHAR(255),
                                                    FOREIGN KEY (category_id) REFERENCES category (id)
        )''')

    def show_product_table_info(self):
        '''
        Извлекает всю информацию из таблицы 'product'.
        '''

        self.cursor.execute('SELECT * FROM product')

        return self.cursor.fetchall()

    def show_category_table_info(self):
        '''
        Извлекает всю информацию из таблицы 'category'.
        '''

        self.cursor.execute('SELECT * FROM category')

        return self.cursor.fetchall()

    def get_categories_url(self):
        '''
        Извлекает url каждой категории.
        '''

        cookies = {'cookie': 'shop_regions_env_key=5faadcfbb64cf1.07259153; path=/; samesite=None; secure'}

        response = requests.get(self.root_url, headers=self.headers, cookies=cookies)

        soup = BeautifulSoup(response.text, 'lxml')
        Q = "INSERT INTO category (category_name, url) VALUES (%s, %s)"

        val = []

        for i in soup.find_all('div', {'class': 'subcat-disclosed__el-name'}):

            name = i.a.get_text()
            url = self.root_url + i.a['href']
            val.append((name, url))

        for i in soup.find_all('div', {'class': 'subcat-menu__el position-relative'}):

            name = i.a.get_text()
            url = self.root_url + i.a['href']
            val.append((name, url))

        i = soup.find('div', {'class': 'js-subcatmenu-el has-subs subcat-menu__el position-relative'}).a
        name = i.get_text()
        url = self.root_url + i['href']
        val.append((name, url))

        name = soup.select_one('#header-nav-categories > div > div > div:nth-child(4) > a > div').get_text()
        url = self.root_url + soup.select_one('#header-nav-categories > div > div > div:nth-child(4) > a')['href']
        val.append((name, url))

        self.cursor.executemany(Q, val)

        self.connection.commit()

    def get_products_url(self):
        '''
        Извлекает url каждого товара.
        '''

        cookie = {'cookie': 'shop_regions_env_key=5faadcfbb64cf1.07259153; path=/; samesite=None; secure; products_per_page=64'}

        Q = 'INSERT INTO product (category_id, product_url) VALUES (%s, %s)'
        val = []

        for category_info in self.show_category_table_info():

            category_id = category_info[0]
            category_url = category_info[2]

            response = requests.get(category_url, headers=self.headers, cookies=cookie)

            soup = BeautifulSoup(response.text, 'lxml')

            for i in soup.find_all('a', {'class': 'products-list_item-img'}):
                product_url = self.root_url + i['href']

                val.append((category_id, product_url))

        self.cursor.executemany(Q, val)
        self.connection.commit()

    def get_product_info(self):
        '''
        Извлекает информацию о каждом продукте.
        Создает файлы csv.
        '''

        cookies = {'cookie': 'shop_regions_env_key=5faadcfbb64cf1.07259153; path=/; samesite=None; secure; mgo-mcw-leadgen-timeout=1'}

        self.cursor.execute('SELECT * FROM category, product WHERE category.id = product.category_id')
        tables_info = self.cursor.fetchall()

        file_count = 1
        product_count = 1

        previous_headers = []
        for row_info in tables_info:

            new_headers = []
            product_features = {}

            category_name = row_info[1]
            product_url = row_info[5]

            response = requests.get(product_url, headers=self.headers, cookies=cookies)
            print(response.status_code)

            soup = BeautifulSoup(response.text, 'lxml')

            name = soup.find('h1', {'class': 'product_name'}).get_text()
            price = soup.find('span', {'class': 'product__price price nowrap'})['data-price']
            img_url = self.root_url + soup.find('img', {'id': 'product-image'})['src']
            new_headers.append('name')
            new_headers.append('price')
            new_headers.append('img_url')
            product_features['name'] = name
            product_features['price'] = price
            product_features['img_url'] = img_url

            for tr in soup.find_all('tr', {'class': 'product_features-item'}):
                feature_name = tr.find('td', {'class': 'product_features-title'}).span.get_text()
                feature_value = tr.find('td', {'class': 'product_features-value'}).get_text()

                new_headers.append(feature_name)
                product_features[feature_name] = feature_value

            if product_count == 1:
                previous_headers = new_headers.copy()

            if previous_headers == new_headers and product_count == 1:
                file_name = f'{file_count}_{category_name}.csv'
                self.file = open(file_name, 'w', encoding='utf-16')
                self.writer = csv.DictWriter(self.file, fieldnames=new_headers)
                self.writer.writeheader()
                self.writer.writerow(product_features)

                product_count += 1

            elif previous_headers == new_headers:
                self.writer.writerow(product_features)

                product_count += 1

            if previous_headers != new_headers:
                self.file.close()
                file_count += 1
                product_count = 2
                previous_headers = new_headers.copy()

                file_name = f'{file_count}_{category_name}.csv'
                self.file = open(file_name, 'w', encoding='utf-16')
                self.writer = csv.DictWriter(self.file, fieldnames=new_headers)
                self.writer.writeheader()
                self.writer.writerow(product_features)

            time.sleep(1)

        self.file.close()


bot = Bot()

bot.create_db()
bot.connect_to_db()
bot.create_category_table()
bot.create_product_table()
bot.get_categories_url()
bot.get_products_url()
bot.get_product_info()
