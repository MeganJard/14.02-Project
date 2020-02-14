import os
import sys

import pygame
import requests

pygame.init()


def get_pic(coords='39 52', spn='0.005 0.005'):
    picserver = 'https://static-maps.yandex.ru/1.x/'
    picparams = {
        'l': 'map',
        'll': ','.join(coords.split()),
        'spn': ','.join(spn.split())
    }
    response = requests.get(picserver, params=picparams).content
    return response


map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(get_pic())
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
FPS = 50
running = True
clock = pygame.time.Clock()
img = pygame.image.load(map_file)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()

    screen.blit(img, (0, 0))
    clock.tick(FPS)

os.remove(map_file)
pygame.quit()
