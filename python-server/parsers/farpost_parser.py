import requests
import special_function as sf
import top_secret as ts

from bs4 import BeautifulSoup
from pprint import pprint
from re import findall
from datetime import datetime


def get_html(url):
    req = requests.get(url)
    # ДОДЕЛАТЬ
    if req.status_code != requests.codes.ok:
        print("Error")
        exit()
    else:
        return req.text


def main(url):
    start = datetime.now()
    print('Start: ', start)
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

    breadcrumbs = []
    tag_breadcrumbs = soup.find_all('span', itemprop='name')

    for i in tag_breadcrumbs:
        breadcrumbs.append(i.get_text().lower())

    # pprint(breadcrumbs)

    get_info()
    data['sourceMedia'] = 'farpost'
    data['sourceUrl'] = url
    data['addDate'] = get_date()
    data['address'] = get_address()
    data['offerTypeCode'] = get_offer_type_code()
    data['categoryCode'] = get_category_code()
    # data['buildingClass'] = get_building_class()
    # data['buildingType'] = get_building_type()
    # data['typeCode'] = get_type_code()
    data['phones_import'] = get_phones()
    pprint(data)

    end = datetime.now()
    print('End: ', end)

    print('Затрачено:', end - start)
    # return data


def get_info():
    global info
    info = {}
    all_info = soup.find_all('div', class_='field viewbull-field__container')

    for unit in all_info:
        key = unit.find(class_='label').get_text().lower()
        value = unit.span.get_text().replace('\t', '').replace('\n', '').replace('\xa0', '').replace('Подробности о '
                                                                                                     'доме ', '')
        info[key] = value

    # pprint(info)


def get_date():
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


def get_address():
    return info['адрес']


def get_offer_type_code():
    offer_type = breadcrumbs[2].split(' ')

    return sf.get_OTC(offer_type[0])


def get_category_code():
    if breadcrumbs[2] == 'продажа домов и коттеджей':
        return sf.get_CC(category_in_title())

    category = breadcrumbs[2].split(' ')

    return sf.get_CC(category[1])


def category_in_title():
    tag_title = soup.find('span', attrs={'data-field': 'subject', 'class': 'inplace'})
    title_text = tag_title.get_text().lower()

    house = 'дом'
    cottage = 'коттедж'

    if findall(house, title_text):
        return house
    elif findall(cottage, title_text):
        return cottage


def get_building_class():
    return None


def get_building_type():
    return None


def get_type_code():
    return None


def get_phones():
    cookies = ts.my_cook

    tag_id = soup.find('div', class_='actionsHeader')
    id_seller = tag_id.div.get_text().replace("№", '')

    ajax_url = "https://www.farpost.ru/bulletin/"+id_seller+"/ajax_contacts?paid=1&ajax=1"
    ajax_req = requests.post(ajax_url, cookies=cookies)
    ajax_html = ajax_req.text
    ajax_soup = BeautifulSoup(ajax_html, 'lxml')

    phones = []
    tag_number = ajax_soup.find_all('div', class_="new-contacts__td new-contact__phone")

    for phone in tag_number:
        phones.append(phone.get_text().replace('\t', '').replace('\n', '').replace('+7', '8'))

    return phones


if __name__ == '__main__':
    farpost_url = "https://www.farpost.ru/khabarovsk/realty/sell_houses/prodam-dom-kottedzh-56559753.html"
    main(farpost_url)
