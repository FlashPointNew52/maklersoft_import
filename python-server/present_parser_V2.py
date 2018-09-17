import requests
import special_function as sf
from time import sleep
from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


class PresentParser():

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

        tag_breadcrumbs = soup.find('div', class_='breadcrumbs')
        breadcrumbs = tag_breadcrumbs.get_text().lower().replace(' ', '').replace('\n', '').split("»")
        # pprint(breadcrumbs)

        info = self.get_info()
        data['sourceMedia'] = 'present'
        data['sourceUrl'] = url
        data['addDate'] = self.get_date()
        data['address'] = self.get_address()
        data['offerTypeCode'] = self.get_offer_type_code()
        data['categoryCode'] = self.get_category_code()
        data['buildingClass'] = self.get_building_class()
        data['buildingType'] = self.get_building_type(data['buildingClass'])
        data['typeCode'] = self.get_type_code()
        data['phones_import'] = self.get_phones()
        # pprint(data)

        return data

    def get_info(self):
        info = {}
        all_info = soup.find_all('div', class_='notice-card__field word-break')

        for unit in all_info:
            key = unit.strong.string.lower().replace(':', '')
            value = unit.span.get_text().replace('\r', ' ').replace('\n', ' ')
            info[key] = value

        # pprint(info)
        return info

    def get_date(self):
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

        date = "{day}-{month}-{year} {hour}:{minute}:{second}".format(**date_time)

        return date

    def get_address(self):
        if 'улица/переулок' in info:
            return info['улица/переулок']

        elif 'местоположение' in info:
            return info['местоположение']

    def get_offer_type_code(self):
        if breadcrumbs[4] == 'посуточно':
            return sf.get_OTC(breadcrumbs[4])
        else:
            return sf.get_OTC(breadcrumbs[2])

    def get_category_code(self):
        return sf.get_CC(breadcrumbs[3])

    def get_building_type(self, buildingClass):
        if breadcrumbs[3] == 'жилая' or breadcrumbs[3] == 'участкиидачи':
            return sf.get_BT(buildingClass)

        elif breadcrumbs[3] == 'коммерческая':
            if 'вид объекта' in info:
                return sf.get_BT(info['вид объекта'])
            else:
                return None

        else:
            return None

    def get_building_class(self):
        if breadcrumbs[3] == 'жилая':
            if breadcrumbs[4] == 'малосемейки':
                return sf.get_BC(breadcrumbs[4])

            elif breadcrumbs[4] == 'дома':
                if 'объект продажи' in info:
                    return sf.get_BC(info['объект продажи'])
                else:
                    return None

            elif breadcrumbs[4] == 'квартиры' or breadcrumbs[4] == 'комнаты':
                if 'планировка' in info:
                    return sf.get_BC(info['планировка'])
                else:
                    return None

            elif breadcrumbs[4] == 'комнаты,малосемейки':
                if 'объект аренды' in info:
                    return sf.get_BC(info['объект аренды'])
                else:
                    return None

            else:
                return None

        elif breadcrumbs[3] == 'коммерческая':
            return sf.get_BC('а+')

        elif breadcrumbs[3] == 'участкиидачи':
            if breadcrumbs[4] == 'дачи':
                return sf.get_BC(breadcrumbs[4])

            elif breadcrumbs[4] == 'участкикоммерческогоис/хназначения':
                return sf.get_BC('дачи')

            elif breadcrumbs[4] == 'индивидуальноестроительство':
                if 'дополнительно' in info:
                    pattr = 'ИЖС'
                    if findall(pattr, info['дополнительно']):
                        return sf.get_BC(pattr)
                    else:
                        return sf.get_BC('дача')
                else:
                    return sf.get_BC('дача')

        else:
            return None

    def get_type_code(self):
        if breadcrumbs[3] == 'жилая':
            if breadcrumbs[4] == 'малосемейки' or breadcrumbs[4] == 'комнаты':
                return sf.get_TC('комнаты')

            elif breadcrumbs[4] == 'дома':
                if 'объект продажи' in info:
                    return sf.get_TC(info['объект продажи'])
                else:
                    return None

            elif breadcrumbs[4] == 'квартиры':
                return sf.get_TC(breadcrumbs[4])

            elif breadcrumbs[4] == 'комнаты,малосемейки':
                if 'объект аренды' in info:
                    return sf.get_BC('комнаты')
                else:
                    return None

            else:
                return None

        elif breadcrumbs[3] == 'коммерческая':
            if 'вид объекта' in info:
                return sf.get_TC(info['вид объекта'])
            else:
                return None

        elif breadcrumbs[3] == 'участкиидачи':
            if breadcrumbs[4] == 'дачи':
                return sf.get_TC(breadcrumbs[4])
            else:
                return sf.get_TC('дачныйземельныйучасток')

        else:
            return None

    def get_phones(self):
        phones = []
        tag_numbers = soup.find('div', class_='media text-125').find('div', class_='media-body').find_all('a')

        for phone in tag_numbers:
            phones.append(str(phone.string))

        return phones


# if __name__ == '__main__':
#     present_url = "https://present-dv.ru/present/notice/view/4155206"
#     local_url = 'http://localhost:9000/get_media_data?url='+present_url+'&ip=800.555.35.35'
#     myreq = requests.get(local_url)
#     print(myreq.text)
