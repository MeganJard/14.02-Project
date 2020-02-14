import requests
import pygame


pygame.init()


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


class Paint(pygame.sprite.Sprite):
    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


FPS = 50
screen = pygame.display.set_mode((500, 500))
screen.fill((0, 0, 0))
pygame.display.flip()
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()
    p = Paint(get_pic(), [0, 0])
    screen.blit(p.image, p.rect)
    clock.tick(30)


pygame.quit()
