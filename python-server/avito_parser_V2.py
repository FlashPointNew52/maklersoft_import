import requests  # пакет для работы с http (запросы и т.п.)
import special_function as sf  # модуль со всеми необходимыми соотвествиями
from time import sleep
from bs4 import BeautifulSoup  # пакет для анализа html страниц
from pprint import pprint  # пакет для "красивого" вывода информации в терминал
from re import findall  # пакет для работы с регулярными выражениями
from datetime import datetime  # пакет для определения времени


class AvitoParser():

    def get_html(self, url):
        attempt = 1  # счетчик попыток
        delay_sec = 0.5  # время задержки (в секундах)
        while attempt <= 10:  # 10 попыток на подключение
            self.req = requests.get(url)  # GET запрос по заданному url-адресу
            if self.req.status_code == requests.codes.ok:  # проверка, если код запроса равен 200
                return self.req.text  # возвращаем полученный html код страницы
            else:  # проверка, если код запроса НЕ равен 200
                attempt += 1  # +1 попытка
                sleep(delay_sec)  # задержка
        exit()

    def get_data(self, url):
        html_code = self.get_html(
            url)  # вызов функции get_html(функция для получения html кода) с параметром в виде url-адреса

        data = {
            'sourceMedia': None,
            'sourceUrl': None,
            'addDate': None,
            'address': None,
            'offerTypeCode': None,
            'categoryCode': None,
            'buildingType': None,
            'buildingClass': None,
            'typeCode': None,
            'phones_import': None,
            # 'owner_phones': None
        }  # сформирован dict(словарь), в котором находятся записи в формате ключ:значение

        # обозначение "глобальности" переменных
        global soup
        global breadcrumbs
        global info
        soup = BeautifulSoup(html_code, 'lxml').find('body')  # создание "дерева кода" для анализа страницы
        breadcrumbs = []  # объявление списка "хлебных крошек"
        tag_breadcrumbs = soup.find_all('a',
                                        class_='js-breadcrumbs-link js-breadcrumbs-link-interaction')  # получение "хлебных крошек"
        for i in tag_breadcrumbs:
            breadcrumbs.append(i.get_text().lower())  # внесение каждой "крошки" в список

        info = self.get_info()  # вызов функции get_info(для получения всей информации из объявления)
        data['sourceMedia'] = 'avito'
        data['sourceUrl'] = url
        data['addDate'] = self.get_date()  # вызов функции get_date(для получения даты размещения объявления)
        data['address'] = self.get_address()  # вызов функции get_address(для получения адреса объекта)
        data[
            'offerTypeCode'] = self.get_offer_type_code()  # вызов функции get_offer_type_code(для получения типа предложения)
        data[
            'categoryCode'] = self.get_category_code()  # вызов функции get_category_code(для получения типа категории недвижимости)
        # data['buildingClass'] = self.get_building_class()  # вызов функции get_building_class(для получения типа недвижимости)
        # data['buildingType'] = self.get_building_type()  # вызов функции get_building_type(для получения типа дома)
        # data['typeCode'] = self.get_type_code()  # вызов функции get_type_code(для получения типа объекта)
        data['phones_import'] = self.get_phones(url)  # вызов функции get_phones(для получения номеров телефонов)
        # pprint(data)  # "красивый" вывод данных

        return data

    def get_info(self):
        info = {}  # сформирован словарь
        all_info = soup.find_all('li',
                                 class_='item-params-list-item')  # поиск всех записей с тегом <li> и определенным классом

        for unit in all_info:  # достаем по одной записи из всех записей
            unit_str = unit.get_text().lower().replace('\n', '').split(":")  # разбираем и редактируем запись
            key = unit_str[0]  # ключем является определяющее слово (пр. адрес)
            value = unit_str[1].replace(' ', '').replace('\xa0',
                                                         '')  # значением является информирующее слово (пр. ул.Ленина)
            info[key] = value  # записываем пару в словарь
        # pprint(info)

        return info

    def get_date(self):
        tag_date = soup.find('div',
                             class_='title-info-metadata-item')  # поиск одной записи с тегом <div> и определенным классом
        info_date = tag_date.get_text().replace('\n', '').replace('размещено',
                                                                  '')  # редактируем запись, избавляясь от лишних символов/слов
        dmy = findall(r'\w+',
                      info_date)  # используя регулярное выражение получаем список [номер объявления, когда размещена, 'в', часы, минуты]

        date_time = {
            'day': None,
            'month': None,
            'year': None,
            'hour': '12',
            'minute': '00',
            'second': '00'
        }  # сформирован словарь

        # разбираем дату и записываем необходимую информацию в словарь
        if dmy[1] == 'вчера':
            date_time['day'] = datetime.now().day - 1
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[3]
            date_time['minute'] = dmy[4]

        elif dmy[1] == 'сегодня':
            date_time['day'] = datetime.now().day
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[3]
            date_time['minute'] = dmy[4]

        else:
            date_time['day'] = dmy[1]
            date_time['month'] = sf.get_month(dmy[2])
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[4]
            date_time['minute'] = dmy[5]

        date = "{day}-{month}-{year} {hour}:{minute}:{second}".format(
            **date_time)  # формируем дату в "красивый" вид DD-MM-YY HH:MM:SS

        return date

    def get_address(self):
        tag_address = soup.find('span',
                                itemprop='streetAddress')  # поиск одной записи с тегом <span> и определенным классом
        address = tag_address.get_text().replace('\n', '')  # редактируем запись, избавляясь от лишних символов/слов

        return address

    def get_offer_type_code(self):
        # определение типа предложения с помощью "хлебных крошек"
        if breadcrumbs[
            5] == 'посуточно':  # если 6-й элемент списка содержит слово 'посуточно' => offer_type_code = short
            offer_type = breadcrumbs[5]
        else:  # иначе offer_type_code равен 4-му элементу списка (продам/сдам)
            offer_type = breadcrumbs[3]

        return sf.get_OTC(offer_type)

    def get_category_code(self):
        # определение типа категории недвижимости с помощью "хлебных крошек"
        category = breadcrumbs[2]

        if category == 'дома, дачи, коттеджи':
            category = breadcrumbs[4]

        return sf.get_CC(category)

    def get_building_class(self):
        # написать реализацию функции
        return None

    def get_building_type(self):
        # написать реализацию функции
        return None

    def get_type_code(self):
        # написать реализацию функции
        return None

    def get_phones(self, url):
        avito_mobile = url.replace('www', 'm')  # изменяем url с "компьютерной" версии, на мобильную версию

        tag_numbers = None
        while tag_numbers is None:  # "крутить" цикл, пока не поймана запись с заданным атрибутом
            mobile_html_code = self.get_html(avito_mobile)  # получение html кода мобильной версии сайта
            mobile_soup = BeautifulSoup(mobile_html_code, 'lxml')  # создание "дерева кода" для анализа страницы
            tag_numbers = mobile_soup.find(
                attrs={'data-marker': 'item-contact-bar/call'})  # поиск записи с определенным аттрибутом

        phones = []  # сформирован список телефонных номеров
        phone = tag_numbers['href'].replace('tel:+7', '8')  # получение номера из записи и редактирование номера
        phones.append(phone)  # добавим номер в список

        return phones

# if __name__ == '__main__':  # НАЧАЛО ТУТ)
#     avito_url = "https://www.avito.ru/habarovsk/kvartiry/7-k_kvartira_250_m_55_et._1043387500"  # необходимый url-адрес
#     local_url = 'http://localhost:9000/get_media_data?url=' + avito_url + '&ip=800.555.35.35'  # сформированная строка запроса к локальному серверу
#     myreq = requests.get(local_url)  # GET запрос к локальному серверу
#     print(myreq.text)  # вывод полученного ответа от сервера
