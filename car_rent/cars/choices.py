from core.types import Choices


class FUEL_TYPE_CHOICES(Choices):
    '''Choices of fuel type'''
    AI_92 = '92'
    AI_95 = '95'
    AI_100 = '10'
    GAS = 'GS'
    DIESEL = 'DT'
    ELECTRO = 'EL'

    CHOICES = (
        (AI_92, 'АИ-92'),
        (AI_95, 'АИ-95'),
        (AI_100, 'АИ-100'),
        (GAS, 'Газ'),
        (DIESEL, 'Дизельное топливо'),
        (ELECTRO, 'Электричество'),
    )


class DRIVE_CHOICES(Choices):
    '''Choices of drive'''
    RWD = 'RWD'
    FWD = 'FWD'
    AWD = 'AWD'

    CHOICES = (
        (RWD, 'Задний привод'),
        (FWD, 'Передний привод'),
        (AWD, 'Полный привод'),
    )


class GEARBOX_CHOICES(Choices):
    '''Choices of gearbox'''
    MANUAL = 'MA'
    AUTOMATIC = 'AU'
    ROBOT = 'AR'
    CVT = 'AC'

    CHOICES = (
        (MANUAL, 'Механическая'),
        (AUTOMATIC, 'Автоматическая'),
        (ROBOT, 'Робот'),
        (CVT, 'Вариатор'),
    )


class BODY_TYPE_CHOCIES(Choices):
    '''Choices of body type'''
    SEDAN = 'SE'
    LIFTBACK = 'LF'
    COUPE = 'CP'
    HATCHBACK_3 = 'H3'
    HATCHBACK_5 = 'H5'
    STATION_WAGON = 'SW'
    SUV_3 = 'S3'
    SUV_5 = 'S5'
    MINIVAN = 'MV'
    PICKUP = 'PC'
    LIMOUSINE = 'LM'
    VAN = 'VN'
    CABRIOLET = 'CB'

    CHOICES = (
        (SEDAN, 'Седан'),
        (LIFTBACK, 'Лифтбек'),
        (COUPE, 'Купе'),
        (HATCHBACK_3, 'Хэтчбек 3 дв.'),
        (HATCHBACK_5, 'Хэтчбек 5 дв.'),
        (STATION_WAGON, 'Универсал'),
        (SUV_3, 'Внедорожник 3 дв.'),
        (SUV_5, 'Внедорожник 5 дв.'),
        (MINIVAN, 'Минивен'),
        (PICKUP, 'Пикап'),
        (LIMOUSINE, 'Лимузин'),
        (VAN, 'Фургон'),
        (CABRIOLET, 'Кабриолет'),
    )


class CAR_STATUS_CHOICES(Choices):
    '''Choices of status'''
    NOT_VERIFIED = 100
    VERIFIED = 200
    ARCHIVED = 300
    BANNED = 400

    CHOICES = (
        (NOT_VERIFIED, 'Не проверено'),
        (VERIFIED, 'Проверено'),
        (ARCHIVED, 'Архивировано'),
        (BANNED, 'Заблокировано'),
    )
