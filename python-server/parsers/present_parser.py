import requests
import special_function as sf

from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


def get_html(url):
    req = requests.get(url)
    # ДОДЕЛАТЬ!
    if req.status_code != requests.codes.ok:
        print("Error")
        exit()
    else:
        return req.text


def main(url):
    html_code = get_html(url)

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

    tag_breadcrumbs = soup.find('div', class_='breadcrumbs')
    breadcrumbs = tag_breadcrumbs.get_text().lower().replace(' ', '').replace('\n', '').split("»")
    pprint(breadcrumbs)

    get_info()
    data['sourceMedia'] = 'present'
    data['sourceUrl'] = url
    data['addDate'] = get_date()
    data['address'] = get_address()
    data['offerTypeCode'] = get_offer_type_code()
    data['categoryCode'] = get_category_code()
    data['buildingClass'] = get_building_class()
    data['buildingType'] = get_building_type(data['buildingClass'])
    data['typeCode'] = get_type_code()
    data['phones_import'] = get_phones()
    pprint(data)

    # return data


def get_info():
    global info
    info = {}
    all_info = soup.find_all('div', class_='notice-card__field word-break')

    for unit in all_info:
        key = unit.strong.string.lower().replace(':', '')
        value = unit.span.get_text().replace('\r', ' ').replace('\n', ' ')
        info[key] = value

    pprint(info)


def get_date():
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


def get_address():
    if 'улица/переулок' in info:
        return info['улица/переулок']

    elif 'местоположение' in info:
        return info['местоположение']


def get_offer_type_code():
    offer_type = breadcrumbs[2]

    return sf.get_OTC(offer_type)


def get_category_code():
    category = breadcrumbs[3]

    return sf.get_CC(category)


def get_building_type(buildingClass):
    if breadcrumbs[3] == 'жилая':
        return sf.get_BT(buildingClass)

    elif breadcrumbs[3] == 'коммерческая':
        if 'вид объекта' in info:
            return sf.get_BT(info['вид объекта'])
        else:
            return None

    elif breadcrumbs[3] == 'участкиидачи':
        return sf.get_BT(buildingClass)

    else:
        return None


def get_building_class():
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
            return sf.get_BC('дача')
        elif breadcrumbs[4] == 'индивидуальноестроительство':
            if 'дополнительно' in info:
                pattr = 'ИЖС'
                if findall(pattr, info['дополнительно']):
                    return sf.get_BC(pattr)
            else:
                return sf.get_BC('дача')

    else:
        return None


def get_type_code():
    if breadcrumbs[3] == 'жилая':
        if breadcrumbs[4] == 'малосемейки'  or breadcrumbs[4] == 'комнаты':
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


def get_phones():
    phones = []
    tag_numbers = soup.find('div', class_='media text-125').find('div', class_='media-body').find_all('a')

    for phone in tag_numbers:
        phones.append(str(phone.string))

    return phones


if __name__ == '__main__':
    present_url = "https://present-dv.ru/present/notice/view/4022576"
    main(present_url)
