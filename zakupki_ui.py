import time
import requests
from bs4 import BeautifulSoup
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import sys
from pathlib import Path

class Ui_MainWindow(object):
    '''
    GUI созданный с помощью PyQt designer.
    '''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(536, 578)
        MainWindow.setWindowIcon(QIcon('icon.jpg'))
        MainWindow.setStyleSheet("background-color: #2f2f2f;\n"
                                    "color: #ffffff;\n"
                                     "\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 491, 491))
        self.frame.setStyleSheet("QFrame{\n"
                                "    background-color: #4b4b4b;\n"
                                "    font-size: 12px;\n"
                                "    color: #020202;\n"
                                "    border-radius: 6px;\n"
                                "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(30, 320, 431, 41))
        self.lineEdit.setStyleSheet("font-size: 16px;\n"
                                    "color: #f8f8f8;\n"
                                    "text-align: center;\n"
                                    "")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 290, 331, 20))
        self.label.setStyleSheet("color: #ffffff;\n"
                                    "font-size: 12px;")
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(180, 400, 121, 41))
        self.pushButton.setStyleSheet("QPushButton{\n"
                                        "    font-size: 16px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background: #000000;\n"
                                        "    border: 1px solid #ffffff;\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "    color: #000000;\n"
                                        "    background: #ffffff;\n"
                                        "    border: 1px solid #000000;\n"
                                        "}")
        self.pushButton.setObjectName("pushButton")

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.move(20, 20)
        self.label_2.setMinimumHeight(240)
        self.label_2.setMinimumWidth(450)
        self.label_2.setStyleSheet("background-color: #e8e8e8;\n"
                                    "font-size: 16px;\n"
                                    "padding: 10px;")
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.scroll = QScrollArea(self.frame)
        self.scroll.setStyleSheet('padding: 20px;')
        self.scroll.setFixedWidth(550)
        self.scroll.setWidget(self.label_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 536, 33))
        self.menubar.setStyleSheet("QMenuBar{\n"
                                    "    font-size: 16px;\n"
                                    "    background-color: #080808;\n"
                                    "    color: #e8e8e8;\n"
                                    "    border: 1px, solid, #e8e8e8;\n"
                                    "    padding: 3px;\n"
                                    "}\n"
                                    "QMenuBar::item:selected { \n"
                                    "    background-color: #e8e8e8;\n"
                                    "    color: #080808;\n"
                                    "}\n"
                                    "QMenu::item{\n"
                                    "    background: #4d4d4d;\n"
                                    "    font-size: 14px;\n"
                                    "    padding: 10px;\n"
                                    "    border: none;\n"
                                    "    margin: 0;\n"
                                    "}\n"
                                    "QMenu::item:selected {\n"
                                    "    background-color: #e8e8e8;\n"
                                    "    color: #080808;\n"
                                    "}\n"
                                    "\n"
                                    "QMenur::item:pressed {\n"
                                    "    color: #5bc53b;\n"
                                    "}")
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.menu.setFont(font)
        self.menu.setStyleSheet("\n"
                                "background-color: #080808;\n"
                                "color: #e8e8e8;\n"
                                "border: 1px, solid, #e8e8e8;\n"
                                "\n"
                                "")
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_txt = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)

        self.action_txt.setFont(font)
        self.action_txt.setObjectName("action_txt")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")

        self.menu.addAction(self.action_txt)
        self.menu_2.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label.setText(_translate("MainWindow", "Введиде код  \"2650102556820001007\""))

        self.pushButton.setText(_translate("MainWindow", "Парсинг"))

        self.menu.setTitle(_translate("MainWindow", "Добавить файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Настройки"))

        self.action_txt.setText(_translate("MainWindow", "Файл .txt"))
        self.action.setText(_translate("MainWindow", "Задержка перед запросом"))

class Bot(Ui_MainWindow):
    '''
    Бот на вход принимает файл txt или просто номер контакта.
    Скачивает все файлы из странички и сохраняет их по соответствующим категориям.
    '''
    def __init__(self):
        '''
        Соединяет сигналы нажатия на кнопки с событиями.
        Хранит все необходимые для работы переменные.
        '''

        self.main_url = 'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html'

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'routeepz0=4; contentFilter=; contractCsvSettingsId=5e691daa-fa66-404f-8eb3-3c9af005f3a4',
            'DNT': '1',
            'Host': 'zakupki.gov.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        self.MainWindow = QtWidgets.QMainWindow()
        super().setupUi(self.MainWindow)

        self.action_txt.triggered.connect(self.file_parser)
        self.pushButton.clicked.connect(self.parse)
        self.action.triggered.connect(self.time_dialog)

        self.text_to_print = ''
        self.time = 0

        self.MainWindow.show()

    def file_parser(self):
        '''
        Диалог файлов. Позволяет выбрать файл с пк пользователя.
        '''

        home_dir = str(Path.home())

        file_name = QFileDialog.getOpenFileName(None, 'Open .txt file', home_dir)[0]

        self.file_txt_to_parse = file_name

    def time_dialog(self, *args, **kwargs):
        '''
        Диалог предназначенный для установки время между скачиваниями файла, по умолчанию 0.
        '''

        dialog = QInputDialog(self.MainWindow)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle('Время (0, 0.5, 1)')
        dialog.setLabelText('Введите время:')
        dialog.resize(300, 300)
        dialog.setTextValue(f'{self.time}')
        bool = dialog.exec_()
        unswer = dialog.textValue()

        if bool and unswer:
            self.time = int(unswer)

    def parse(self):
        '''
        Реализует threading, что позволяет работать графическому интерфейсу без провисайний в то время, как будет работать парсер.
        '''

        number = self.lineEdit.text().strip()
        self.lineEdit.clear()
        self.workers = WorkThread(number, self.file_txt_to_parse, self.time)
        # запускает новый поток
        self.workers.start()
        # когда поступает сигнал, то вызывает функцию self.print_into_label()
        self.workers.update.connect(self.print_into_label)

    def print_into_label(self, value):
        '''
        Обновляет информацию на дисплее.

        value: новая строка
        '''

        self.text_to_print += value
        self.label_2.setText(self.text_to_print)
        self.label_2.adjustSize()

