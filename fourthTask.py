import os
import sys

import pygame
import requests

pygame.init()

def draw_buttons():
    for i in range(3):
        if Buttons[i]:
            screen.blit(clickedButton, (500 + 25 * i, 400))
        else:
            screen.blit(normalButton, (500 + 25 * i, 400))


def get_pic(coords='39 52', spn='0.005 0.005', l='map'):
    picserver = 'https://static-maps.yandex.ru/1.x/'
    picparams = {
        'l': l,
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

spm = ['0.005 0.005', '0.01 0.01', '0.05 0.05', '0.1 0.1', '0.25 0.25', '0.5 0.5', '1 1', '2 2',
       '5 5', '10 10', '20 20', '30 30', '50 50']

Buttons = [False, False, False]
normalButton = pygame.transform.scale(pygame.image.load('data/normalButton.png'), (25, 25))
clickedButton = pygame.transform.scale(pygame.image.load('data/clickedButton.png'), (25, 25))

k = 0
screen = pygame.display.set_mode((600, 450))
pygame.display.flip()
FPS = 40
running = True
clock = pygame.time.Clock()
img = pygame.image.load(map_file)
first_c, sec_c = 39, 52
l = ['map', 'sat', 'sat,skl']
while running:
    try:
        with open(map_file, "wb") as file:
            try:
                file.write(get_pic(spn=spm[k], l=l[Buttons.index(True)],
                                   coords=' '.join([str(i) for i in [first_c, sec_c]])))
            except ValueError:
                file.write(get_pic(spn=spm[k],
                                   coords=' '.join([str(i) for i in [first_c, sec_c]])))
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    screen.blit(pygame.image.load(map_file), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == 281:
                if k < len(spm) - 1:
                    k += 1
            elif event.key == 280:
                if k > 0:
                    k -= 1
            elif event.key == pygame.K_UP:
                sec_c += (float(spm[k].split()[0]) * 2)
            elif event.key == pygame.K_DOWN:
                sec_c -= (float(spm[k].split()[0]) * 2)
            elif event.key == pygame.K_RIGHT:
                first_c += (float(spm[k].split()[1]) * 2)
            elif event.key == pygame.K_LEFT:
                first_c -= (float(spm[k].split()[1]) * 2)
            if first_c >= 180:
                first_c -= 359
            elif first_c <= - 180:
                first_c += 359
            if sec_c >= 86:
                sec_c -= 171
            elif sec_c <= -86:
                sec_c += 171
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clickedButton.get_rect(x=500, y=400).collidepoint(event.pos):
                Buttons = [True, False, False]
            elif clickedButton.get_rect(x=525, y=400).collidepoint(event.pos):
                Buttons = [False, True, False]
            elif clickedButton.get_rect(x=550, y=400).collidepoint(event.pos):
                Buttons = [False, False, True]
    draw_buttons()
    pygame.display.flip()
    clock.tick(FPS)

os.remove(map_file)
pygame.quit()
