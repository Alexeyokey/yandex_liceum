API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

def geocode(adress):
    geocoder_request = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={adress}&format=json'

    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(f"""Ошибка выполнения запроса : {response.status_code} ({response.reason})""")
    
    feature = json_response['response']['GeoObjectCollection']['featureMember']
    return feature[0]['GeoObject'] if feature else None

def get_adress_component(town, component_id):
    toponym = geocode(town)

    components = toponym['metaDataProperty']['GeocoderMetaData']['Address']['Components']

    return components[component_id]['name']

def get_coorinates(adress):
    toponym = geocode(adress)

    if not toponym:
        return None, None

    toponym_coords = toponym['Point']['pos']

    toponym_longitude, toponym_lattitude = toponym_coords.split(' ')
    return float(toponym_longitude), float(toponym_lattitude)
def get_ll_span(adress):
    toponym = geocode(adress)

    toponym_coords = toponym['Point']['pos']

    toponym_longitude, toponym_lattitude = toponym_coords.split(' ')
    ll = ','.join([toponym_longitude, toponym_lattitude])

    envelope = toponym['boundedBy']['Envelope']

    l, b = envelope['lowerCorner'].split(' ')
    r, t = envelope['upperCorner'].split(' ')

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    spn = f'{dx},{dy}'

    return ll, spn 

import pygame
import requests
import sys
import os


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)