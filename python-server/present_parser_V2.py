import requests
import special_function as sf
import time
import datetime
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


class PresentParser():

    def __get_html(self, url):
        attempt = 1
        delay_sec = 0.5
        while attempt <= 5:
            self.req = requests.get(url, headers=sf.headers)
            if self.req.status_code == requests.codes.ok:
                return self.req.text
            else:
                attempt += 1
                time.sleep(delay_sec)

        exit()

    def get_data(self, url):
        html_code = self.__get_html(url)

        global data

        data = {
            'id': None,
            'source_media': None,
            'source_url': None,
            'add_date': None,
            'offer_type_code': None,
            'type_code': None,
            'category_code': None,
            'phones_import': None,
            'address': None,

            'building_type': None,
            'building_class': None,
            # 'location_lat': None,
            # 'location_lon': None,
            'new_building': None,
            'object_stage': 'ready'
        }

        global soup
        global breadcrumbs
        global info
        soup = BeautifulSoup(html_code, 'lxml').find('body')

        tag_breadcrumbs = soup.find('div', class_='breadcrumbs')
        breadcrumbs = tag_breadcrumbs.get_text().lower().replace(' ', '').replace('\n', '').split("»")

        info = self.__get_info()
        # Обязательные поля
        data['id'] = self.__get_id()
        data['source_media'] = 'present'
        data['source_url'] = url
        data['add_date'] = self.__get_date()
        data['offer_type_code'] = self.__get_offer_type_code()
        data['type_code'] = self.__get_type_code()
        data['category_code'] = self.__get_category_code()
        data['phones_import'] = self.__get_phones()
        data['address'] = self.__get_address()

        # Обязательные поля, но возможны значения по умолчанию

        data['building_class'] = self.__get_building_class()
        data['building_type'] = self.__get_building_type()
        data['new_building'] = self.__get_type_novelty()
        # data['object_stage'] = self.__get_object_stage()

        # Прочие поля
        self.__get_price()
        self.__get_photo_url()
        self.__get_email()
        self.__get_balcony()
        self.__get_source_media_text()
        self.__get_rooms_count()
        self.__get_floor()
        self.__get_square()
        self.__get_condition()
        self.__get_house_type()

        return data

    def __get_info(self):
        info = {}
        all_info = soup.find_all('div', class_='notice-card__field word-break')

        for unit in all_info:
            key = unit.strong.string.lower().replace(':', '')
            value = unit.span.get_text().replace('\r', ' ').replace('\n', ' ')
            info[key] = value

        return info

    def __get_id(self):
        date_create = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                               datetime.now().minute, datetime.now().second)

        unix_id = int(time.mktime(date_create.timetuple()))

        return unix_id

    def __get_date(self):
        tag_date = soup.find('div', class_='items-bar__group items-bar__group--double-indent')
        info_date = tag_date.get_text().lower().replace('\n', '').replace('размещено:', '')
        dmy = findall(r'\w+', info_date)
        date_time = {
            'day': None,
            'month': None,
            'year': None,
            'hour': '12',
            'minute': '00',
            'second': '00'
        }

        if dmy[0] == 'вчера':
            date_time['day'] = datetime.now().day - 1
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year

        elif dmy[0] == 'сегодня':
            date_time['day'] = datetime.now().day
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[2]
            date_time['minute'] = dmy[3]

        else:
            date_time['day'] = dmy[0]
            date_time['month'] = sf.get_month(dmy[1])
            date_time['year'] = dmy[2]

        date = datetime(int(date_time['year']), int(date_time['month']), int(date_time['day']), int(date_time['hour']),
                        int(date_time['minute']))

        unix_date = int(time.mktime(date.timetuple()))

        return unix_date

    def __get_address(self):
        if 'улица/переулок' in info:
            return info['улица/переулок']

        elif 'улица' in info:
            return info['улица']

        elif 'местоположение' in info:
            return info['местоположение']

        else:
            return None

    def __get_type_novelty(self):
        try:
            if breadcrumbs[6] == 'новыеквартиры':
                return True

            elif 'новые квартиры' in info:
                if info['новые квартиры'] == 'да':
                    return True
                else:
                    return False
            else:
                return False

        except IndexError:
            return False

    def __get_offer_type_code(self):
        try:
            if breadcrumbs[4] == 'посуточно':
                return sf.get_OTC(breadcrumbs[4])
            else:
                return sf.get_OTC(breadcrumbs[2])
        except IndexError:
            return sf.get_OTC(breadcrumbs[2])

    def __get_category_code(self):
        return sf.get_CC(breadcrumbs[3])

    def __get_building_type(self):
        if breadcrumbs[3] == 'жилая':
            return sf.get_BT(data['building_class'])

        elif breadcrumbs[3] == 'участкиидачи':
            return sf.get_BT('dacha_land')

        elif breadcrumbs[3] == 'коммерческая' or breadcrumbs[3] == 'гаражи':
            if 'вид объекта' in info:
                if sf.get_BT(data['type_code']):
                    return sf.get_BT(data['type_code'])
                else:
                    data['type_code'] = 'other'
                    return sf.get_BT('other')
            else:
                data['type_code'] = 'other'
                return sf.get_BT('other')

    def __get_building_class(self):
        if breadcrumbs[3] == 'жилая':
            if breadcrumbs[4] == 'малосемейки':
                return sf.get_BC(breadcrumbs[4])

            elif breadcrumbs[4] == 'дома':
                if 'объект продажи' in info:
                    return sf.get_BC(info['объект продажи'])
                else:
                    return sf.get_BC('экономкласс')

            elif breadcrumbs[4] == 'квартиры' or breadcrumbs[4] == 'комнаты':
                if 'планировка' in info:
                    return sf.get_BC(info['планировка'])
                else:
                    return sf.get_BC('экономкласс')

            elif breadcrumbs[4] == 'комнаты,малосемейки':
                if 'объект аренды' in info:
                    return sf.get_BC(info['объект аренды'])
                else:
                    return sf.get_BC('экономкласс')

        elif breadcrumbs[3] == 'коммерческая' or breadcrumbs[3] == 'гаражи':
            return sf.get_BC('а')

        elif breadcrumbs[3] == 'участкиидачи':
            return None

    def __get_type_code(self):
        if breadcrumbs[3] == 'жилая':
            if 'количество комнат' in info:
                if findall('дол', info['количество комнат']):
                    return sf.get_TC('доля')

            if breadcrumbs[4] == 'малосемейки' or breadcrumbs[4] == 'комнаты':
                return sf.get_TC('комната')

            elif breadcrumbs[4] == 'дома':
                if 'объект продажи' in info:
                    return sf.get_TC(info['объект продажи'])
                else:
                    return sf.get_TC('дом')

            elif breadcrumbs[4] == 'квартиры':
                return sf.get_TC(breadcrumbs[4])

            elif breadcrumbs[4] == 'комнаты,малосемейки':
                if 'объект аренды' in info:
                    return sf.get_TC(info['объект аренды'])
                else:
                    return sf.get_TC('комната')

        elif breadcrumbs[2] == 'сдам' and breadcrumbs[3] == 'коммерческая':
            data['type_code'] = sf.get_TC(breadcrumbs[4])
            if 'вид объекта' in info:
                if sf.get_TC(info['вид объекта']):
                    return sf.get_TC(info['вид объекта'])
                else:
                    return data['type_code']

        elif breadcrumbs[3] == 'коммерческая':
            if 'вид объекта' in info:
                if sf.get_TC(info['вид объекта']):

                    return sf.get_TC(info['вид объекта'])
                else:
                    return sf.get_TC('другое')

        elif breadcrumbs[3] == 'участкиидачи':
            return sf.get_TC('дачныйземельныйучасток')

        elif breadcrumbs[3] == 'гаражи':
            return sf.get_TC('другое')

    def __get_phones(self):
        phones = []

        try:
            tag_numbers = soup.find('div', class_='media text-125').find('div', class_='media-body').find_all('a')

            for phone in tag_numbers:
                phones.append(str(phone.string))

            return phones
        except AttributeError:
            exit()

    def __get_price(self):
        check_tag_price = soup.find('div', class_='notice-card__financial-fields media')
        if check_tag_price:
            tag_price = check_tag_price.find('div', class_='media-body').find('p')
            price = int(tag_price.get_text().replace(' ', '').replace('\n', '').replace('\xa0', ''))
            data['price'] = float(price / 1000)

        else:
            return None

    def __get_photo_url(self):
        check_tag_photos = soup.find('div', class_='light-box')
        if check_tag_photos:
            tag_photos = check_tag_photos.find_all('div', class_='image-flex mb-1')
            data['photo_url'] = []
            for photo in tag_photos:
                data['photo_url'].append(photo.find('a')['href'])

        else:
            return None

    def __get_email(self):
        if 'e-mail' in info:
            data['mails_import'] = []
            data['mails_import'].append(info['e-mail'])

        else:
            return None

    def __get_balcony(self):
        if 'балкон/лоджия' in info:
            pattr = 'балкон'
            if findall(pattr, info['балкон/лоджия']):
                data['balcony'] = True

            pattr = 'лоджия'
            if findall(pattr, info['балкон/лоджия']):
                data['loggia'] = True

            if findall('без', info['балкон/лоджия']):
                data['balcony'] = False

        else:
            return False

    def __get_source_media_text(self):
        if 'дополнительно' in info:
            data['source_media_text'] = info['дополнительно']

        else:
            return None

    def __get_rooms_count(self):
        if 'количество комнат' in info:
            try:
                data['rooms_count'] = int(info['количество комнат'].split(' ')[0])
            except ValueError:
                try:
                    data['rooms_count'] = int(info['количество комнат'].split('-')[0])
                except ValueError:
                    return None
        else:
            return None

    def __get_floor(self):
        if 'этажность' in info:
            data['floor'] = int(info['этажность'])

        if 'этаж' in info:
            data['floor_count'] = int(info['этаж'])

        else:
            return None

    def __get_square(self):
        if 'площадь общая (кв. м)' in info:
            data['square_total'] = float(info['площадь общая (кв. м)'].replace(',', '.'))
        if 'общая площадь (кв. м)' in info:
            data['square_total'] = float(info['общая площадь (кв. м)'].replace(',', '.'))
        if 'площадь жилая (кв. м)' in info:
            data['square_living'] = float(info['площадь жилая (кв. м)'].replace(',', '.'))
        if 'площадь комнаты (кв. м)' in info and data['type_code'] == 'room' or data['type_code'] == 'share':
            data['square_living'] = float(info['площадь комнаты (кв. м)'].replace(',', '.'))
        if 'площадь кухни (кв. м)' in info:
            data['square_kitchen'] = float(info['площадь кухни (кв. м)'].replace(',', '.'))
        if 'площадь участка (сотки)' in info:
            data['square_land'] = float(info['площадь участка (сотки)'].replace(',', '.'))
            data['square_land'] = 'ar'
        if 'площадь (сотки)' in info:
            data['square_land'] = float(info['площадь (сотки)'].replace(',', '.'))
            data['square_land'] = 'ar'
        else:
            return None

    def __get_condition(self):
        if 'состояние' in info:
            data['condition_id'] = sf.get_condition(info['состояние'])
        else:
            return None

    def __get_house_type(self):
        if 'материал стен' in info:
            data['house_type'] = sf.get_house_type(info['материал стен'])

# if __name__ == '__main__':
#     present_url = "https://present-dv.ru/present/notice/view/4177349"
# #     # present_url = 'https://present-dv.ru/present/notice/view/4177623'
# #     # present_url = 'https://present-dv.ru/present/notice/view/4183842'
# #     # local_url = 'http://localhost:9000/get_media_data?url='+present_url+'&ip=800.555.35.35'
# #     # myreq = requests.get(local_url)
# #     # print(myreq.text)
#     X = PresentParser()
#     pprint(X.get_data(present_url))
