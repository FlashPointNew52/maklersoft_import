from user_agent import generate_user_agent

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))
}

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

    try:
        return month.get(x.lower(), None)
    except AttributeError:
        return None


def get_OTC(x):
    offerTypeCode = {
        'продам': 'sale',
        'сдам': 'rent',
        'посуточно': 'short',
        'продажа': 'sale',
        'аренда': 'rent',
        'квартиры': 'short'
    }

    try:
        return offerTypeCode.get(x.lower(), None)
    except AttributeError:
        return None


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

    try:
        return categoryCode.get(x.lower(), None)
    except AttributeError:
        return None


def get_BT(x):
    buildingType = {
        'elite': 'multisection_house',
        'business': 'multisection_house',
        'economy': 'multisection_house',
        'improved': 'multisection_house',
        'brezhnev': 'multisection_house',
        'khrushchev': 'multisection_house',
        'stalin': 'multisection_house',
        'old_fund': 'multisection_house',

        'small_apartm': 'corridor_house',
        'dormitory': 'corridor_house',
        'gostinka': 'corridor_house',

        'individual': 'galary_house',

        'house': 'lowrise_house',
        'cottage': 'lowrise_house',
        'townhouse': 'lowrise_house',
        'duplex': 'lowrise_house',



        'dacha_land': 'agricultural_land',


        'помещение свободного назначения': 'gpurpose_place',
        'торговое помещение': 'market_place',
        'торговые площади': 'market_place',
        'производственное помещение': 'production_place',
        'здание': 'other',
        'здания': 'other',
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
        'other': 'production_place',
    }

    try:
        return buildingType.get(x.lower(), None)
    except AttributeError:
        return None


def get_BC(x):
    buildingClass = {
        'элиткласс': 'elite',
        'бизнескласс': 'business',
        'экономкласс': 'economy',
        'улучшенная': 'improved',
        'улучшенная планировка': 'improved',
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
        'индивидуальная планировка': 'individual',

        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',

        'коттедж': 'cottage',
        'дом': 'house',


        'а': 'A',
        'а+': 'A+',
        'b': 'B',
        'b+': 'B+',
        'c': 'C',
        'c+': 'C+'

    }

    try:
        return buildingClass.get(x.lower(), None)
    except AttributeError:
        return None


def get_TC(x):
    typeCode = {
        'доля': 'share',
        'комната': 'room',
        'комнаты': 'room',
        'комната в квартире': 'room',
        'малосемейка': 'room',
        'квартира': 'apartment',
        'квартиры': 'apartment',
        'дом': 'house',
        'коттедж': 'cottage',
        'таунхаус': 'townhouse',
        'дуплекс': 'duplex',


        'дачныйземельныйучасток': 'dacha_land',
        'садовыйземельныйучасток': 'garden_land',
        'огородныйземельныйучасток': 'cultivate_land',


        'отель' : 'hotel',
        'ресторан': 'restaurant',
        'кафе': 'cafe',
        'спортивный зал': 'sport_building',
        'спортивное сооружение': 'sport_building',
        'магазин': 'shop',
        'торговое помещение': 'shop',
        'торговый центр': 'shop_center',
        'тогово-развлекательный центр': 'shop_entertainment',
        'кабинет': 'cabinet',
        'офисное помещение': 'office_space',
        'офисное здание': 'office_building',
        'бизнес-центр': 'business_center',
        'бизнес центр': 'business_center',
        'производственное помещение': 'manufacture_building',
        'складское помещение': 'warehouse_space',
        'промышленное предприятие': 'industrial_enterprice',
        'другое': 'other',

        # 'помещение свободного назначения': 'gpurpose_place',
        # 'помещение под сферу услуг': 'other',
        # 'здание': 'other',
        # 'база': 'warehouse_space',


    }
    try:
        return typeCode.get(x.lower(), None)
    except AttributeError:
        return None


def get_condition(x):
    condition = {
        'хорошее': 2,
        'отличное': 2,
        'удовлетворительное': 2,
        'после строителей': 6,
        'соцремонт': 1,
        'сделан ремонт': 2,
        'после ремонта': 2,
        'евроремонт': 7,
        'дизайнерский ремонт': 3,
        'требуется ремонт': 4,
        'требуется капитальный ремонт': 4,
        'требуется косметический ремонт': 4,
        'ветхий': 4
    }

    try:
        return condition.get(x.lower(), None)
    except AttributeError:
        return None


def get_bathroom(x):
    bathroom = {
        'нет': 'no',
        'раздельный санузел': 'splited',
        'совмещенный санузел': 'combined',
        # 'в доме': 'combined',
        # 'на улице': 'no'
    }

    try:
        return bathroom.get(x.lower(), None)
    except AttributeError:
        return None


def get_house_type(x):
    house_type = {
        'панельный': 1,
        'деревянный': 2,
        'дерево': 2,
        'шлакоблочный': 3,
        'кирпичный': 4,
        'кирпич': 4,
        # 'каркасный' : '???',
        'блочный': 3,
        'монолитный': 5,
        'монолитный бетон': 5,
        'монолитно-кирпичный': 6,
    }

    try:
        return house_type.get(x.lower(), None)
    except AttributeError:
        return None


def get_room_scheme(x):
    room_scheme = {
        'свободная планировка': 1,
        'смежные': 5,
        'раздельные': 3,
        'смежно-раздельные': 4,
        'студия': 6,
        'другое': 2,
    }

    try:
        return room_scheme.get(x.lower(), 'other')
    except AttributeError:
        return 'other'


def get_object_stage(x):
    object_stage = {
        'в стадии проекта': 'project',
        'строящийся объект': 'building',
        'сданный объект': 'ready'
    }

    try:
        return object_stage.get(x.lower(), 'ready')
    except AttributeError:
        return 'ready'



