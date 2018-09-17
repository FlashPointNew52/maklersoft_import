import requests
import special_function as sf
import top_secret as ts
from time import sleep
from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


class FarpostParser():

    def get_html(self, url):
        attempt = 1
        delay_sec = 0.5
        while attempt <= 5:
            self.req = requests.get(url)
            if self.req.status_code == requests.codes.ok:
                return self.req.text
            else:
                attempt += 1
                sleep(delay_sec)
        exit()

    def get_data(self, url):
        html_code = self.get_html(url)

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
        }

        global soup
        global breadcrumbs
        global info
        soup = BeautifulSoup(html_code, 'lxml').find('body')

        breadcrumbs = []
        tag_breadcrumbs = soup.find_all('span', itemprop='name')

        for i in tag_breadcrumbs:
            breadcrumbs.append(i.get_text().lower())

        # pprint(breadcrumbs)

        info = self.get_info()
        data['sourceMedia'] = 'farpost'
        data['sourceUrl'] = url
        data['addDate'] = self.get_date()
        data['address'] = self.get_address()
        data['offerTypeCode'] = self.get_offer_type_code()
        data['categoryCode'] = self.get_category_code()
        data['buildingClass'] = self.get_building_class()
        data['buildingType'] = self.get_building_type()
        data['typeCode'] = self.get_type_code()
        data['phones_import'] = self.get_phones()
        # pprint(data)

        return data

    def get_info(self):
        info = {}
        all_info = soup.find_all('div', class_='field viewbull-field__container')

        for unit in all_info:
            key = unit.find(class_='label').get_text().lower()
            value = unit.span.get_text().replace('\t', '').replace('\n', '').replace('\xa0', '').replace(
                'Подробности о '
                'доме ', '')
            info[key] = value

        # pprint(info)
        return info

    def get_date(self):
        tag_date = soup.find('span', class_='viewbull-header__actuality')
        info_date = tag_date.get_text()
        dmy = findall(r'\w+', info_date)

        date_time = {
            'day': None,
            'month': None,
            'year': None,
            'hour': '12',
            'minute': '00',
            'second': '00'
        }

        if dmy[2] == 'вчера':
            date_time['day'] = datetime.now().day - 1
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[0]
            date_time['minute'] = dmy[1]

        elif dmy[2] == 'сегодня':
            date_time['day'] = datetime.now().day
            date_time['month'] = datetime.now().month
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[0]
            date_time['minute'] = dmy[1]

        else:
            date_time['day'] = dmy[2]
            date_time['month'] = sf.get_month(dmy[3])
            date_time['year'] = datetime.now().year
            date_time['hour'] = dmy[0]
            date_time['minute'] = dmy[1]

        date = "{day}-{month}-{year} {hour}:{minute}:{second}".format(**date_time)

        return date

    def get_address(self):
        return info['адрес']

    def get_offer_type_code(self):
        offer_type = breadcrumbs[2].split(' ')

        return sf.get_OTC(offer_type[0])

    def get_category_code(self):
        if breadcrumbs[2] == 'продажа домов и коттеджей':
            return sf.get_CC(self.category_in_title())

        category = breadcrumbs[2].split(' ')

        return sf.get_CC(category[1])

    def category_in_title(self):
        tag_title = soup.find('span', attrs={'data-field': 'subject', 'class': 'inplace'})
        title_text = tag_title.get_text().lower()

        house = 'дом'
        cottage = 'коттедж'

        if findall(house, title_text):
            return house
        elif findall(cottage, title_text):
            return cottage

    def get_building_class(self):
        return None

    def get_building_type(self):
        return None

    def get_type_code(self):
        return None

    def get_phones(self):
        cookies = ts.my_cook

        tag_id = soup.find('div', class_='actionsHeader')
        id_seller = tag_id.div.get_text().replace("№", '')

        ajax_url = "https://www.farpost.ru/bulletin/" + id_seller + "/ajax_contacts?paid=1&ajax=1"
        ajax_req = requests.post(ajax_url, cookies=cookies)
        ajax_html = ajax_req.text
        ajax_soup = BeautifulSoup(ajax_html, 'lxml')

        phones = []
        tag_number = ajax_soup.find_all('div', class_="new-contacts__td new-contact__phone")

        for phone in tag_number:
            phones.append(phone.get_text().replace('\t', '').replace('\n', '').replace('+7', '8'))

        return phones

# if __name__ == '__main__':
#     farpost_url = "https://www.farpost.ru/khabarovsk/realty/sell_houses/prodam-dom-kottedzh-56559753.html"
#     local_url = 'http://localhost:9000/get_media_data?url='+farpost_url+'&ip=800.555.35.35'
#     myreq = requests.get(local_url)
#     print(myreq.text)
