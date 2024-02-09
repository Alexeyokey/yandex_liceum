import pygame
import requests
from io import BytesIO
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def geocode(address):
    geocoder_request = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(f""""Ошибка выполнения запроса""")

    feature = json_response['response']['GeoObjectCollection']["featureMember"]
    return feature[0]['GeoObject'] if feature else None


def draw(screen: pygame.Surface, position):
    color = pygame.Color("green")
    pygame.draw.rect(screen, color, (*position, 100, 100), 0)


def get_ll_span(address, dx, dy):
    toponym = geocode(address)
    toponym_coords = toponym["Point"]['pos']
    toponym_longitude, toponym_lattitude = toponym_coords.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]['Envelope']
    l, b = envelope['lowerCorner'].split(' ')
    r, t = envelope['upperCorner'].split(' ')
    # dx = abs(float(l) - float(r)) / 2.0
    # dy = abs(float(t) - float(b)) / 2.0
    spn = f'{dx},{dy}'
    return ll, spn

#
# ll, spn = get_ll_span("55.713010, 37.660449", 0.1, 0.1)
# print(f"https://static-maps.yandex.ru/1.x/?lang=ru_RU&ll={ll}&spn={spn}&l=map")


if __name__ == "__main__":
    pygame.init()
    w, h = 600, 600
    size = (w, h)
    screen = pygame.display.set_mode((w, h))
    screen2 = pygame.display.set_mode((w, h))
    x1, y1, a, b = 0, 0, 0, 0
    drawing = False
    v = 60
    fps = 100
    x_pos = 0
    r = 20
    clock = pygame.time.Clock()
    running = True
    draw_cir = False
    position = (0, 0)
    # coords = []
    position = pygame.Vector2((0, 0))
    flag = 0
    coords = input("Введите координаты в формате: \n55.713010, 37.660449\n").split(', ')
    spn = (1, 1)
    # coords = [coords[1], coords[0]]
    response = requests.get(f'https://static-maps.yandex.ru/1.x/?lang=ru_RU&ll={coords[1]},{coords[0]}&spn={spn[0]},{spn[1]}&l=sat')
    img = pygame.image.load(BytesIO(response.content))
    # f1 = pygame.font.Font(None, 36)
    # text1 = f1.render('Введите координаты в формате: \n55.713010, 37.660449', True,
    #                   (255, 255, 255))
    while running:
        for event in pygame.event.get():
            screen2 = pygame.Surface(screen.get_size())
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = 1
                # speed.append([-1, -1])
            elif event.type == pygame.MOUSEMOTION and flag:
                position += event.rel
            elif event.type == pygame.MOUSEBUTTONUP:
                flag = 0

        screen2.fill(pygame.Color('black'))
        screen2.blit(img, (0,0))
        screen.blit(screen2, (0, 0))
        # screen.blit(text1, (0, 500))
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
