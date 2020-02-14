import requests

def get_pic(geocode='Москва, Кремль', spn='0.005, 0.005'):

    geocode = geocode
    spn = spn

    geoserver = 'https://geocode-maps.yandex.ru/1.x/'

    geoparams = {
        'geocode':geocode,
        'spn': spn,
        'apikey':'40d1649f-0493-4b70-98ba-98533de7710b'
    }
    point = requests.get(geoserver, params=geoparams).json()["response"]["GeoObjectCollectio"
                                  "n"]["featureMember"][0]["GeoObject"]['Point']['po'
                                                                                 's']

    picserver = 'https://static-maps.yandex.ru/1.x/'

    picparams = {
    'l':'map',
    'll': ','.join(point.split()),
    'spn': ','.join(spn.split())
    }

    response = requests.get(picserver, params=picparams).content
    return response