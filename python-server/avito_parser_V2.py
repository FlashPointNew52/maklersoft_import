import requests
import special_function as sf

from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


class AvitoParser():

    def get_html(self, url):
        self.req = requests.get(url)
        if self.req.status_code != requests.codes.ok:
            print("Error")
            exit()
        else:
            return self.req.text

    def get_data(self, url):
        global avito_url
        avito_url = url

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
        soup = BeautifulSoup(html_code, 'lxml').find('body')
        breadcrumbs = []
        tag_breadcrumbs = soup.find_all('a', class_='js-breadcrumbs-link js-breadcrumbs-link-interaction')
        for i in tag_breadcrumbs:
            breadcrumbs.append(i.get_text().lower())

        self.get_info()
        data['sourceMedia'] = 'avito'
        data['sourceUrl'] = url
        data['addDate'] = self.get_date()
        data['address'] = self.get_address()
        data['offerTypeCode'] = self.get_offer_type_code()
        data['categoryCode'] = self.get_category_code()
        # data['buildingClass'] = self.get_building_class()
        # data['buildingType'] = self.get_building_type()
        # data['typeCode'] = self.get_type_code()
        data['phones_import'] = self.get_phones()
        # pprint(data)

        return data

    def get_info(self):
        global info
        info = {}
        all_info = soup.find_all('li', class_='item-params-list-item')

        for unit in all_info:
            str = unit.get_text().lower().replace('\n', '').split(":")
            key = str[0]
            value = str[1].replace(' ', '').replace('\xa0', '')
            info[key] = value

        # pprint(info)

    def get_date(self):
        tag_date = soup.find('div', class_='title-info-metadata-item')
        info_date = tag_date.get_text().replace('\n', '').replace('размещено', '')
        dmy = findall(r'\w+', info_date)

        date_time = {
            'day': None,
            'month': None,
            'year': None,
            'hour': '12',
            'minute': '00',
            'second': '00'
        }

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

        date = "{day}-{month}-{year} {hour}:{minute}:{second}".format(**date_time)

        return date

    def get_address(self):
        tag_address = soup.find('span', itemprop='streetAddress')
        address = tag_address.get_text().replace('\n', '')

        return address

    def get_offer_type_code(self):
        if breadcrumbs[5] == 'посуточно':
            offer_type = breadcrumbs[5]
        else:
            offer_type = breadcrumbs[3]

        return sf.get_OTC(offer_type)

    def get_category_code(self):
        category = breadcrumbs[2]

        if category == 'дома, дачи, коттеджи':
            category = breadcrumbs[4]

        return sf.get_CC(category)

    def get_building_class(self):
        return None

    def get_building_type(self):
        return None

    def get_type_code(self):
        return None

    def get_phones(self):
        avito_mobile = avito_url.replace('www', 'm')

        tag_numbers = None
        while tag_numbers is None:
            # print('!')
            mobile_html_code = self.get_html(avito_mobile)
            mobile_soup = BeautifulSoup(mobile_html_code, 'lxml')
            tag_numbers = mobile_soup.find(attrs={'data-marker': 'item-contact-bar/call'})

        phones = []
        phone = tag_numbers['href'].replace('tel:+7', '8')
        phones.append(phone)

        return phones

# if __name__ == '__main__':
#     X = AvitoParser()
#     avito_url = "https://www.avito.ru/habarovsk/kvartiry/7-k_kvartira_250_m_55_et._1043387500"
#     pprint(X.get_data(avito_url))
