from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import mysql.connector
from datetime import datetime

class InstaBot:
    '''
    Бот собирает информацию о людях (никнейм, количество публикаций, количество подписок и подписчиков),
    а также о их постах (лайки, время публикации, локацию, ссылку локацию, контент (фото, видео)) и сохраняет всё в две таблици в базе данных.
    Создает папку в рабочей директории, в ней создает папку для каждого человка (название папки это никнейм), в которую загружаются все посты (фото, видео),
    в порядке в котором они расположены в инстаграме.
    '''

    def __init__(self, username, password, db_name='instagram', host='localhost', user='root', password_db='dghkjYFY989))900-'):
        '''
        Заходит в профиль инстаграмма. Создает папку 'Posts'

        :param username:        ваш логин инстаграмм
        :param password:        ваш пароль инстаграмм
        :param db_name:         имя базы данных mysql
        :param host:            ip mysql сервера
        :param user:            имя пользователя mysql сервера
        :param password_db:     пароль сервера mysql
        '''

        self.username = username
        self.password = password
        self.database = db_name
        self.host = host
        self.user = user
        self.password_db = password_db

        self.main_table_name = 'Users'
        self.posts_table_name = 'Posts'

        self.root_insta_url = 'https://www.instagram.com/'

        google_exe = 'chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('headless')


        self.driver = webdriver.Chrome(google_exe, options=options)

        current_directory = os.getcwd()
        self.imgs_folder = 'Posts'
        self.path = current_directory + '\{}'.format(self.imgs_folder)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.driver.get(self.root_insta_url)

        time.sleep(2)

        username_input = self.driver.find_element_by_name('username').send_keys(self.username)
        password_input = self.driver.find_element_by_name('password').send_keys(self.password)
        submit_button = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()

        time.sleep(3)

        try:
            not_now = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        except:
            pass
        time.sleep(5)
        try:
            not_now = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except:
            pass

    def create_db(self):
        '''
        Создает базу данных mysql.
        '''

        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password_db,
        )

        cursor = db.cursor()

        try:
            cursor.execute('CREATE DATABASE {}'.format(self.database))
        except:
            print('База данных {} уже существует'.format(self.database))

    def connect_to_database(self):
        '''
        Соединяется с базой данных mysql.
        '''

        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password_db,
            database=self.database,
        )

        self.cursor = self.db.cursor(buffered=True)

    def create_main_table_in_db(self):
        '''
        Создает таблицу в базе данных. Если таблица существует, то перезаписывает её.
        '''

        self.cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        self.cursor.execute('DROP TABLE IF EXISTS {}'.format(self.main_table_name))
        self.cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        self.cursor.execute('''CREATE TABLE {} (
                                                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                                Никнейм VARCHAR(255),
                                                Публикаций VARCHAR(255),
                                                Подписчиков VARCHAR(255),
                                                Подписок VARCHAR(255),
                                                Ссылка_на_профиль VARCHAR(255)
        )'''.format(self.main_table_name))

    def create_post_table_in_db(self):
        '''
        Создает таблицу в базе данных. Если таблица существует, то перезаписывает её.
        '''

        self.cursor.execute('DROP TABLE IF EXISTS {}'.format(self.posts_table_name))

        self.cursor.execute('''CREATE TABLE {0} (
                                                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                                user_id INT,
                                                Лайки VARCHAR(255),
                                                Дата DATETIME,
                                                Локация VARCHAR(255),
                                                Ссылка_на_локацию VARCHAR(255),
                                                Контент LONGBLOB,
                                                Тип_контента VARCHAR(255),
                                                FOREIGN KEY (user_id)  REFERENCES {1} (id) ON DELETE CASCADE
        )'''.format(self.posts_table_name, self.main_table_name))

    def show_info_in_db_tables(self, user_id):
        '''
        Извлекает всю информацию из базы данных и возвращает курсор.
        '''

        self.cursor.execute('''SELECT * FROM {0}, {1} WHERE {1}.user_id = {0}.id and {0}.id = {2}'''.format(self.main_table_name, self.posts_table_name, user_id))

        return self.cursor

    def insert_info_in_db_main_table(self, nickname='NULL', count_posts='NULL', subscribers='NULL', subscribe='NULL', href='NULL'):
        '''
        Вставляет строку в таблицу    self.main_table_name = 'Users'.
        '''

        sql = 'INSERT INTO {} (Никнейм, Публикаций, Подписчиков, Подписок, Ссылка_на_профиль) VALUES (%s, %s, %s, %s, %s)'.format(self.main_table_name)
        val = (nickname, count_posts, subscribers, subscribe, href)
        self.cursor.execute(sql, val)

        self.cursor.execute('SELECT id FROM {} ORDER BY id DESC LIMIT 1'.format(self.main_table_name))

        self.last_user_id = self.cursor.fetchone()[0]

        self.db.commit()

    def insert_info_in_db_posts_table(self, likes='NULL', date='NULL', location='NULL', location_url='NULL', content='NULL', content_type='NULL'):
        '''
        Вставляет строку в таблицу   self.posts_table_name = 'Posts'.
        '''

        sql = 'INSERT INTO {} (user_id, Лайки, Дата, Локация, Ссылка_на_локацию, Контент, Тип_контента) VALUES (%s, %s, %s, %s, %s, %s, %s)'.format(self.posts_table_name)
        val = (self.last_user_id, likes, date, location, location_url, content, content_type)
        self.cursor.execute(sql, val)

        self.db.commit()

    def get_person_info(self, insta_url):
        '''
        Извлекает информацию о пользователе (никнейм, количество публикаций, количество подписок и подписчиков),
        а также о их постах (лайки, время публикации, локацию, ссылку локацию, контент (фото, видео)) и сохраняет всё в две таблици в базе данных.

        :param insta_url:   url инстаграм акаунта человека
        '''

        self.driver.get(insta_url)

        time.sleep(3)

        nickname = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text
        posts = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
        subscribers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
        subscribe = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text

        self.insert_info_in_db_main_table(nickname, posts, subscribers, subscribe, insta_url)

        try:
            # кликает на первый пост если у пользователя нету сохраненных историй
            first_post = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]'))
            )

            first_post.click()
        except:
            try:
                # кликает на первый пост если у пользователя есть сохраненные истории
                first_post = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]'))
                )

                first_post.click()
            except:
                pass

        while True:

            time.sleep(2.5)

            try:
                # собирает количество лайков
                likes = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button/span').text
            except:
                try:
                    # собирает количество лайков = просмотров "на видео"
                    likes = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span/span').text
                except:
                    # если ни один из выше перечисленных элементов не найден, то лайков нету
                    likes = '0'
            try:
                # время поста есть вседа, а если его нет, то это значит, что пост не успел прогрузиться и мы запускаем цикл заново (ждём еще 2.5 секунды)
                date = datetime.fromisoformat(self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[2]/a/time').get_attribute('datetime')[:19])
            except:
                continue

            try:
                location = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[2]/div[2]/a').text
                location_url = self.root_insta_url[:-1] + self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[2]/div[2]/a').get_attribute('href')
            except:
                location = 'Не указана'
                location_url = 'Нету'

            photo_set = False
            try:
                content_url = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div[1]/img').get_attribute('src')
            except:

                try:
                    content_url = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/img').get_attribute('src')
                except:
                    try:
                        content_url = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div/div/video').get_attribute('src')
                    except:
                        photo_set = True

            if photo_set == False:
                try:
                    content = requests.get(content_url)
                except requests.exceptions.MissingSchema:
                    continue
                content_type = content.headers['Content-type']
                content = content.content
                self.insert_info_in_db_posts_table(likes, date, location, location_url, content, content_type)

            else:

                count = 0
                used_content_url = []

                while True:

                    time.sleep(1)

                    content_urls = []

                    for index in (2, 3):
                        try:
                            content_url = self.driver.find_element_by_xpath(f'/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[{index}]/div/div/div/div[1]/div[1]/img').get_attribute('src')
                        except:
                            try:
                                content_url = self.driver.find_element_by_xpath(f'/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[{index}]/div/div/div/div[1]/img').get_attribute('src')
                            except:
                                try:
                                    content_url = self.driver.find_element_by_xpath(f'/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[{index}]/div/div/div/div[1]/div/div/video').get_attribute('src')
                                except Exception as e:
                                    print(e)

                        if content_url not in used_content_url and content_url != None:
                            content_urls.append(content_url)
                            used_content_url.append(content_url)

                    if content_urls != []:
                        for content_url in content_urls:
                            content = requests.get(content_url)
                            content_type = content.headers['Content-type']
                            content = content.content

                            self.insert_info_in_db_posts_table(likes, date, location, location_url, content, content_type)

                    try:
                        next_photo_in_seria = WebDriverWait(self.driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/button[2]/div'))
                        )
                        next_photo_in_seria.click()

                    except:
                        try:
                            if count == 0:
                                next_photo_in_seria = WebDriverWait(self.driver, 1).until(
                                    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/button/div'))
                                )
                                next_photo_in_seria.click()
                                count += 1
                            else:
                                break
                        except:
                            break
            try:
                next_post_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Далее'))
                )
                next_post_button.click()
            except:
                break

    def save_posts_in_folder(self):
        '''
        Сохраняем посты в паки. Паки находятся в папке 'Posts'.
        Имя каждой папки - никнейм.
        Имя поста - ПостId_ВремяПубликации.
        '''

        self.cursor.execute('SELECT id, Никнейм FROM {}'.format(self.main_table_name))

        users_info = {}

        for user_id_nick in self.cursor:
            user_id = user_id_nick[0]
            user_nickname = user_id_nick[1]

            new_folder_name = str(user_nickname)
            path = self.path + '\{}'.format(new_folder_name)
            if not os.path.exists(path):
                os.makedirs(path)

            users_info[user_id] = {}
            users_info[user_id]['path'] = path

        for user_id in users_info:
            for info in self.show_info_in_db_tables(user_id):

                path = users_info[user_id]['path']

                content_format = info[13].split('/')[-1]
                content_binary_data = info[12]
                post_id = info[6]

                post_datetime = info[9].strftime("%m_%d_%Y___%H_%M_%S")

                file_name = str(post_id) + '_' + post_datetime + '.' + content_format
                full_path_file = path + '\{}'.format(file_name)
                open(full_path_file, 'wb').write(content_binary_data)

    def gather_persons_info(self, *insta_urls):
        '''
        Собирает информацию о профилях.

        :param insta_urls:  ссылки на профили
        '''

        self.connect_to_database()

        for insta_url in insta_urls:

            try:
                self.get_person_info(insta_url)
            except:
                pass



bot = InstaBot('username', 'password')

bot.create_db()
bot.connect_to_database()
#bot.create_main_table_in_db()
#bot.create_post_table_in_db()

bot.gather_persons_info('https://www.instagram.com/vibepeddler/',
                        'https://www.instagram.com/alinagrosman/',
                        'https://www.instagram.com/neonguyen/',
                        'https://www.instagram.com/jxnlco/',
                        'https://www.instagram.com/theopioidcrisis_lookbook/',
                        'https://www.instagram.com/octaveperrault/',
                        'https://www.instagram.com/mamali_shafahi/',
                        'https://www.instagram.com/tahapx/',
                        'https://www.instagram.com/vedatmilorlezzetrehberi/')

bot.save_posts_in_folder()
