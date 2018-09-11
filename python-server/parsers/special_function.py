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

    return month.get(x.lower(), None)


def get_OTC(x):
    offerTypeCode = {
        'продам': 'sale',
        'сдам': 'rent',
        'посуточно': 'short',
        'продажа': 'sale',
        'аренда': 'rent',
        'квартиры': 'short'
    }

    return offerTypeCode.get(x.lower(), None)


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

    return categoryCode.get(x.lower(), None)


def get_BT(x):
    buildingType = {
        'elite': 'multisection_house',
        'business': 'multisection_house',
        'econom': 'multisection_house',
        'improved': 'multisection_house',
        'brezhnev': 'multisection_house',
        'khrushchev': 'multisection_house',
        'stalin': 'multisection_house',
        'old_fund': 'multisection_house',

        'small_apartm': 'corridor_house',
        'dormitory': 'corridor_house',
        'gostinka': 'corridor_house',

        'individual': 'galary_house',

        'single_house': 'lowrise_house',
        'cottage': 'lowrise_house',
        'townhouse': 'lowrise_house',
        'duplex': 'lowrise_house',

        'IZS!!!': 'settlements_land',
        'dacha': 'agricultural_land',

        'помещение свободного назначения': 'gpurpose_place',
        'торговое помещение': 'market_place',
        'производственное помещение': 'production_place',
        'здание': 'other',
        'база': 'production_place',
        'складское помещение': 'production_place',
        'офисное помещение': 'office',


        'hotel': 'gpurpose_place',
        'restaurant': 'gpurpose_place',
        'cafe': 'gpurpose_place',
        'sport_building': 'gpurpose_place',

        'shop': 'market_place',
        'shops_center': 'market_place',
        'shop_entertainment': 'market_place',

        'cabinet': 'office',
        'office_space': 'office',
        'office_building': 'office',
        'business_center': 'office',

        'manufacture_building': 'production_place',
        'warehouse_space': 'production_place',
        'industrial_enterprise': 'production_place',
    }

    return buildingType.get(x.lower(), None)


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
        'малосемейки': 'small_apartm',
        'малосемейка': 'small_apartm',
        'общежитие': 'dormitory',
        'гостинка': 'gostinka',
        'индивидуальная': 'individual',
        'дом': 'single_house',
        'дома': 'single_house',
        'коттедж': 'cottage',
        'дача': 'dacha',
        'дачи': 'dacha',
        'ИЖС': 'IZS!!!',
        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',
        'а+': 'A+'
    }

    return buildingClass.get(x.lower(), None)


def get_TC(x):
    typeCode = {
        'доля': 'share',
        'комната': 'room',
        'комнаты': 'room',
        'квартира': 'apartment',
        'квартиры': 'apartment',
        'дом': 'house',
        'коттедж': 'cottage',
        'дача': 'dacha',
        'дачи': 'dacha',
        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',
        'дачныйземельныйучасток': 'dacha_land',

        'помещение свободного назначения': 'gpurpose_place',
        'торговое помещение': 'shop',
        'производственное помещение': 'manufacture_building',
        'здание': 'other',
        'база': 'manufacture_building',
        'складское помещение': 'warehouse_space',
        'офисное помещение': 'office_space'
    }

    return typeCode.get(x.lower(), None)