class WorkThread(QThread):
    '''
    Класс которые представляет собой новый поток.
    '''
    # создает экземпляр сигнала
    update = pyqtSignal(str)

    def __init__(self, number, file_txt, time):
        super().__init__()

        self.main_url = 'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'routeepz0=4; contentFilter=; contractCsvSettingsId=5e691daa-fa66-404f-8eb3-3c9af005f3a4',
            'DNT': '1',
            'Host': 'zakupki.gov.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        self.number = number
        self.file_txt = file_txt
        self.time = time

    def get_files_from_company_number(self, company_number, time_sleep=0):
        '''
        Производит выкачку файлов из сайта по номеру контакта.
        Создает сигнал для интерфейса.

        :param company_number: номер контакта
        :param time_sleep:     задержка между скачиваниями файла
        '''

        self.file_count = 0

        payload = {
            'reestrNumber': f'{company_number}',
            'backUrl': '2c308575-b3f2-422f-aafa-e236fde3a77c'
        }

        current_path = os.getcwd()
        path = current_path + f'\{company_number}'
        if not os.path.exists(path):
            os.makedirs(path)

        response = requests.get(self.main_url, params=payload, headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')

        for info_block in soup.find_all('div', {'class': 'row no-gutters notice-documents blockInfo__section first-row-active-documents closedInactiveDocuments'}):

            files = {}

            for i in info_block.find_all('span', {'class': 'section__value'}):

                file_name = i.a['title'].strip()
                for index, char in enumerate(file_name[::-1]):
                    if char == '.' and not file_name[len(file_name) - index].isdigit():
                        break
                    if char == '(':
                        index = len(file_name) - index - 1
                        file_name = file_name[:index]

                file_url = i.a['href']
                files[file_name] = file_url

            if files != {}:
                folder_name = info_block.find('div', {'class': 'section__value docName'}).get_text().strip()
                subpath = path + f'\{folder_name}'
                if not os.path.exists(subpath):
                    os.makedirs(subpath)

                for file_name in files:

                    self.file_count += 1

                    time.sleep(time_sleep)

                    full_file_path = subpath + f'\{file_name}'

                    r = requests.get(files[file_name], stream=True)

                    with open(full_file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=128):
                            f.write(chunk)

        for info_block in soup.find_all('div', {'class': 'row no-gutters notice-documents blockInfo__section row-active-documents'}):

            files = {}

            for i in info_block.find_all('span', {'class': 'section__value'}):

                file_name = i.a['title'].strip()
                for index, char in enumerate(file_name[::-1]):
                    if char == '.' and not file_name[len(file_name) - index].isdigit():
                        break
                    if char == '(':
                        index = len(file_name) - index - 1
                        file_name = file_name[:index]

                file_url = i.a['href']
                files[file_name] = file_url

            if files != {}:
                folder_name = info_block.find('div', {'class': 'section__value docName'}).get_text().strip()
                subpath = path + f'\{folder_name}'
                if not os.path.exists(subpath):
                    os.makedirs(subpath)

                for file_name in files:

                    self.file_count += 1

                    time.sleep(time_sleep)

                    full_file_path = subpath + f'\{file_name}'

                    r = requests.get(files[file_name], stream=True)

                    with open(full_file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=128):
                            f.write(chunk)

        # создает сигнал
        self.update.emit(f'{company_number} скачано {self.file_count} файла\n\n')

    def get_files_from_company_number_in_txt(self, txt_file, time_sleep=0):
        '''
        Производит чтение номеров с файла.
        Передает их функции self.get_files_from_company_number(number, time_sleep)

        :param txt_file:    файл .txt
        :param time_sleep:  задержка между скачиваниями файла
        '''

        file = open(txt_file, 'r')
        for number in file:
            number = number.strip()
            self.get_files_from_company_number(number, time_sleep)
        file.close()

    def run(self):

        try:
            self.get_files_from_company_number(self.number, self.time)
        except:
            pass

        try:
            self.get_files_from_company_number_in_txt(self.file_txt, self.time)
        except:
            pass


app = QtWidgets.QApplication(sys.argv)
ui = Bot()
sys.exit(app.exec_())
