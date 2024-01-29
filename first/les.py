import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
from geocoder import get_coorinates, show_map, get_ll_span
# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
def main():
    toponym_to_find = " ".join(sys.argv[1:])

    if toponym_to_find:
        lat, lon = get_coorinates(toponym_to_find)
        ll_spn = f'll={lat},{lon}&spn-0.005,0.005'
        # show_map(ll_spn, 'map')

        ll, spn = get_ll_span(toponym_to_find)
        ll_spn = f'll={ll}&spn={spn}'

        point_param = f'pt={ll}'
        show_map(ll_spn, 'map', add_params=point_param)
    else:
        print('error')

if __name__ == '__main__':
    main()