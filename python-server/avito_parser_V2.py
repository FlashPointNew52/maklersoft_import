import requests  # пакет для работы с http (запросы и т.п.)
import special_function as sf  # модуль со всеми необходимыми соотвествиями
import time
import datetime
from bs4 import BeautifulSoup  # пакет для анализа html страниц
from pprint import pprint  # пакет для "красивого" вывода информации в терминал
from re import findall  # пакет для работы с регулярными выражениями
from datetime import datetime  # пакет для определения времени


class AvitoParser():

    def __get_html(self, url):
        attempt = 1  # счетчик попыток
        delay_sec = 0.5  # время задержки (в секундах)
        while attempt <= 10:  # 10 попыток на подключение
            self.req = requests.get(url, headers=sf.headers, timeout=5)  # GET запрос по заданному url-адресу
            if self.req.status_code == requests.codes.ok:  # проверка, если код запроса равен 200
                return self.req.text  # возвращаем полученный html код страницы
            else:  # проверка, если код запроса НЕ равен 200
                attempt += 1  # +1 попытка
                time.sleep(delay_sec)  # задержка
        exit()

    def get_data(self, url):
        html_code = self.__get_html(
            url)  # вызов функции get_html(функция для получения html кода) с параметром в виде url-адреса
        # pprint(html_code)
        data = {
            'id': None,
            'source_media': None,
            'source_url': None,
            'add_date': None,
            'offer_type_code': None,
            'type_code': None,
            'phones_import': None,

            'category_code': None,
            'building_type': None,
            'building_class': None,
            'address': None,
            # 'location_lat': None,
            # 'location_lon': None,
            'new_building': False
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

        info = self.__get_info()
        # pprint(info)
        # Обязательные поля
        data['id'] = self.__get_id()
        data['source_media'] = 'present'
        data['source_url'] = url
        data['add_date'] = self.__get_date()
        data['offer_type_code'] = self.__get_offer_type_code()
        # data['type_code'] = self.__get_type_code()
        data['phones_import'] = self.__get_phones(url)

        # Обязательные поля, но возможны значения по умолчанию
        data['category_code'] = self.__get_category_code()
        # data['building_class'] = self.__get_building_class()
        # data['building_type'] = self.__get_building_type(data['building_class'])
        data['address'] = self.__get_address()
        # data['new_building'] = self.__get_type_novelty()
        #
        # # Прочие поля
        # self.__get_price()
        # self.__get_photo_url()
        # self.__get_email()
        # self.__get_balcony()
        # self.__get_source_media_text()
        # self.__get_rooms_count()
        # self.__get_floor()
        # self.__get_square()
        # self.__get_condition()

        return data

    def __get_id(self):
        date_create = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                               datetime.now().minute, datetime.now().second)
        unix_id = int(time.mktime(date_create.timetuple()))

        return unix_id

    def __get_info(self):
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

    def __get_date(self):
        tag_date = soup.find('div',
                             class_='title-info-metadata-item')  # поиск одной записи с тегом <div> и определенным классом
        # pprint(tag_date)
        info_date = tag_date.get_text().replace('\n', '').replace('размещено',
                                                                  '')  # редактируем запись, избавляясь от лишних символов/слов
        # pprint(info_date)
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

        # date = "{day}-{month}-{year} {hour}:{minute}:{second}".format(**date_time)  # формируем дату в "красивый" вид DD-MM-YY HH:MM:SS
        date = datetime(int(date_time['year']), int(date_time['month']), int(date_time['day']), int(date_time['hour']),
                        int(date_time['minute']))

        unix_date = int(time.mktime(date.timetuple()))

        return unix_date

    def __get_address(self):
        tag_address = soup.find('span',
                                itemprop='streetAddress')  # поиск одной записи с тегом <span> и определенным классом
        address = tag_address.get_text().replace('\n', '')  # редактируем запись, избавляясь от лишних символов/слов

        return address

    def __get_offer_type_code(self):
        # определение типа предложения с помощью "хлебных крошек"
        if breadcrumbs[
            5] == 'посуточно':  # если 6-й элемент списка содержит слово 'посуточно' => offer_type_code = short
            offer_type = breadcrumbs[5]
        else:  # иначе offer_type_code равен 4-му элементу списка (продам/сдам)
            offer_type = breadcrumbs[3]

        return sf.get_OTC(offer_type)

    def __get_category_code(self):
        # определение типа категории недвижимости с помощью "хлебных крошек"
        category = breadcrumbs[2]

        if category == 'дома, дачи, коттеджи':
            category = breadcrumbs[4]

        return sf.get_CC(category)

    def __get_building_class(self):
        # написать реализацию функции
        return None

    def __get_building_type(self):
        # написать реализацию функции
        return None

    def __get_type_code(self):
        # написать реализацию функции
        return None

    def __get_phones(self, url):
        avito_mobile = url.replace('www', 'm')  # изменяем url с "компьютерной" версии, на мобильную версию

        tag_numbers = None
        while tag_numbers is None:  # "крутить" цикл, пока не поймана запись с заданным атрибутом
            mobile_html_code = self.__get_html(avito_mobile)  # получение html кода мобильной версии сайта
            mobile_soup = BeautifulSoup(mobile_html_code, 'lxml')  # создание "дерева кода" для анализа страницы
            tag_numbers = mobile_soup.find(
                attrs={'data-marker': 'item-contact-bar/call'})  # поиск записи с определенным аттрибутом

        phones = []  # сформирован список телефонных номеров
        phone = tag_numbers['href'].replace('tel:+7', '8')  # получение номера из записи и редактирование номера
        phones.append(phone)  # добавим номер в список

        return phones


if __name__ == '__main__':  # НАЧАЛО ТУТ)
    avito_url = "https://www.avito.ru/habarovsk/kvartiry/3-k_kvartira_58_m_55_et._1519616533"  # необходимый url-адрес
    # local_url = 'http://localhost:9000/get_media_data?url=' + avito_url + '&ip=800.555.35.35'  # сформированная строка запроса к локальному серверу
    # myreq = requests.get(local_url)  # GET запрос к локальному серверу
    # print(myreq.text)  # вывод полученного ответа от сервера
    X = AvitoParser()
    pprint(X.get_data(avito_url))
