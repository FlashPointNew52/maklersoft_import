def get_month(x):
    month = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }

    return month[x]


def get_OTC(x):
    offerTypeCode = {
        'продам': 'sale',
        'сдам': 'rent',
        'посуточно': 'short',
        'продажа': 'sale',
        'аренда': 'rent',
        'квартиры': 'short'
    }

    return offerTypeCode[x]


def get_CC(x):
    categoryCode = {
        'жилая': 'REZIDENTIAL',
        'коммерческая': 'COMMERSIAL',
        'участкиидачи': 'LAND',

        'квартиры': 'REZIDENTIAL',
        'посуточная аренда квартир': 'REZIDENTIAL',
        'комнаты': 'REZIDENTIAL',
        'коммерческая недвижимость': 'COMMERSIAL',
        'дома': 'REZIDENTIAL',
        'дачи': 'LAND',
        'коттеджи': 'LAND',
        'посуточная аренда домов': 'REZIDENTIAL',
        'земельные участки': 'LAND',

        'квартир': 'REZIDENTIAL',
        'дом': 'REZIDENTIAL',
        'коттедж': 'LAND',
        'посуточно': 'REZIDENTIAL',
        'помещений': 'COMMERSIAL',
        'земельных': 'LAND',
        'дач': 'LAND',
    }

    return categoryCode[x]


def get_BT(x):
    buildingType = {

    }

    return buildingType[x]


def get_BC(x):
    buildingClass = {
        'элиткласс': 'elite',
        'бизнескласс': 'business',
        'экономкласс': 'econom',
        'улучшенная': 'improved',
        'новая': 'improved',
        'брежневка': 'brezhnev',
        'хрущевка': 'khrushchev',
        'сталинка': 'stalin',
        'старыйфонд': 'old_fund',
        'малосемейка': 'small_apartm',
        'общежитие': 'dormitory',
        'гостинка': 'gostinka',
        'индивидуальная': 'individual',
        'дом': 'single_house',
        'коттедж': 'cottage',
        'дача': 'dacha',
        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',
        'A+': 'A+'
    }

    return buildingClass[x]


def get_TC(x):
    typeCode = {
        'доля': 'share',
        'комната': 'room',
        'квартира': 'apartment',
        'дом': 'house',
        'коттедж': 'cottage',
        'дача': 'dacha',
        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',
        'дачныйземельныйучасток': 'dacha_land'
    }

    return typeCode[x]
